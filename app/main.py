import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routers import convert, validate, reproject

app = FastAPI(
    title="geoparse",
    description=(
        "Open source REST API for processing geospatial files.\n\n"
        "**Supported vector formats:** GeoJSON, Shapefile (.zip), KML, GeoPackage\n\n"
        "**Supported raster formats:** GeoTIFF, JPEG2000\n\n"
        "No authentication required. All endpoints accept `multipart/form-data`."
    ),
    version="0.1.0",
)

MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE_MB", "100")) * 1024 * 1024

@app.middleware("http")
async def limit_upload_size(request: Request, call_next):
    if request.method == "POST":
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > MAX_FILE_SIZE:
            return JSONResponse(
                status_code=413,
                content={"detail": f"File too large. Maximum allowed size is {MAX_FILE_SIZE // (1024 * 1024)}MB."},
            )
    return await call_next(request)

app.include_router(convert.router, prefix="/convert", tags=["convert"])
app.include_router(validate.router, prefix="/validate", tags=["validate"])
app.include_router(reproject.router, prefix="/reproject", tags=["reproject"])

@app.get("/health")
def health():
    return {"status": "ok"}
