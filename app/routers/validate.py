import os
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from app.services.validation import validate_file
from app.services.utils import cleanup, extract_zip

router = APIRouter()

@router.post(
    "/",
    summary="Validate geospatial file",
    description=(
        "Check if a file is a valid geospatial file and return its metadata.\n\n"
        "**Returns for vector:** type, layer count, feature count, CRS (EPSG code)\n\n"
        "**Returns for raster:** type, band count, width, height, CRS (EPSG code)\n\n"
        "Returns `{\"valid\": false}` if the file cannot be recognized."
    ),
)
async def validate(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    if suffix in (".zip", ".kmz"):
        try:
            input_path = extract_zip(tmp_path)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        input_path = tmp_path

    result = validate_file(input_path)
    background_tasks.add_task(cleanup, tmp_path)
    return result
