import json
import logging
from typing import Dict, Any

from fastapi import HTTPException
from langchain_core.messages import HumanMessage

from website_builder.agents.json_parser_agent import send_message
from website_builder.models.state_models import JsonDecoderState

logger = logging.getLogger(__name__)


def service_parse_json(json_data: Dict[str, Any]):
    logger.info(f"JSON Data to be parsed: {json_data}")
    try:
        logger.info(f"Received JSON: {json_data}")
        json_string = json.dumps(json_data, indent=2)
        logger.info(f"Processing: {json_string}...")
        initial_state = JsonDecoderState(
            parsed_input_JSON={},
            parsed_text=[HumanMessage(content=json_string)]
        )
        result_state = send_message(initial_state)

        if result_state["parsed_text"] and len(result_state["parsed_text"]) > 0:
            last_message = result_state["parsed_text"][-1]
            if hasattr(last_message, 'content'):
                description = str(last_message.content) if last_message.content is not None else "No content generated"
            else:
                description = str(last_message)
            response =  {"description": description}
            logger.info(f"Response: {response}")
        else:
            logger.error("Error generating description")
            raise HTTPException(status_code=500, detail="No response generated from LLM")

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid JSON format: {str(e)}")
    except Exception as e:
        logger.error(f"Processing error: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
