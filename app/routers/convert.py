import os
import zipfile
import tempfile
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.conversion import convert_vector, VECTOR_DRIVERS
from fastapi.responses import FileResponse

router = APIRouter()

@router.post("/vector")
async def vector_conversion(
        file: UploadFile = File(...),
        output_format: str = Form(...),
):
    if output_format not in VECTOR_DRIVERS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported format. Choose from: {', '.join(VECTOR_DRIVERS.keys())}",
        )

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
        input_path=tmp_path

    try:
        output_path = convert_vector(input_path, output_format)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    ext = "zip" if output_format == "shapefile" else output_format
    return FileResponse(output_path, filename=f"converted.{ext}")
