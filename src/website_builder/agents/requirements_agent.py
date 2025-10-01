from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from website_builder.models.state_models import RequirementsState
from website_builder.tools.validation_tools import exit_tool

requirements_llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro").bind_tools([exit_tool])


def user_message(state: RequirementsState) -> RequirementsState:
    # Check if user_input is provided in state (from API)
    if "user_input" in state and state["user_input"]:
        message = HumanMessage(content=state["user_input"])
        return {"requirements_messages": [message]}
    
    # Interactive mode (CLI)
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


def process_single_message(state: RequirementsState) -> RequirementsState:
    """Process a single message in conversational mode for API"""
    # If there's a user_input in state, add it as a HumanMessage
    if "user_input" in state and state["user_input"]:
        # Add the user message to the conversation
        user_msg = HumanMessage(content=state["user_input"])
        messages = list(state["requirements_messages"]) + [user_msg]
    else:
        # Use existing messages
        messages = state["requirements_messages"]
    
    # Get agent response
    response = requirements_llm.invoke(messages)
    print(f"Requirements Agent: {response.content}")
    
    # Add agent response to messages
    messages.append(response)
    
    return {
        "requirements_messages": messages,
        "requirements_data": ""
    }
