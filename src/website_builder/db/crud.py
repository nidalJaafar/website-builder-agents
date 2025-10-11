import json
from typing import Dict, Any
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

from website_builder.db.database import Db_session
from website_builder.db.database_models import Session


def serialize_message(msg):
    """Convert a LangChain message to a JSON-serializable dict"""
    if isinstance(msg, BaseMessage):
        return {
            "type": msg.__class__.__name__,
            "content": msg.content,
        }
    return msg


def deserialize_message(msg_dict):
    """Convert a dict back to a LangChain message"""
    if isinstance(msg_dict, dict) and "type" in msg_dict:
        msg_type = msg_dict["type"]
        content = msg_dict["content"]

        if msg_type == "SystemMessage":
            return SystemMessage(content=content)
        elif msg_type == "HumanMessage":
            return HumanMessage(content=content)
        elif msg_type == "AIMessage":
            return AIMessage(content=content)

    return msg_dict


def serialize_state(state: Dict[str, Any]) -> str:
    """Serialize state with LangChain messages to JSON"""
    serialized = {}
    for key, value in state.items():
        if isinstance(value, list):
            # Handle list of messages
            serialized[key] = [serialize_message(item) for item in value]
        elif isinstance(value, BaseMessage):
            # Handle single message
            serialized[key] = serialize_message(value)
        else:
            serialized[key] = value

    return json.dumps(serialized)

def serialize_list(list_messages: list[BaseMessage]) -> str:
    return json.dumps([serialize_message(message) for message in list_messages])


def summarize_content_with_llm(content: str, content_type: str) -> str:
    """Summarize content using LLM when it becomes too long"""
    # Initialize LLM for summarization
    summarization_llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro")
    
    # Create summarization prompt
    prompt = f"""
Please provide a concise summary of the following {content_type} content. The content correspond to an AI website creator, was used to generate the website and may include technical details, user requirements, and task management information. Focus on preserving the key information and important details:

{content}

Summary:
"""
    
    try:
        response = summarization_llm.invoke([HumanMessage(content=prompt)])
        return response.content
    except Exception as e:
        # If summarization fails, truncate the content as fallback
        return f"[SUMMARIZATION_ERROR: {str(e)}]\n\n{content[-1000:]}"


def should_summarize_content(content: str, max_length: int = 5000) -> bool:
    """Check if content needs summarization based on length"""
    return len(content) > max_length


def deserialize_state(state_json: str) -> Dict[str, Any]:
    """Deserialize JSON back to state with LangChain messages"""
    state = json.loads(state_json)
    deserialized = {}

    for key, value in state.items():
        if key == "requirements_messages" and isinstance(value, list):
            # Handle list of messages
            deserialized[key] = [deserialize_message(item) for item in value]
        else:
            deserialized[key] = value

    return deserialized


def initialize_session() -> Session:
    with Db_session() as db:
        session = Session()
        db.add(session)
        db.commit()
        db.refresh(session)
        return session


def find_session_by_id(session_id: str) -> Session:
    with Db_session() as db:
        session = db.query(Session).filter(Session.id == session_id).first()
        if not session:
            raise ValueError("session not found")
        return session


def add_requirements_gatherer_output(session_id: str, requirements_gatherer_output: Any) -> Session:
    with Db_session() as db:
        session = db.query(Session).filter(Session.id == session_id).first()
        if not session:
            raise ValueError("session not found")
        
        new_content = serialize_list(requirements_gatherer_output)
        
        if session.requirement_gatherer_output is not None:
            # Check if existing content needs summarization
            if should_summarize_content(session.requirement_gatherer_output):
                summarized_existing = summarize_content_with_llm(
                    session.requirement_gatherer_output, 
                    "requirements gatherer"
                )
                session.requirement_gatherer_output = f"[SUMMARIZED PREVIOUS CONTENT]\n{summarized_existing}\n\n[NEW CONTENT]\n{new_content}"
            else:
                session.requirement_gatherer_output = session.requirement_gatherer_output + "\n\n\n\n\n\n" + new_content
        else:
            session.requirement_gatherer_output = new_content
            
        db.commit()
        db.refresh(session)
        return session


def add_task_manager_output(session_id: str, task_manager_output: Any) -> Session:
    with Db_session() as db:
        session = db.query(Session).filter(Session.id == session_id).first()
        if not session:
            raise ValueError("session not found")
        
        new_content = serialize_list(task_manager_output)
        
        if session.task_manager_output is not None:
            # Check if existing content needs summarization
            if should_summarize_content(session.task_manager_output):
                summarized_existing = summarize_content_with_llm(
                    session.task_manager_output, 
                    "task manager"
                )
                session.task_manager_output = f"[SUMMARIZED PREVIOUS CONTENT]\n{summarized_existing}\n\n[NEW CONTENT]\n{new_content}"
            else:
                session.task_manager_output = session.task_manager_output + "\n\n\n\n\n\n" + new_content
        else:
            session.task_manager_output = new_content
            
        db.commit()
        db.refresh(session)
        return session


def update_session_state(session_id: str, state: Dict[str, Any]) -> Session:
    """Update session state by session ID"""
    with Db_session() as db:
        session = db.query(Session).filter(Session.id == session_id).first()
        if not session:
            raise ValueError("session not found")

        # Serialize state with message conversion
        session.state = serialize_state(state)
        db.commit()
        db.refresh(session)
        return session

def complete_session(session_id: str) -> Session:
    with Db_session() as db:
        session = db.query(Session).filter(Session.id == session_id).first()
        if not session:
            raise ValueError("session not found")

        session.status = "complete"
        db.commit()
        db.refresh(session)
        return session


def summarize_session_outputs(session_id: str) -> Session:
    """Manually trigger summarization of existing session outputs"""
    with Db_session() as db:
        session = db.query(Session).filter(Session.id == session_id).first()
        if not session:
            raise ValueError("session not found")
        
        # Summarize requirements gatherer output if it exists and is long
        if session.requirement_gatherer_output and should_summarize_content(session.requirement_gatherer_output):
            session.requirement_gatherer_output = summarize_content_with_llm(
                session.requirement_gatherer_output, 
                "requirements gatherer"
            )
        
        # Summarize task manager output if it exists and is long
        if session.task_manager_output and should_summarize_content(session.task_manager_output):
            session.task_manager_output = summarize_content_with_llm(
                session.task_manager_output, 
                "task manager"
            )
        
        db.commit()
        db.refresh(session)
        return session