import logging

from website_builder.db.crud import find_session_by_id

logger = logging.getLogger(__name__)

def service_health_check():
    try:
        from website_builder.graphs.orchestrator_graph import build_orchestrator_graph
        return {
            "status": "healthy",
            "orchestrator": "available",
            "version": "1.0.0"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "version": "1.0.0"
        }

def service_poll(session_id: str):
    logger.info(f"Polling session status for {session_id}")
    session = find_session_by_id(session_id)
    response = {
        "status": session.status
    }
    logger.info(f"Polling response: {response}")
    return response
