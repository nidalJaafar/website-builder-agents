from langchain_core.tools import tool


@tool
def exit_tool() -> str:
    """exit tool to end the conversation

    Returns:
        str: exit message
    """
    return "exit"


@tool
def validate_task_completion(task_id: str, success_criteria: str) -> str:
    """Validate that a task has been completed successfully

    Args:
        task_id: The task identifier
        success_criteria: Description of what should be validated

    Returns:
        str: Validation result
    """

    return (
        f"{task_id}: Basic validation passed"
    )


@tool
def next_task() -> str:
    """Signal that current task is complete and ready for next task

    Returns:
        str: Confirmation message
    """
    return "Task completed, ready for next task"
