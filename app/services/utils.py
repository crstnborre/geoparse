import os
import shutil

def cleanup(*paths: str) -> None:
    for path in paths:
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            elif os.path.isfile(path):
                os.remove(path)
        except Exception:
            pass
