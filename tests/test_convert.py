def test_convert_vector_to_geojson(client, geojson_file):
    with open(geojson_file, "rb") as f:
        response = client.post(
            "/convert/vector",
            data={"output_format": "geojson"},
            files={"file": ("test.geojson", f, "application/json")},
        )
    assert response.status_code == 200


def test_convert_vector_to_shapefile(client, geojson_file):
    with open(geojson_file, "rb") as f:
        response = client.post(
            "/convert/vector",
            data={"output_format": "shapefile"},
            files={"file": ("test.geojson", f, "application/json")},
        )
    assert response.status_code == 200
    assert "content-disposition" in response.headers
    assert "converted.zip" in response.headers["content-disposition"]


def test_convert_vector_invalid_format(client, geojson_file):
    with open(geojson_file, "rb") as f:
        response = client.post(
            "/convert/vector",
            data={"output_format": "pdf"},
            files={"file": ("test.geojson", f, "application/json")},
        )
    assert response.status_code == 400


def test_convert_raster_to_jpeg2000(client, geotiff_file):
    with open(geotiff_file, "rb") as f:
        response = client.post(
            "/convert/raster",
            data={"output_format": "jpeg2000"},
            files={"file": ("test.tif", f, "image/tiff")},
        )
    assert response.status_code == 200
