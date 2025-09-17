from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

from website_builder.agents.developer_agent import execute_current_task, check_task_completion, advance_to_next_task, \
    project_complete
from website_builder.mcp.file_system import mcp_file_system_tools
from website_builder.models.state_models import DeveloperState
from website_builder.tools.validation_tools import validate_task_completion, next_task


async def build_developer_graph():
    """Build the developer execution subgraph"""
    graph = StateGraph(DeveloperState)

    # Create tool node that works with developer_messages field
    tools = await mcp_file_system_tools() + [validate_task_completion, next_task]
    tool_node = ToolNode(tools, messages_key="developer_messages")

    # Add nodes
    graph.add_node("agent", execute_current_task)
    graph.add_node("tools", tool_node)
    graph.add_node("advance_to_next_task", advance_to_next_task)
    graph.add_node("project_complete", project_complete)

    # Routing function
    def should_continue(state: DeveloperState) -> str:
        last_message = state["developer_messages"][-1]
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            # Check if next_task was called
            for tool_call in last_message.tool_calls:
                if tool_call["name"] == "next_task":
                    return "advance"
            return "tools"  # Execute other tools
        return "continue"  # No tools, continue with agent

    # Add edges
    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", should_continue, {
        "tools": "tools",
        "advance": "advance_to_next_task",
        "continue": "agent"
    })
    graph.add_edge("tools", "agent")  # After tools, back to agent

    graph.add_conditional_edges(
        "advance_to_next_task",
        lambda state: "complete" if state.get("project_status") == "completed" else "continue",
        {"continue": "agent", "complete": "project_complete"}
    )
    graph.add_edge("project_complete", END)

    return graph.compile()