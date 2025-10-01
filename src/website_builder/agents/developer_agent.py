from typing import List

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, RemoveMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from website_builder.config import PROJECT_WORKSPACE
from website_builder.mcp.file_system import mcp_file_system_tools
from website_builder.models.state_models import DeveloperState
from website_builder.tools.validation_tools import validate_task_completion, next_task

_developer_llm = None


async def get_developer_llm():
    global _developer_llm
    if _developer_llm is None:
        tools = await mcp_file_system_tools() + [validate_task_completion, next_task]
        _developer_llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro").bind_tools(tools)
    return _developer_llm

async def execute_current_task(state: DeveloperState) -> DeveloperState:
    """Execute the current task"""
    developer_llm = await get_developer_llm()
    try:
        if state["current_task_index"] >= len(state["parsed_tasks"]):
            return {"project_status": "completed"}

        current_task = state["parsed_tasks"][state["current_task_index"]]

        # Check if we need to add initial task message
        needs_task_message = True

        # Check if we already have a task message for the current task
        for msg in state["developer_messages"]:
            if isinstance(msg, HumanMessage) and "Execute this task:" in msg.content:
                # Extract task ID from existing message to see if it matches current task
                if current_task.get('id', 'Unknown') in msg.content:
                    needs_task_message = False
                    break

        if needs_task_message:
            context_info = ""
            if state.get("project_context"):
                context_info = f"\n**PROJECT CONTEXT:**\n{state['project_context']['summary']}\n\n"

            task_message = HumanMessage(
                content=f"Execute this task:\n\n"
                        + f"**Task ID:** {current_task.get('id', 'Unknown')}\n"
                        + f"**Title:** {current_task.get('title', 'Unknown')}\n"
                        + f"**Description:** {current_task.get('description', 'No description')}\n"
                        + f"**Files to work with:** {', '.join(current_task.get('files', []))}\n"
                        + f"**Success Criteria:** {current_task.get('success_criteria', 'No criteria specified')}\n"
                        + context_info
                        + f"Use the appropriate tools to complete this task, then use next_task when done.\n"
                        + f"**CRITICAL: After successfully completing ALL required files for a task, you MUST immediately call next_task.**"
            )
            messages = [*state["developer_messages"], task_message]
            response = await developer_llm.ainvoke(messages)
            return {"developer_messages": [task_message, response]}

        last_message = state["developer_messages"][-1]

        if isinstance(last_message, AIMessage) and hasattr(last_message, 'invalid_tool_calls') and last_message.invalid_tool_calls:
            error_responses = []
            for invalid_call in last_message.invalid_tool_calls:
                error_msg = f"""Tool call failed due to content size or formatting issues.
                ERROR: {invalid_call.get('error', 'Invalid tool call')}
                SOLUTION: Break your content into smaller pieces (under 1500 characters) and retry."""
                error_responses.append(ToolMessage(
                    content=error_msg,
                    tool_call_id=invalid_call['id']
                ))
            messages = [*state["developer_messages"], error_responses]
            response = await developer_llm.ainvoke(messages)
            return {"developer_messages": error_responses + [response]}

        messages = state["developer_messages"]
        response = await developer_llm.ainvoke(messages)
        return {"developer_messages": [response]}

    except Exception as e:
        return {
            "developer_messages": [AIMessage(content=f"Call failed with this exception {e} please try again")]
        }

def check_task_completion(state: DeveloperState) -> str:
    """Check if current task is complete and decide next action"""
    try:
        last_message = state["developer_messages"][-1]

        if isinstance(last_message, AIMessage) and last_message.tool_calls:
            # Check if next_task tool was called
            for tool_call in last_message.tool_calls:
                if tool_call["name"] == "next_task":
                    return "next_task"
            return "continue_task"

        # If no tool calls, assume task needs more work
        return "continue_task"

    except Exception:
        return "continue_task"


def advance_to_next_task(state: DeveloperState) -> DeveloperState:
    """Move to the next task with context preservation"""
    try:
        next_index = state["current_task_index"] + 1

        if next_index >= len(state["parsed_tasks"]):
            return {"project_status": "completed", "current_task_index": next_index}

        # Extract summary from the last AI message (before next_task call)
        task_summary = extract_task_summary(state)

        # Create context for next task
        project_context = build_project_context(state, task_summary)

        # Keep only system message + context summary
        system_message = None
        for msg in state["developer_messages"]:
            if isinstance(msg, SystemMessage):
                system_message = msg
                break

        context_message = HumanMessage(content=f"Previous task completed. Project context: {project_context}")

        return {
            "current_task_index": next_index,
            "project_context": {"summary": project_context},
            "developer_messages": [system_message, context_message]
        }

    except Exception as e:
        return {
            "project_status": "error",
            "developer_messages": [
                state["developer_messages"][0] if state["developer_messages"] else SystemMessage(content="Error"),
                AIMessage(content=f"❌ Error advancing to next task: {str(e)}"),
            ],
        }

def extract_task_summary(state: DeveloperState) -> str:
    """Extract summary from the last AI message"""
    for msg in reversed(state["developer_messages"]):
        if isinstance(msg, AIMessage) and msg.content:
            # Look for summary in the message content (before tool call)
            return msg.content
    return "Task completed"

def build_project_context(state: DeveloperState, task_summary: str) -> str:
    """Build context for next task"""
    current_task = state["parsed_tasks"][state["current_task_index"]]

    # Extract created files from message history
    created_files = extract_created_files_from_messages(state["developer_messages"])

    context = f"Project: Special Brew coffee shop website. "
    context += f"Completed: {current_task['title']}. "
    context += f"Files created: {', '.join(created_files)}. "
    context += f"Summary: {task_summary}"

    return context

def extract_created_files_from_messages(messages) -> List[str]:
    """Extract file paths from successful write_file calls"""
    created_files = []
    for msg in messages:
        if hasattr(msg, 'tool_calls'):
            for tool_call in msg.tool_calls:
                if tool_call['name'] == 'write_file':
                    created_files.append(tool_call['args']['path'])
    return created_files

def project_complete(state: DeveloperState) -> DeveloperState:
    """Handle project completion"""
    try:
        total_tasks = len(state["parsed_tasks"])

        return {
            "project_status": "completed",
            "developer_messages": [
                state["developer_messages"][0],
                AIMessage(
                    content=f"All {total_tasks} tasks completed successfully! Website development finished. Project files are available in: {PROJECT_WORKSPACE}"
                ),
            ],
        }

    except Exception as e:
        return {
            "project_status": "completed",
            "developer_messages": [
                SystemMessage(content="Project completion"),
                AIMessage(content=f"Project completed with some errors: {str(e)}"),
            ],
        }
