from osgeo import ogr, gdal, osr

def validate_file(input_path: str) -> dict:
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
