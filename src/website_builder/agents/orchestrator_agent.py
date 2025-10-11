import logging

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from website_builder.db.crud import find_session_by_id, add_task_manager_output, complete_session
from website_builder.models.state_models import OrchestratorState, RequirementsState, TaskManagerState, DeveloperState
from website_builder.prompts.developer_prompts import developer_system_prompt
from website_builder.prompts.requirements_prompts import requirements_system_prompt
from website_builder.prompts.task_manager_prompts import task_manager_system_prompt

logger = logging.getLogger(__name__)

def create_task_manager_node(task_manager_graph):
    def task_manager_node(state: OrchestratorState) -> OrchestratorState:
        logger.info("Starting Task Management Phase...")

        session = find_session_by_id(state["session_id"])

        # Handle different types of requirements_output
        if isinstance(state["requirements_output"], str):
            conversation_summary = state["requirements_output"]
        else:
            # Handle messages array (from requirements agent)
            conversation_summary = ""
            for msg in state["requirements_output"]:
                if isinstance(msg, HumanMessage):
                    conversation_summary += f"User: {msg.content}\n"
                elif isinstance(msg, AIMessage) and not msg.tool_calls:
                    conversation_summary += f"Assistant: {msg.content}\n"
        tasks = [
            SystemMessage(content=task_manager_system_prompt(session.id)),
            HumanMessage(
                content=f"Based on this requirements conversation, create a project plan: {conversation_summary}"
            ),
        ]
        if session.task_manager_output is not None:
            tasks.append(
                HumanMessage(
                    content=f"The following tasks have been already executed by the developer agent, create the additional tasks to finish the new requirements {session.task_manager_output}"
                )
            )

        task_manager_input: TaskManagerState = {
            "requirements_data": conversation_summary,
            "tasks_messages": tasks,
            "parsed_tasks": []
        }

        logger.info(f"Task manager input: {task_manager_input}")

        task_result = task_manager_graph.invoke(task_manager_input)

        logger.info(f"Task manager output: {task_result}")
        add_task_manager_output(session.id, task_result["parsed_tasks"])

        logger.info(f"Task Management Complete - Generated {len(task_result['parsed_tasks'])} tasks")

        return {
            "current_phase": "tasks_complete",
            "tasks_output": task_result["parsed_tasks"]
        }

    return task_manager_node


def create_developer_node(developer_graph):
    async def developer_node(state: OrchestratorState) -> OrchestratorState:
        logger.info(" Starting Development Phase...")

        developer_input: DeveloperState = {
            "parsed_tasks": state["tasks_output"],
            "current_task_index": 0,
            "project_status": "in_progress",
            "developer_messages": [SystemMessage(content=developer_system_prompt())],
            "project_context": {}
        }

        dev_result = await developer_graph.ainvoke(developer_input)

        logger.info("Development Phase Complete")

        # Transform back to orchestrator state
        return {
            "current_phase": "development_complete",
            "development_output": dev_result["project_status"],
            "project_status": dev_result["project_status"]
        }

    return developer_node


def finalize_project_node(state: OrchestratorState) -> OrchestratorState:
    """Finalize the project and create summary"""
    logger.info("Finalizing Project...")

    # Handle requirements output length calculation
    requirements_length = len(str(state["requirements_output"])) if state["requirements_output"] else 0

    summary = f"""
    Project Complete!

    Requirements: {requirements_length} characters gathered
    Tasks: {len(state["tasks_output"])} tasks generated  
    Development: {state["development_output"]}

    Your website has been successfully created!
    """

    complete_session(state["session_id"])

    return {
        "current_phase": "complete",
        "final_result": summary
    }
