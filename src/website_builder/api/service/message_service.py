import logging
from typing import Dict, Any

from fastapi import HTTPException
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from website_builder.db.crud import find_session_by_id, deserialize_state, update_session_state, \
    add_requirements_gatherer_output, initialize_session
from website_builder.db.database_models import Session
from website_builder.graphs.orchestrator_graph import build_orchestrator_graph
from website_builder.graphs.requirements_graph import build_single_step_requirements_graph
from website_builder.models.state_models import OrchestratorState, RequirementsState
from website_builder.prompts.requirements_prompts import requirements_system_prompt

logger = logging.getLogger(__name__)


async def service_send_chat_message(message_data: Dict[str, Any]):
    try:
        session_id = message_data.get("session_id", "")
        user_message = message_data.get("user_input", "")
        if not session_id or not user_message:
            raise HTTPException(status_code=400, detail="session_id and user_input are required.")
        session = find_session_by_id(session_id)
        result = __send_requirement_gathering_message(session, user_message)
        is_complete, agent_response = __check_if_completed(result)
        if is_complete:
            await __handle_completed_requirements(session)
        return {
            "agent_message": agent_response,
        }
    except Exception as e:
        logger.error(f"Chat message error: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


def service_start_requirements_chat(user_input: Dict[str, Any]):
    try:
        user_prompt = user_input.get("user_input", "")
        if not user_prompt:
            raise HTTPException(status_code=400, detail="user_input field is required.")
        session = initialize_session()
        requirements_state: RequirementsState = {
            "requirements_messages": [SystemMessage(content=requirements_system_prompt())],
            "requirements_data": "",
            "user_input": user_prompt
        }
        requirements_graph = build_single_step_requirements_graph()
        result = requirements_graph.invoke(requirements_state)
        update_session_state(session.id, result)
        last_message = result["requirements_messages"][-1]
        agent_response = last_message.content if hasattr(last_message, 'content') else str(last_message)
        return {
            "session_id": session.id,
            "agent_message": agent_response,
        }
    except Exception as e:
        logger.error(f"Chat start error: {e}")
        raise HTTPException(status_code=500, detail=f"Error starting conversation: {str(e)}")


def __send_requirement_gathering_message(session: Session, user_message: str):
    current_state = deserialize_state(session.state)
    current_state["requirements_messages"].append(HumanMessage(content=user_message))
    current_state["user_input"] = user_message
    requirements_graph = build_single_step_requirements_graph()
    result = requirements_graph.invoke(current_state)
    update_session_state(session.id, result)
    return result


def __check_if_completed(result: RequirementsState):
    last_message = result["requirements_messages"][-1]
    agent_response = last_message.content if hasattr(last_message, 'content') else str(last_message)
    return (isinstance(last_message, AIMessage) and
            hasattr(last_message, 'tool_calls') and
            last_message.tool_calls), agent_response


async def __handle_completed_requirements(session: Session):
    logger.info(f"Requirements complete for session {session.id}, proceeding to website building...")
    requirements_result = deserialize_state(session.state)
    orchestrator = await build_orchestrator_graph()
    initial_state: OrchestratorState = {
        "user_input": "",  # todo delete this from the orchestrator graph
        "current_phase": "requirements_complete",
        "requirements_output": requirements_result["requirements_messages"],
        "tasks_output": [],
        "development_output": "",
        "project_status": "starting",
        "final_result": "",
        "session_id": session.id
    }
    add_requirements_gatherer_output(session.id, requirements_result["requirements_messages"])
    logger.info("Starting orchestrator execution with completed requirements...")
    final_state = None
    async for step in orchestrator.astream(initial_state, config={"recursion_limit": 100000}):
        for node_name, state_update in step.items():
            logger.info(f"Phase: {node_name}")
            if "current_phase" in state_update:
                logger.info(f"Current Phase: {state_update['current_phase']}")
            if "final_result" in state_update and state_update["final_result"]:
                logger.info(f"Result: {state_update['final_result']}")
            final_state = state_update

    logger.info("Orchestrator execution completed")

    if not final_state:
        raise HTTPException(status_code=500, detail="No final state received from orchestrator")

    return {
        "status": "success",
        "message": "Requirements complete - proceeding to website creation",
        "final_result": final_state.get("final_result", ""),
        "project_status": final_state.get("project_status", "unknown"),
        "current_phase": final_state.get("current_phase", "unknown"),
        "auto_completed": True
    }
