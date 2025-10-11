import logging
import sys
from typing import Dict, Any

from dotenv import load_dotenv
from fastapi import FastAPI

from website_builder.api.service.json_service import service_parse_json
from website_builder.api.service.message_service import service_send_chat_message, service_start_requirements_chat
from website_builder.api.service.status_service import service_poll, service_health_check
from website_builder.api.service.zip_service import service_zip_folder
from website_builder.db.database import init_db

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logging.getLogger("langchain_google_genai._function_utils").setLevel(logging.ERROR)
logging.getLogger("grpc._cython.cygrpc").setLevel(logging.INFO)

app = FastAPI(
    title="Website Builder API",
    description="This API endpoint receives user inputs and processes them to build websites using AI agents.",
    version="1.0.0"
)

logger = logging.getLogger(__name__)


@app.get("/health")
async def health_check():
    return service_health_check()


@app.post("/chat/start")
async def start_requirements_chat(user_input: Dict[str, Any]):
    return service_start_requirements_chat(user_input)


@app.post("/chat/message")
async def send_chat_message(message_data: Dict[str, Any]):
    return await service_send_chat_message(message_data)


@app.get("/poll/{session_id}")
def poll(session_id: str):
    return service_poll(session_id)


@app.get("/zip/{session_id}")
def zip_folder(session_id: str):
    return service_zip_folder(session_id)


@app.post("/parse")
async def parse_json(json_data: Dict[str, Any]):
    return service_parse_json(json_data)


def main():
    import uvicorn
    init_db()
    uvicorn.run("website_builder.api.controller.api:app", host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
