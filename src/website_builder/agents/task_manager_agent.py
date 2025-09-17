import re

from langchain_deepseek import ChatDeepSeek

from website_builder.models.state_models import TaskManagerState

task_manager_llm = ChatDeepSeek(model="deepseek-chat")


def task_manager_send(state: TaskManagerState) -> TaskManagerState:
    response = task_manager_llm.invoke(state["tasks_messages"])
    return {"tasks_messages": [response]}


import json


def parse_tasks(state: TaskManagerState) -> TaskManagerState:
    try:
        tasks_output = state["tasks_messages"][-1].content if state["tasks_messages"] else ""
        print(tasks_output)
        tasks_output = tasks_output.split("```json")[1].split("```")[0]
        tasks = json.loads(tasks_output.strip())
        print(tasks)
        return {"parsed_tasks": tasks}
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Raw output: {tasks_output}")
        return {"project_status": "error", "parsed_tasks": []}

    except Exception as e:
        print(f"Error parsing tasks: {e}")
        return {"project_status": "error", "parsed_tasks": []}
