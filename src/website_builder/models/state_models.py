from typing import TypedDict, Annotated, Sequence, List, Dict, Any, Union
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class JsonDecoderState(TypedDict):
    parsed_input_JSON: Dict[str, Any]
    parsed_text: List[BaseMessage]

class RequirementsState(TypedDict):
    requirements_messages: Annotated[Sequence[BaseMessage], add_messages]
    requirements_data: str
    user_input: str


class TaskManagerState(TypedDict):
    requirements_data: str
    tasks_messages: Annotated[Sequence[BaseMessage], add_messages]
    parsed_tasks: List[Dict[str, Any]]


class DeveloperState(TypedDict):
    parsed_tasks: List[Dict[str, Any]]
    current_task_index: int
    project_status: str
    developer_messages: Annotated[Sequence[BaseMessage], add_messages]
    project_context: Dict[str, Any]


class OrchestratorState(TypedDict):
    user_input: str
    current_phase: str
    requirements_output: Union[str, Sequence[BaseMessage]]
    tasks_output: List[Dict[str, Any]]
    development_output: str
    project_status: str
    final_result: str