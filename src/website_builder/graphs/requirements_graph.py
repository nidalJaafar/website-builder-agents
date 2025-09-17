from langgraph.constants import START, END
from langgraph.graph import StateGraph

from website_builder.agents.requirements_agent import user_message, send_message, should_continue
from website_builder.models.state_models import RequirementsState


def build_requirements_graph():
    """Build the requirements gathering subgraph"""
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
