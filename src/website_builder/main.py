import asyncio

from dotenv import load_dotenv

from website_builder.config import PROJECT_WORKSPACE
from website_builder.graphs.orchestrator_graph import build_orchestrator_graph


async def run_orchestrator():
    print("\nStarting Multi-Graph Website Builder...")
    print(f"Project workspace: {PROJECT_WORKSPACE}")
    print("=" * 50)

    orchestrator = await build_orchestrator_graph()

    initial_state = {
        "user_input": "",
        "current_phase": "starting",
        "requirements_output": "",
        "tasks_output": [],
        "development_output": "",
        "project_status": "starting",
        "final_result": ""
    }

    try:
        async for step in orchestrator.astream(initial_state, config={"recursion_limit": 100000}, stream_mode=["custom", "updates"]):
            for node_name, state_update in step.items():
                print(f"Phase: {node_name}")
                if "current_phase" in state_update:
                    print(f"  Current Phase: {state_update['current_phase']}")
                if "final_result" in state_update and state_update["final_result"]:
                    print(f"  Result: {state_update['final_result']}")
                print("=" * 50)

    except Exception as e:
        print(f"Orchestrator error: {e}")


def main():
    async def main_async():
        load_dotenv()

        print("Website Builder System")
        print("=" * 50)
        await run_orchestrator()

    asyncio.run(main_async())
