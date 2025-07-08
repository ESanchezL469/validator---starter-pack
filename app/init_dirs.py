import os
from app.config import DATASETS_DIR, METADATA_DIR, REPORTS_DIR, PROFILES_DIR

def create_required_directories() -> None:
    for path in [DATASETS_DIR, METADATA_DIR, REPORTS_DIR, PROFILES_DIR]:
        os.makedirs(path, exist_ok=True)