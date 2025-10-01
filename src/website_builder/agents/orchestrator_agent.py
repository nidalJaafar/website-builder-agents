from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from website_builder.models.state_models import OrchestratorState, RequirementsState, TaskManagerState, DeveloperState
from website_builder.prompts.developer_prompts import developer_system_prompt
from website_builder.prompts.requirements_prompts import requirements_system_prompt
from website_builder.prompts.task_manager_prompts import task_manager_system_prompt


def route_entry_point(state: OrchestratorState) -> str:
    """Route to appropriate starting phase based on current state"""
    current_phase = state.get("current_phase", "starting")

    if current_phase == "requirements_complete":
        # Requirements already completed, skip to task management
        return "tasks"
    else:
        # Start with requirements gathering
        return "requirements"


def create_requirements_node(requirements_graph):
    def requirements_node(state: OrchestratorState) -> OrchestratorState:
        print("Starting Requirements Phase...")

        # Create requirements input state
        requirements_input: RequirementsState = {
            "requirements_messages": [SystemMessage(content=requirements_system_prompt())],
            "requirements_data": ""
        }

        # If user_input is provided (from API), pass it to the requirements graph
        if state.get("user_input"):
            print(f"Processing user input: {state['user_input'][:100]}...")
            requirements_input["user_input"] = state["user_input"]
        else:
            print("Using interactive requirements gathering...")

        # Execute the requirements graph
        requirements_result = requirements_graph.invoke(requirements_input)

        print("Requirements Phase Complete")

        return {
            "current_phase": "requirements_complete",
            "requirements_output": requirements_result["requirements_messages"][1:]
        }

    return requirements_node


def create_task_manager_node(task_manager_graph):
    def task_manager_node(state: OrchestratorState) -> OrchestratorState:
        print("Starting Task Management Phase...")

        # Handle different types of requirements_output
        if isinstance(state["requirements_output"], str):
            conversation_summary = state["requirements_output"]
        else:
            # Handle messages array (from requirements agent)
            conversation_summary = ""
            for msg in state["requirements_output"]:
                if isinstance(msg, HumanMessage):
                    conversation_summary += f"User: {msg.content}\n"
                elif isinstance(msg, AIMessage) and not msg.tool_calls:
                    conversation_summary += f"Assistant: {msg.content}\n"

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

    # Handle requirements output length calculation
    requirements_length = len(str(state["requirements_output"])) if state["requirements_output"] else 0

    summary = f"""
    Project Complete!

    Requirements: {requirements_length} characters gathered
    Tasks: {len(state["tasks_output"])} tasks generated  
    Development: {state["development_output"]}

    Your website has been successfully created!
    """

    return {
        "current_phase": "complete",
        "final_result": summary
    }
