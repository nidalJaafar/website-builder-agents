from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from website_builder.models.state_models import OrchestratorState, RequirementsState, TaskManagerState, DeveloperState
from website_builder.prompts.developer_prompts import developer_system_prompt
from website_builder.prompts.requirements_prompts import requirements_system_prompt
from website_builder.prompts.task_manager_prompts import task_manager_system_prompt


def create_requirements_node(requirements_graph):
    def requirements_node(state: OrchestratorState) -> OrchestratorState:
        print("Starting Requirements Phase...")

        requirements_input: RequirementsState = {
            "requirements_messages": [SystemMessage(content=requirements_system_prompt())],
            "requirements_data": ""
        }

        requirements_result = requirements_graph.invoke(requirements_input)

        print("Requirements Phase Complete")
        print(requirements_result)

        return {
            "current_phase": "requirements_complete",
            "requirements_output": requirements_result["requirements_messages"][1:]
        }

    return requirements_node


def create_task_manager_node(task_manager_graph):
    def task_manager_node(state: OrchestratorState) -> OrchestratorState:
        print("Starting Task Management Phase...")
        conversation_summary = ""

        print(state)

        for msg in state["requirements_output"]:
            if isinstance(msg, HumanMessage):
                conversation_summary += f"User: {msg.content}"
            elif isinstance(msg, AIMessage) and not msg.tool_calls:
                conversation_summary += f"Assistant: {msg.content}"

        task_manager_input: TaskManagerState = {
            "requirements_data": conversation_summary,
            "tasks_messages": [
                SystemMessage(content=task_manager_system_prompt()),
                HumanMessage(
                    content=f"Based on this requirements conversation, create a project plan: {conversation_summary}"
                ),
            ],
            "parsed_tasks": []
        }

        print("printing task manager input")
        print("printing task manager input")
        print("printing task manager input")
        print("printing task manager input")
        print("printing task manager input")
        print("printing task manager input")
        print("printing task manager input")
        print("printing task manager input")
        print("printing task manager input")
        print("printing task manager input")
        print(task_manager_input)

        task_result = task_manager_graph.invoke(task_manager_input)

        print(f"Task Management Complete - Generated {len(task_result['parsed_tasks'])} tasks")

        return {
            "current_phase": "tasks_complete",
            "tasks_output": task_result["parsed_tasks"]
        }

    return task_manager_node


def create_developer_node(developer_graph):
    async def developer_node(state: OrchestratorState) -> OrchestratorState:
        print(" Starting Development Phase...")

        developer_input: DeveloperState = {
            "parsed_tasks": state["tasks_output"],
            "current_task_index": 0,
            "project_status": "in_progress",
            "developer_messages": [SystemMessage(content=developer_system_prompt())],
            "project_context": {}
        }

        dev_result = await developer_graph.ainvoke(developer_input)

        print("Development Phase Complete")

        # Transform back to orchestrator state
        return {
            "current_phase": "development_complete",
            "development_output": dev_result["project_status"],
            "project_status": dev_result["project_status"]
        }

    return developer_node


def finalize_project_node(state: OrchestratorState) -> OrchestratorState:
    """Finalize the project and create summary"""
    print("Finalizing Project...")

    summary = f"""
    Project Complete!

    Requirements: {len(state["requirements_output"])} characters gathered
    Tasks: {len(state["tasks_output"])} tasks generated
    Development: {state["development_output"]}

    Your website has been successfully created!
    """

    return {
        "current_phase": "complete",
        "final_result": summary
    }
