import io
import os
import zipfile

from fastapi import HTTPException, Response

from website_builder.db.crud import find_session_by_id


def service_zip_folder(session_id: str):
    session = find_session_by_id(session_id)
    if session.status != "complete":
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
        return Response(zip_buffer.getvalue(),
                        headers={"Content-Disposition": f"attachment; filename={session_id}.zip"},
                        media_type="application/zip")
    except Exception as e:
        raise HTTPException(detail=f"Error in processing data: {str(e)}", status_code=500)
    finally:
        zip_buffer.close()
