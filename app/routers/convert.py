import os
import zipfile
import tempfile
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.conversion import convert_vector, convert_raster, VECTOR_DRIVERS, RASTER_DRIVERS, RASTER_EXTENSIONS
from fastapi.responses import FileResponse

router = APIRouter()

@router.post(
    "/vector",
    summary="Convert vector file",
    description=(
        "Convert a vector geospatial file between formats.\n\n"
        "**Accepted input formats:** GeoJSON, Shapefile (.zip), KML, GeoPackage\n\n"
        "**output_format values:** `geojson`, `shapefile`, `kml`, `gpkg`\n\n"
        "Shapefile output is returned as a `.zip` containing all required component files."
    ),
)
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

@router.post(
    "/raster",
    summary="Convert raster file",
    description=(
        "Convert a raster geospatial file between formats.\n\n"
        "**Accepted input formats:** GeoTIFF, JPEG2000\n\n"
        "**output_format values:** `geotiff`, `jpeg2000`"
    ),
)
async def raster_conversion(
    file: UploadFile = File(...),
    output_format: str = Form(...),
):
    if output_format not in RASTER_DRIVERS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported format. Choose from: {', '.join(RASTER_DRIVERS.keys())}",
        )

    suffix = os.path.splitext(file.filename)[1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        output_path = convert_raster(tmp_path, output_format)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    ext = RASTER_EXTENSIONS[output_format].lstrip(".")
    return FileResponse(output_path, filename=f"converted.{ext}")
