import io
import logging
import os
import zipfile

from fastapi import HTTPException, Response

from website_builder.db.crud import find_session_by_id

logger = logging.getLogger(__name__)

def service_zip_folder(session_id: str):
    logger.info(f"Zipping generated files for session {session_id}")
    session = find_session_by_id(session_id)
    if session.status != "completed":
        raise HTTPException(detail="Session is not completed", status_code=400)
    
    project_path = f"./website_project/{session_id}"
    
    # Check if the project directory exists
    if not os.path.exists(project_path):
        raise HTTPException(detail="Project directory not found", status_code=404)
    
    zip_buffer = io.BytesIO()
    try:
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    archive_name = os.path.relpath(file_path, project_path)
                    zf.write(file_path, archive_name)
        
        zip_buffer.seek(0)
        response = Response(zip_buffer.getvalue(),
                        headers={"Content-Disposition": f"attachment; filename={session_id}.zip"},
                        media_type="application/zip")
        logger.info(f"Website zipped successfully for session {session_id}")
        return response
    except Exception as e:
        logger.error(f"Error zipping generated files for session {session_id}")
        raise HTTPException(detail=f"Error in processing data: {str(e)}", status_code=500)
    finally:
        zip_buffer.close()
