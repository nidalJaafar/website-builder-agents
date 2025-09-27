import json
import os
from typing import Any, Dict, List, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from website_builder.models.state_models import JsonDecoderState
from website_builder.prompts.json_parser_prompt import json_parser_system_prompt

# Load environment variables
load_dotenv()

# Initialize LLM based on configuration
llm_provider = os.getenv('LLM_PROVIDER', 'deepseek').lower()

if llm_provider == 'lmstudio':
    # LM Studio configuration
    base_url = os.getenv('LM_STUDIO_BASE_URL', 'http://localhost:1234/v1')
    model_name = os.getenv('LM_STUDIO_MODEL', 'local-model')
    
    print(f"Initializing LM Studio at {base_url} with model: {model_name}")
    json_decoder_llm = ChatOpenAI(
        base_url=base_url,
        api_key=SecretStr("not-needed"),  # LM Studio doesn't require a real API key
        model=model_name,
        temperature=0.7
    )
elif llm_provider == 'deepseek':
    # DeepSeek configuration
    # api_key = os.getenv('DEEPSEEK_API_KEY')
    # if not api_key:
        # raise ValueError("DEEPSEEK_API_KEY environment variable is required when using DeepSeek. Please set it in your .env file.")
    
    print("Initializing DeepSeek AI")
    json_decoder_llm = ChatDeepSeek(model="deepseek-chat")
else:
    raise ValueError(f"Unsupported LLM provider: {llm_provider}. Supported providers: 'deepseek', 'lmstudio'")


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
        print("Invalid input. Please provide a JSON string.")
        return state

    try:
        parsed_json = json.loads(user_input)
    except json.JSONDecodeError:
        print("Invalid JSON input. Please provide a valid JSON description.")
        return state

    # Prepare prompt for LLM using the system prompt
    system_prompt = json_parser_system_prompt()
    json_content = json.dumps(parsed_json, indent=2)
    prompt = f"{system_prompt}\n\nJSON:\n{json_content}\nDescription:"
    
    try:
        response = json_decoder_llm.invoke([HumanMessage(content=prompt)])
        print(f"JSON Decoder Agent: {response.content}")
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return state
    return {
        "parsed_text": [response],
        "parsed_input_JSON": parsed_json
    }


def should_continue(state: JsonDecoderState) -> str:
    # Never continue automatically
    return "no"