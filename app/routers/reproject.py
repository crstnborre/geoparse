import os
import tempfile
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from app.services.reprojection import reproject
from app.services.utils import cleanup, extract_zip

router = APIRouter()

@router.post(
    "/",
    summary="Reproject geospatial file",
    description=(
        "Reproject a geospatial file to a different coordinate reference system.\n\n"
        "**Accepted input formats:** GeoJSON, Shapefile (.zip), KML, GeoPackage, GeoTIFF, JPEG2000\n\n"
        "**target_epsg:** EPSG code of the target CRS (e.g. `4326` for WGS84, `3857` for Web Mercator, "
        "`9377` for MAGNA-SIRGAS Colombia)\n\n"
        "Vector files are returned as GeoJSON. Raster files are returned as GeoTIFF."
    ),
)
async def reproject_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    target_epsg: int = Form(...),
):
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

    try:
        output_path = reproject(input_path, target_epsg)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    ext = os.path.splitext(output_path)[1].lstrip(".")
    background_tasks.add_task(cleanup, tmp_path, os.path.dirname(output_path))
    return FileResponse(output_path, filename=f"reprojected.{ext}")
