from fastapi import FastAPI
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

app.include_router(convert.router, prefix="/convert", tags=["convert"])
app.include_router(validate.router, prefix="/validate", tags=["validate"])
app.include_router(reproject.router, prefix="/reproject", tags=["reproject"])


@app.get("/health")
def health():
    return {"status": "ok"}
