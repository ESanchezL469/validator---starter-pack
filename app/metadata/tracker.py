import os

from app.config import METADATA_DIR


def version_exists(version: str) -> bool:
    """
    Check if a version already exists in the metadata file.
    """
    file_path = os.path.join(METADATA_DIR, f"""{version}_metadata.json""")
    return os.path.exists(file_path)


def find_previous_version(version: str) -> str:
    """
    Find the previous version of the dataset.
    """
    files = os.listdir(METADATA_DIR)
    for file in files:
        if file.startswith(version) and file.endswith("_metadata.json"):
            return file
    return ""
