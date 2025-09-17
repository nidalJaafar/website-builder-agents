from pathlib import Path

from dotenv import load_dotenv

from website_builder.config import PROJECT_WORKSPACE


def setup_project_workspace():
    """Set up the project workspace directory"""
    load_dotenv()

    workspace = Path(PROJECT_WORKSPACE)
    workspace.mkdir(exist_ok=True)

    print(f"Project workspace created at: {workspace.absolute()}")


def clean_project_workspace():
    """Clean the project workspace"""
    import shutil

    workspace = Path(PROJECT_WORKSPACE)
    if workspace.exists():
        shutil.rmtree(workspace)
        print("Project workspace cleaned")
    else:
        print("No workspace to clean")


async def visualize_all_graphs():
    """Generate visualization for all graphs"""
    load_dotenv()

    try:
        from website_builder.graphs.requirements_graph import build_requirements_graph
        from website_builder.graphs.task_manager_graph import build_task_manager_graph
        from website_builder.graphs.developer_graph import build_developer_graph
        from website_builder.graphs.orchestrator_graph import build_orchestrator_graph

        graphs_to_visualize = [
            (build_requirements_graph(), "requirements_graph.png"),
            (build_task_manager_graph(), "task_manager_graph.png"),
            (await build_developer_graph(), "developer_graph.png"),
            (build_orchestrator_graph(), "orchestrator_graph.png")
        ]

        for graph, filename in graphs_to_visualize:
            try:
                graph_image = graph.get_graph().draw_mermaid_png()
                with open(filename, "wb") as f:
                    f.write(graph_image)
                print(f"Saved {filename}")
            except Exception as e:
                print(f"Could not save {filename}: {e}")

    except Exception as e:
        print(f"Visualization error: {e}")
        import traceback
        traceback.print_exc()
