import os
import zipfile
import tempfile
from osgeo import ogr, gdal

gdal.UseExceptions()
ogr.UseExceptions()

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

RASTER_DRIVERS = {
    "geotiff": "GTiff",
    "jpeg2000": "JP2OpenJPEG",
}

RASTER_EXTENSIONS = {
    "geotiff": ".tif",
    "jpeg2000": ".jp2",
}

def convert_vector(input_path: str, output_format: str) -> str:
    driver = ogr.GetDriverByName(VECTOR_DRIVERS[output_format])
    source = ogr.Open(input_path)

    if source is None:
        raise ValueError("Could not open input file")

    output_dir = tempfile.mkdtemp()
    output_path = os.path.join(output_dir, "output" + VECTOR_EXTENSIONS[output_format])

    result = driver.CopyDataSource(source, output_path)
    if result is None:
        raise ValueError("Conversion failed")

    result = None
    source = None

    if output_format == "shapefile":
        zip_path = os.path.join(output_dir, "output.zip")
        with zipfile.ZipFile(zip_path, "w") as zf:
            for f in os.listdir(output_dir):
                if not f.endswith(".zip"):
                    zf.write(os.path.join(output_dir, f), f)
        return zip_path

    return output_path

def convert_raster(input_path: str, output_format: str) -> str:
    driver = gdal.GetDriverByName(RASTER_DRIVERS[output_format])
    source = gdal.Open(input_path)

    if source is None:
        raise ValueError("Could not open input file")

    output_dir = tempfile.mkdtemp()
    output_path = os.path.join(output_dir, "output" + RASTER_EXTENSIONS[output_format])

    result = driver.CreateCopy(output_path, source)
    if result is None:
        raise ValueError("Conversion failed")

    result = None
    source = None

    return output_path
