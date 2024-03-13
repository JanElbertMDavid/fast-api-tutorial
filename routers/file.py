import uuid
from fastapi import APIRouter, File, UploadFile
import shutil
from fastapi.responses import FileResponse

router = APIRouter(prefix="/file", tags=["file"])

# Store file in memory
@router.post("/file")
def get_file(file: bytes = File(...)):
    content = file.decode("utf-8")
    lines = content.split("\n")
    return {"lines": lines}

# Make file upload and write on disk
@router.post("/uploadfile")
def get_upload_file(upload_file: UploadFile = File(...)):
    file_extension = upload_file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_extension}"
    path = f"files/{filename}"
    with open(path, "w+b") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return {"filename": path, "type": upload_file.content_type}

@router.get('/download/{name}', response_class=FileResponse)
def download_file(name: str):
    path = f'files/{name}'
    return path
