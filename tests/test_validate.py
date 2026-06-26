def test_validate_vector(client, geojson_file):
    with open(geojson_file, "rb") as f:
        response = client.post("/validate/", files={"file": ("test.geojson", f, "application/json")})
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert data["type"] == "vector"
    assert data["features"] == 1


def test_validate_raster(client, geotiff_file):
    with open(geotiff_file, "rb") as f:
        response = client.post("/validate/", files={"file": ("test.tif", f, "image/tiff")})
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert data["type"] == "raster"
    assert data["bands"] == 1


def test_validate_invalid_file(client):
    response = client.post("/validate/", files={"file": ("bad.txt", b"not a geo file", "text/plain")})
    assert response.status_code == 200
    assert response.json()["valid"] is False
