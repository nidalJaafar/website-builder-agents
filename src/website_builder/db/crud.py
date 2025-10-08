import json
from typing import Dict, Any
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage

from website_builder.db.database import Db_session
from website_builder.db.database_models import Session, File


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
        if session.requirement_gatherer_output is not None:
            session.requirement_gatherer_output = session.requirement_gatherer_output + "\n\n\n\n\n\n" + serialize_list(requirements_gatherer_output)
        else:
            session.requirement_gatherer_output = serialize_list(requirements_gatherer_output)
        db.commit()
        db.refresh(session)
        return session


def add_task_manager_output(session_id: str, task_manager_output: Any) -> Session:
    with Db_session() as db:
        session = db.query(Session).filter(Session.id == session_id).first()
        if not session:
            raise ValueError("session not found")
        if session.task_manager_output is not None:
            session.task_manager_output = session.task_manager_output + "\n\n\n\n\n\n" + serialize_list(task_manager_output)
        else:
            session.task_manager_output = serialize_list(task_manager_output)
        db.commit()
        db.refresh(session)
        return session


def add_file_to_session(session_id: str, file_path: str, content: str) -> Session:
    with Db_session() as db:
        session = db.query(Session).filter(Session.id == session_id).first()
        if not session:
            raise ValueError("session not found")

        file = File(
            file_path=file_path,
            content=content,
            session_id=session_id
        )
        db.add(file)
        db.commit()
        db.refresh(file)
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