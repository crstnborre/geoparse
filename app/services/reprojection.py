import os
import tempfile
from osgeo import ogr, gdal, osr

def reproject(input_path: str, target_epsg: int) -> str:
    target_srs = osr.SpatialReference()
    target_srs.ImportFromEPSG(target_epsg)

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

    raster = gdal.Open(input_path)
    if raster is not None:
        output_dir = tempfile.mkdtemp()
        output_path = os.path.join(output_dir, "reprojected.tif")
        gdal.Warp(output_path, raster, dstSRS=f"EPSG:{target_epsg}")
        raster = None
        return output_path

    raise ValueError("Could not open input file")
