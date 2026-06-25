import os
import zipfile
import tempfile
from osgeo import ogr, gdal, osr

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

def validate_file(input_path: str) -> dict:
    # intenta abrir como vector
    vector = ogr.Open(input_path)
    if vector is not None:
        layer = vector.GetLayer(0)
        crs = layer.GetSpatialRef()
        info = {
            "valid": True,
            "type": "vector",
            "layers": vector.GetLayerCount(),
            "features": layer.GetFeatureCount(),
            "crs": crs.GetAuthorityCode(None) if crs else None,
        }
        vector = None
        return info

    # intenta abrir como raster
    raster = gdal.Open(input_path)
    if raster is not None:
        crs = osr.SpatialReference()
        crs.ImportFromWkt(raster.GetProjection())
        info = {
            "valid": True,
            "type": "raster",
            "bands": raster.RasterCount,
            "width": raster.RasterXSize,
            "height": raster.RasterYSize,
            "crs": crs.GetAuthorityCode(None) if raster.GetProjection() else None,
        }
        raster = None
        return info

    return {"valid": False}

def reproject(input_path: str, target_epsg: int) -> str:
    target_srs = osr.SpatialReference()
    target_srs.ImportFromEPSG(target_epsg)

    # intenta como vector
    source = ogr.Open(input_path)
    if source is not None:
        output_dir = tempfile.mkdtemp()
        output_path = os.path.join(output_dir, "reprojected.geojson")
        driver = ogr.GetDriverByName("GeoJSON")
        out_ds = driver.CreateDataSource(output_path)

        for i in range(source.GetLayerCount()):
            in_layer = source.GetLayer(i)
            source_srs = in_layer.GetSpatialRef()
            transform = osr.CoordinateTransformation(source_srs, target_srs)
            out_layer = out_ds.CreateLayer(in_layer.GetName(), target_srs)

            in_defn = in_layer.GetLayerDefn()
            for j in range(in_defn.GetFieldCount()):
                out_layer.CreateField(in_defn.GetFieldDefn(j))

            for feature in in_layer:
                geom = feature.GetGeometryRef()
                if geom is None:
                    continue
                geom = geom.Clone()
                geom.Transform(transform)
                feature.SetGeometry(geom)
                out_layer.CreateFeature(feature)

        out_ds = None
        source = None
        return output_path

    # intenta como raster
    raster = gdal.Open(input_path)
    if raster is not None:
        output_dir = tempfile.mkdtemp()
        output_path = os.path.join(output_dir, "reprojected.tif")
        gdal.Warp(output_path, raster, dstSRS=f"EPSG:{target_epsg}")
        raster = None
        return output_path

    raise ValueError("Could not open input file")
