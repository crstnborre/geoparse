# geoparse

Open source REST API for converting, validating and reprojecting geospatial files. No authentication required.

## Supported Formats

| Format | Input | Output |
|---|---|---|
| GeoJSON | ✓ | ✓ |
| Shapefile (.zip) | ✓ | ✓ |
| KML / KMZ | ✓ | ✓ |
| GeoPackage (.gpkg) | ✓ | ✓ |
| GeoTIFF | ✓ | ✓ |
| JPEG2000 | ✓ | ✓ |

## Tech Stack

- FastAPI
- GDAL
- Docker

## Local Setup

```bash
git clone https://github.com/crstnborre/geoparse.git
cd geoparse
docker compose up --build
```

API available at `http://localhost:8000`
Interactive docs at `http://localhost:8000/docs`

## Endpoints

### Convert vector file
```
POST /convert/vector
```
| Field | Type | Description |
|---|---|---|
| `file` | file | GeoJSON, Shapefile (.zip), KML or GeoPackage |
| `output_format` | string | `geojson`, `shapefile`, `kml`, `gpkg` |

```bash
curl -X POST http://localhost:8000/convert/vector \
  -F "file=@input.geojson" \
  -F "output_format=shapefile" \
  -o output.zip
```

---

### Convert raster file
```
POST /convert/raster
```
| Field | Type | Description |
|---|---|---|
| `file` | file | GeoTIFF or JPEG2000 |
| `output_format` | string | `geotiff`, `jpeg2000` |

```bash
curl -X POST http://localhost:8000/convert/raster \
  -F "file=@input.tif" \
  -F "output_format=jpeg2000" \
  -o output.jp2
```

---

### Validate file
```
POST /validate/
```
| Field | Type | Description |
|---|---|---|
| `file` | file | Any supported format |

```bash
curl -X POST http://localhost:8000/validate/ \
  -F "file=@input.geojson"
```

Response:
```json
{"valid": true, "type": "vector", "layers": 1, "features": 42, "crs": "4326"}
```

---

### Reproject file
```
POST /reproject/
```
| Field | Type | Description |
|---|---|---|
| `file` | file | Any supported format |
| `target_epsg` | integer | Target CRS EPSG code |

```bash
curl -X POST http://localhost:8000/reproject/ \
  -F "file=@input.geojson" \
  -F "target_epsg=3857" \
  -o reprojected.geojson
```

Common EPSG codes: `4326` (WGS84), `3857` (Web Mercator), `9377` (MAGNA-SIRGAS Colombia)

## License

MIT
