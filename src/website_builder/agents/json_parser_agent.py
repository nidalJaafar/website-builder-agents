import json
import logging

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from website_builder.models.state_models import JsonDecoderState
from website_builder.prompts.json_parser_prompt import json_parser_system_prompt

logger = logging.getLogger(__name__)
load_dotenv()

json_decoder_llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro")


def user_message(state: JsonDecoderState) -> JsonDecoderState:
    if not any(isinstance(msg, HumanMessage) for msg in state.get("parsed_text", [])):
        input_text = "Hi, this is a JSON parser service. Send your JSON to be converted to natural language.\nUser: "
    else:
        input_text = "User: "

    message = HumanMessage(content=input(input_text))
    return {
        "parsed_text": [message],
        "parsed_input_JSON": state.get("parsed_input_JSON", {})
    }


def send_message(state: JsonDecoderState) -> JsonDecoderState:
    last_message = state["parsed_text"][-1]
    user_input = last_message.content

    # Ensure user_input is a string
    if not isinstance(user_input, str):
        logger.warn("Invalid input. Please provide a JSON string.")
        return state

    try:
        parsed_json = json.loads(user_input)
    except json.JSONDecodeError:
        logger.error("Invalid JSON input. Please provide a valid JSON description.")
        return state

    # Prepare prompt for LLM using the system prompt
    system_prompt = json_parser_system_prompt()
    json_content = json.dumps(parsed_json, indent=2)
    prompt = f"{system_prompt}\n\nJSON:\n{json_content}\nDescription:"

    try:
        response = json_decoder_llm.invoke([HumanMessage(content=prompt)])
        logger.info(f"JSON Decoder Agent: {response.content}")
    except Exception as e:
        logger.error(f"Error calling LLM: {e}")
        return state
    return {
        "parsed_text": [response],
        "parsed_input_JSON": parsed_json
    }


def should_continue(state: JsonDecoderState) -> str:
    # Never continue automatically
    return "no"
