from fastapi import FastAPI, HTTPException
from typing import Dict, Any
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from website_builder.agents.json_parser_agent import json_decoder_llm, send_message
from website_builder.models.state_models import JsonDecoderState
from langchain_core.messages import HumanMessage

app = FastAPI(
    title="JSON to Natural Language Parser API",
    description="Convert JSON structures into clear, natural language descriptions",
    version="1.0.0"
)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "JSON to Natural Language Parser API",
        "version": "1.0.0",
        "endpoints": {
            "/parse": "POST - Convert JSON to natural language",
            "/health": "GET - Health check",
            "/docs": "GET - API documentation"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "llm_initialized": json_decoder_llm is not None}

@app.post("/parse")
async def parse_json(json_data: Dict[str, Any]):
    """
    Convert JSON data to natural language description
    
    Send your JSON directly - no wrapper needed!
    
    Example:
    {
        "website": {
            "title": "My Portfolio",
            "theme": "dark",
            "navigation": ["Home", "About", "Projects"]
        }
    }
    """
    try:
        print(f"[DEBUG] Received JSON: {json_data}")
        
        # Convert to string
        json_string = json.dumps(json_data, indent=2)
        print(f"[DEBUG] Processing: {json_string[:200]}...")
        
        # Create initial state
        initial_state = JsonDecoderState(
            parsed_input_JSON={},
            parsed_text=[HumanMessage(content=json_string)]
        )
        
        # Process the JSON
        result_state = send_message(initial_state)
        
        # Return the description
        if result_state["parsed_text"] and len(result_state["parsed_text"]) > 0:
            last_message = result_state["parsed_text"][-1]
            # Ensure we get a string description
            if hasattr(last_message, 'content'):
                description = str(last_message.content) if last_message.content is not None else "No content generated"
            else:
                description = str(last_message)
            return {"description": description}
        else:
            raise HTTPException(status_code=500, detail="No response generated from LLM")
            
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON decode error: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid JSON format: {str(e)}")
    except Exception as e:
        print(f"[ERROR] Processing error: {e}")
        print(f"[ERROR] Error type: {type(e).__name__}")
        import traceback
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
    
def main():
    import uvicorn
    uvicorn.run("website_builder.api.json_api:app", host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()
