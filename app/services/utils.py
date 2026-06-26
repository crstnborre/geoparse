import os
import shutil
import zipfile
import tempfile


def extract_zip(zip_path: str) -> str:
    extract_dir = tempfile.mkdtemp()
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_dir)

    for ext in (".shp", ".kml"):
        matches = [f for f in os.listdir(extract_dir) if f.lower().endswith(ext)]
        if matches:
            return os.path.join(extract_dir, matches[0])

    raise ValueError("Zip must contain a .shp or .kml file")


def cleanup(*paths: str) -> None:
    for path in paths:
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            elif os.path.isfile(path):
                os.remove(path)
        except Exception:
            pass
