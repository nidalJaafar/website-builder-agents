from langgraph.constants import START, END
from langgraph.graph import StateGraph

from website_builder.agents.json_parser_agent import user_message, send_message
from website_builder.models.state_models import JsonDecoderState


def build_json_parser_graph():
    """Build the JSON parsing subgraph"""
    graph = StateGraph(JsonDecoderState)

    # Add nodes
    graph.add_node("user_message", user_message)
    graph.add_node("send_message", send_message)

    # Add edges
    graph.add_edge(START, "user_message")
    graph.add_edge("user_message", "send_message")
    graph.add_edge("user_message", END)

    return graph.compile()
