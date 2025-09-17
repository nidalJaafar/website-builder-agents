from langchain_core.messages import HumanMessage, AIMessage
from langchain_deepseek import ChatDeepSeek

from website_builder.models.state_models import RequirementsState
from website_builder.tools.validation_tools import exit_tool

requirements_llm = ChatDeepSeek(model="deepseek-chat").bind_tools([exit_tool])


def user_message(state: RequirementsState) -> RequirementsState:
    if not any(
            msg for msg in state["requirements_messages"] if isinstance(msg, HumanMessage)
    ):
        input_text = "Hi, this is a website builder service. Add your website description here.\nUser: "
    else:
        input_text = "User: "
    message = HumanMessage(content=input(input_text))
    return {"requirements_messages": [message]}


def send_message(state: RequirementsState) -> RequirementsState:
    response = requirements_llm.invoke(state["requirements_messages"])
    print(f"Requirements Agent: {response.content}")
    return {"requirements_messages": [response]}


def should_continue(state: RequirementsState) -> str:
    last_message = state["requirements_messages"][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "no"
    return "yes"
