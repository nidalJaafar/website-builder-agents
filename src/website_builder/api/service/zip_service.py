import io
import os
import zipfile

from fastapi import HTTPException, Response

from website_builder.db.crud import find_session_by_id


def service_zip_folder(session_id: str):
    session = find_session_by_id(session_id)
    if session.status != "complete":
        raise HTTPException(detail="Session is not completed", status_code=400)
    zip_buffer = io.BytesIO()
    try:
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for dirname, subdir, files in os.walk("./website_project"):
                zf.write(dirname)
                for filename in files:
                    zf.write(os.path.join(dirname, filename))
        zip_buffer.seek(0)
        return Response(zip_buffer.getvalue(),
                        headers={"Content-Disposition": f"attachment; filename={session_id}.zip"},
                        media_type="application/zip")
    except:
        raise HTTPException(detail="Error in processing data", status_code=500)
    finally:
        zip_buffer.close()
