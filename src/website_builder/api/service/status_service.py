from website_builder.db.crud import find_session_by_id

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
    session = find_session_by_id(session_id)
    return {
        "status": session.status
    }
