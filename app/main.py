from fastapi import FastAPI
from app.routers import convert, validate, reproject

app = FastAPI(
    title="geoparse",
    description="REST API for converting, validating and reprojecting geospatial files.",
    version="0.1.0",
)

app.include_router(convert.router, prefix="/convert", tags=["convert"])
app.include_router(validate.router, prefix="/validate", tags=["validate"])
app.include_router(reproject.router, prefix="/reproject", tags=["reproject"])


@app.get("/health")
def health():
    return {"status": "ok"}
