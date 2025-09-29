from langgraph.constants import START, END
from langgraph.graph import StateGraph

from website_builder.agents.orchestrator_agent import create_task_manager_node, create_requirements_node, \
    finalize_project_node, create_developer_node, route_entry_point
from website_builder.models.state_models import OrchestratorState


async def build_orchestrator_graph():
    from website_builder.graphs.requirements_graph import build_requirements_graph
    from website_builder.graphs.task_manager_graph import build_task_manager_graph
    from website_builder.graphs.developer_graph import build_developer_graph

    requirements_graph = build_requirements_graph()
    task_manager_graph = build_task_manager_graph()
    developer_graph = await build_developer_graph()

    graph = StateGraph(OrchestratorState)

    graph.add_node("requirements_phase", create_requirements_node(requirements_graph))
    graph.add_node("task_management_phase", create_task_manager_node(task_manager_graph))
    graph.add_node("development_phase", create_developer_node(developer_graph))
    graph.add_node("finalize_project", finalize_project_node)

    # Add conditional entry point
    graph.add_conditional_edges(
        START,
        route_entry_point,
        {
            "requirements": "requirements_phase",
            "tasks": "task_management_phase"
        }
    )
    
    # Add edges
    graph.add_edge("requirements_phase", "task_management_phase")
    graph.add_edge("task_management_phase", "development_phase")
    graph.add_edge("development_phase", "finalize_project")
    graph.add_edge("finalize_project", END)

    return graph.compile()
