import os
import zipfile
import tempfile
from osgeo import ogr

VECTOR_DRIVERS = {
    "geojson": "GeoJSON",
    "shapefile": "ESRI Shapefile",
    "kml": "KML",
    "gpkg": "GPKG",
}

VECTOR_EXTENSIONS = {
    "geojson": ".geojson",
    "shapefile": ".shp",
    "kml": ".kml",
    "gpkg": ".gpkg",
}

def convert_vector(input_path: str, output_format: str) -> str:
    driver = ogr.GetDriverByName(VECTOR_DRIVERS[output_format])
    source = ogr.Open(input_path)

    if source is None:
        raise ValueError("Could not open input file")

    output_dir = tempfile.mkdtemp()
    output_path = os.path.join(output_dir, "output" + VECTOR_EXTENSIONS[output_format])

    result = driver.CopuDataSource(source, output_path)
    if result is None:
        raise ValueError("Conversion failed")

    result = None
    source = None

    if output_format == "shapefile":
        zip_path = os.path.join(output_dir, "output.zip")
        with zipfile.ZipFile(zip_path, "w") as zf:
            for f in os.listdir(output_dir):
                if f.startswith("output") and not f.endswith(".zip"):
                    zf.write(os.path.join(output_dir, f), f)
        return zip_path

    return output_path


