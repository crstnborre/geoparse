import os
import pytest
import tempfile
from osgeo import ogr, gdal, osr
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def geojson_file():
    with tempfile.NamedTemporaryFile(suffix=".geojson", delete=False, mode="w") as f:
        f.write('{"type":"FeatureCollection","features":[{"type":"Feature","geometry":{"type":"Point","coordinates":[-74.0,4.6]},"properties":{"name":"Bogota"}}]}')
        path = f.name
    yield path
    os.remove(path)


@pytest.fixture
def geotiff_file():
    path = tempfile.mktemp(suffix=".tif")
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    driver = gdal.GetDriverByName("GTiff")
    ds = driver.Create(path, 10, 10, 1, gdal.GDT_Byte)
    ds.SetGeoTransform([-74.0, 0.01, 0, 4.6, 0, -0.01])
    ds.SetProjection(srs.ExportToWkt())
    ds.GetRasterBand(1).Fill(128)
    ds = None
    yield path
    os.remove(path)
