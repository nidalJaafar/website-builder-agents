from langgraph.constants import START, END
from langgraph.graph import StateGraph

from website_builder.agents.task_manager_agent import task_manager_send, parse_tasks
from website_builder.models.state_models import TaskManagerState


def build_task_manager_graph():
    """Build the task manager subgraph"""
    graph = StateGraph(TaskManagerState)

    # Add nodes
    graph.add_node("generate_tasks", task_manager_send)
    graph.add_node("parse_tasks", parse_tasks)

    # Add edges
    graph.add_edge(START, "generate_tasks")
    graph.add_edge("generate_tasks", "parse_tasks")
    graph.add_edge("parse_tasks", END)

    return graph.compile()
