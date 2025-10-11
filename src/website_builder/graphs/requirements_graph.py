from langgraph.constants import START, END
from langgraph.graph import StateGraph

from website_builder.agents.requirements_agent import process_single_message
from website_builder.models.state_models import RequirementsState


def build_single_step_requirements_graph():
    """Build a single-step requirements graph for API conversational mode"""
    graph = StateGraph(RequirementsState)

    # Add node for processing a single message
    graph.add_node("process_message", process_single_message)

    # Simple flow: start -> process -> end
    graph.add_edge(START, "process_message")
    graph.add_edge("process_message", END)

    return graph.compile()
