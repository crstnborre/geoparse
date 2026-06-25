# geoparse

> 🚧 In development

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

## License

MIT
