import json


def test_reproject_vector(client, geojson_file):
    with open(geojson_file, "rb") as f:
        response = client.post(
            "/reproject/",
            data={"target_epsg": 3857},
            files={"file": ("test.geojson", f, "application/json")},
        )
    assert response.status_code == 200
    data = json.loads(response.content)
    assert data["type"] == "FeatureCollection"


def test_reproject_raster(client, geotiff_file):
    with open(geotiff_file, "rb") as f:
        response = client.post(
            "/reproject/",
            data={"target_epsg": 3857},
            files={"file": ("test.tif", f, "image/tiff")},
        )
    assert response.status_code == 200
