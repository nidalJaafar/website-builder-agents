from langgraph.constants import START, END
from langgraph.graph import StateGraph

from website_builder.agents.requirements_agent import user_message, send_message, should_continue, process_single_message
from website_builder.models.state_models import RequirementsState


def build_requirements_graph():
    """Build the requirements gathering subgraph for interactive CLI mode"""
    graph = StateGraph(RequirementsState)

    # Add nodes
    graph.add_node("user_message", user_message)
    graph.add_node("send_message", send_message)

    # Add edges
    graph.add_edge(START, "user_message")
    graph.add_edge("user_message", "send_message")
    graph.add_conditional_edges(
        "send_message",
        should_continue,
        {"yes": "user_message", "no": END},
    )

    return graph.compile()


def build_single_step_requirements_graph():
    """Build a single-step requirements graph for API conversational mode"""
    graph = StateGraph(RequirementsState)

    # Add node for processing a single message
    graph.add_node("process_message", process_single_message)

    # Simple flow: start -> process -> end
    graph.add_edge(START, "process_message")
    graph.add_edge("process_message", END)

    return graph.compile()
