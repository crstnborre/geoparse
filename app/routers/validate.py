import os
import zipfile
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.conversion import validate_file

router = APIRouter()

@router.post("/")
async def validate(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    if suffix == ".zip":
        extract_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(tmp_path, "r") as zf:
            zf.extractall(extract_dir)
        shp_files = [f for f in os.listdir(extract_dir) if f.endswith(".shp")]
        if not shp_files:
            raise HTTPException(status_code=400, detail="No .shp file found in zip")
        input_path = os.path.join(extract_dir, shp_files[0])
    else:
        input_path = tmp_path

    return validate_file(input_path)
