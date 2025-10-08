from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from typing import Dict, Any, Optional
import json
import asyncio
import uuid
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from website_builder.db.crud import initialize_session, update_session_state, find_session_by_id, deserialize_state, \
    add_requirements_gatherer_output
from website_builder.db.database import init_db

# Load environment variables
load_dotenv()

from website_builder.graphs.orchestrator_graph import build_orchestrator_graph
from website_builder.graphs.requirements_graph import build_requirements_graph, build_single_step_requirements_graph
from website_builder.models.state_models import OrchestratorState, RequirementsState
from website_builder.prompts.requirements_prompts import requirements_system_prompt

app = FastAPI(
    title="Website Builder API",
    description="This API endpoint receives user inputs and processes them to build websites using AI agents.",
    version="1.0.0"
)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Website Builder API - AI-powered website creation",
        "version": "1.0.0",
        "endpoints": {
            "/submit": "POST - Submit user input to create a website",
            "/chat/start": "POST - Start a requirements gathering conversation",
            "/chat/message": "POST - Send a message in an ongoing conversation (auto-redirects to completion when requirements are done)",
            "/chat/complete": "POST - Complete requirements and build website",
            "/health": "GET - Health check",
            "/docs": "GET - API documentation"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test that we can import and initialize the orchestrator
        from website_builder.graphs.orchestrator_graph import build_orchestrator_graph
        return {
            "status": "healthy",
            "orchestrator": "available",
            "version": "1.0.0"
        }
    except Exception as e:
        return {
            "status": "unhealthy", 
            "error": str(e),
            "version": "1.0.0"
        }

@app.post("/chat/start")
async def start_requirements_chat(user_input: Dict[str, Any]):
    """
    Start a requirements gathering conversation
    
    Example:
    {
        "user_input": "I want to create a portfolio website"
    }
    
    Returns:
    {
        "session_id": "unique-session-id",
        "agent_message": "Agent's response/question"
    }
    """
    try:
        # Extract user input
        user_prompt = user_input.get("user_input", "")
        if not user_prompt:
            raise HTTPException(status_code=400, detail="user_input field is required.")
        
        # Create new session
        session = initialize_session()
        
        # Initialize requirements state
        requirements_state: RequirementsState = {
            "requirements_messages": [SystemMessage(content=requirements_system_prompt())],
            "requirements_data": "",
            "user_input": user_prompt
        }
        
        # Build requirements graph
        requirements_graph = build_single_step_requirements_graph()
        
        # Process the first user message
        result = requirements_graph.invoke(requirements_state)
        
        # Store session
        update_session_state(session.id, result)

        # Get the last agent message
        last_message = result["requirements_messages"][-1]
        agent_response = last_message.content if hasattr(last_message, 'content') else str(last_message)
        
        # Check if conversation is complete (agent used exit tool)
        is_complete = (isinstance(last_message, AIMessage) and 
                      hasattr(last_message, 'tool_calls') and 
                      last_message.tool_calls)
        
        return {
            "session_id": session.id,
            "agent_message": agent_response,
            "is_complete": is_complete
        }
        
    except Exception as e:
        print(f"[ERROR] Chat start error: {e}")
        import traceback
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error starting conversation: {str(e)}")


@app.post("/chat/message")
async def send_chat_message(message_data: Dict[str, Any]):
    """
    Send a message in an ongoing requirements conversation
    
    Example:
    {
        "session_id": "unique-session-id",
        "user_input": "Yes, I want it to have a dark theme"
    }
    
    Returns:
    {
        "agent_message": "Agent's response/question",
        "is_complete": false
    }
    
    OR if requirements are complete, automatically proceeds to website building:
    {
        "status": "success",
        "message": "Requirements complete - proceeding to website creation",
        "final_result": "...",
        "project_status": "complete",
        "current_phase": "...",
        "auto_completed": true
    }
    """
    try:
        session_id = message_data.get("session_id", "")
        user_message = message_data.get("user_input", "")
        
        if not session_id or not user_message:
            raise HTTPException(status_code=400, detail="session_id and user_input are required.")
        
        session = find_session_by_id(session_id)
        
        # Get current session state
        current_state = deserialize_state(session.state)
        
        # Add user message to conversation
        current_state["requirements_messages"].append(HumanMessage(content=user_message))
        current_state["user_input"] = user_message
        
        # Build requirements graph
        requirements_graph = build_single_step_requirements_graph()
        
        # Process the message
        result = requirements_graph.invoke(current_state)
        
        # Update session
        session = update_session_state(session.id, result)
        
        # Get the last agent message
        last_message = result["requirements_messages"][-1]
        agent_response = last_message.content if hasattr(last_message, 'content') else str(last_message)
        
        # Check if conversation is complete
        is_complete = (isinstance(last_message, AIMessage) and 
                      hasattr(last_message, 'tool_calls') and 
                      last_message.tool_calls)
        
        # If requirements are complete, automatically proceed to website building
        if is_complete:
            print(f"[DEBUG] Requirements complete for session {session_id}, proceeding to website building...")
            
            # Get the completed requirements conversation
            requirements_result = deserialize_state(session.state)
            
            # Build the orchestrator graph
            orchestrator = await build_orchestrator_graph()
            
            # Initialize the orchestrator state with completed requirements
            initial_state: OrchestratorState = {
                "user_input": "",  # Not needed since we have requirements
                "current_phase": "requirements_complete",
                "requirements_output": requirements_result["requirements_messages"],
                "tasks_output": [],
                "development_output": "",
                "project_status": "starting",
                "final_result": "",
                "session_id": session.id
            }

            add_requirements_gatherer_output(session.id, requirements_result["requirements_messages"])
            
            print("[DEBUG] Starting orchestrator execution with completed requirements...")
            
            # Execute the orchestrator graph starting from task management
            final_state = None
            async for step in orchestrator.astream(initial_state, config={"recursion_limit": 10000}):
                for node_name, state_update in step.items():
                    print(f"[DEBUG] Phase: {node_name}")
                    if "current_phase" in state_update:
                        print(f"[DEBUG] Current Phase: {state_update['current_phase']}")
                    if "final_result" in state_update and state_update["final_result"]:
                        print(f"[DEBUG] Result: {state_update['final_result']}")
                    final_state = state_update
            
            print("[DEBUG] Orchestrator execution completed")

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
        
        # If not complete, return normal chat response
        return {
            "agent_message": agent_response,
            "is_complete": is_complete
        }
        
    except Exception as e:
        print(f"[ERROR] Chat message error: {e}")
        import traceback
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


# @app.post("/chat/complete")
# async def complete_requirements_and_build(completion_data: Dict[str, Any]):
#     """
#     Complete requirements gathering and start building the website
    
#     Example:
#     {
#         "session_id": "unique-session-id"
#     }
    
#     Returns:
#     {
#         "status": "success",
#         "message": "Website creation completed successfully",
#         "final_result": "...",
#         "project_status": "complete"
#     }
#     """
#     try:
#         session_id = completion_data.get("session_id", "")
        
#         if not session_id:
#             raise HTTPException(status_code=400, detail="session_id is required.")
        
#         if session_id not in conversation_sessions:
#             raise HTTPException(status_code=404, detail="Session not found.")
        
#         # Get the completed requirements conversation
#         requirements_result = conversation_sessions[session_id]
        
#         # Build the orchestrator graph
#         orchestrator = await build_orchestrator_graph()
        
#         # Initialize the orchestrator state with completed requirements
#         initial_state: OrchestratorState = {
#             "user_input": "",  # Not needed since we have requirements
#             "current_phase": "requirements_complete",
#             "requirements_output": requirements_result["requirements_messages"],
#             "tasks_output": [],
#             "development_output": "",
#             "project_status": "starting",
#             "final_result": ""
#         }
        
#         print("[DEBUG] Starting orchestrator execution with completed requirements...")
        
#         # Execute the orchestrator graph starting from task management
#         final_state = None
#         async for step in orchestrator.astream(initial_state, config={"recursion_limit": 10000}):
#             for node_name, state_update in step.items():
#                 print(f"[DEBUG] Phase: {node_name}")
#                 if "current_phase" in state_update:
#                     print(f"[DEBUG] Current Phase: {state_update['current_phase']}")
#                 if "final_result" in state_update and state_update["final_result"]:
#                     print(f"[DEBUG] Result: {state_update['final_result']}")
#                 final_state = state_update
        
#         print("[DEBUG] Orchestrator execution completed")
        
#         # Clean up session
#         del conversation_sessions[session_id]
        
#         if not final_state:
#             raise HTTPException(status_code=500, detail="No final state received from orchestrator")
        
#         return {
#             "status": "success", 
#             "message": "Website creation completed successfully",
#             "final_result": final_state.get("final_result", ""),
#             "project_status": final_state.get("project_status", "unknown"),
#             "current_phase": final_state.get("current_phase", "unknown")
#         }
        
#     except Exception as e:
#         print(f"[ERROR] Completion error: {e}")
#         import traceback
#         print(f"[ERROR] Traceback: {traceback.format_exc()}")
#         raise HTTPException(status_code=500, detail=f"Error completing website creation: {str(e)}")


def main():
    import uvicorn
    init_db()
    uvicorn.run("website_builder.api.api:app", host="127.0.0.1", port=8080)

if __name__ == "__main__":
    main()
