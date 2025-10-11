import json
import logging

from json_repair import repair_json
from langchain_google_genai import ChatGoogleGenerativeAI

from website_builder.models.state_models import TaskManagerState

logger = logging.getLogger(__name__)

task_manager_llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro")


def task_manager_send(state: TaskManagerState) -> TaskManagerState:
    response = task_manager_llm.invoke(state["tasks_messages"])
    return {"tasks_messages": [response]}


def parse_tasks(state: TaskManagerState) -> TaskManagerState:
    try:
        tasks_output = state["tasks_messages"][-1].content if state["tasks_messages"] else ""
        logger.info(tasks_output)
        tasks_output = tasks_output.split("```json")[1].split("```")[0].strip()
        tasks = json.loads(repair_json(tasks_output.strip()))
        logger.info(tasks)
        return {"parsed_tasks": tasks}
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {e}")
        logger.error(f"Raw output: {tasks_output}")
        return {"project_status": "error", "parsed_tasks": []}

    except Exception as e:
        logger.error(f"Error parsing tasks: {e}")
        return {"project_status": "error", "parsed_tasks": []}
