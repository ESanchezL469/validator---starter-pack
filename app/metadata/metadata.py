import json
import os
from typing import Any

from app.config import METADATA_DIR


def save_metadata(val: Any) -> None:
    """
    Save metadata to a JSON file.

    Args:
        version (str): The version of the dataset.
        timestamp (str): The timestamp when the dataset was processed.
        total_rows (int): The total number of rows in the dataset.
        is_valid (bool): Whether the dataset is valid or not.
        errors (dict): A dictionary containing validation errors, if any.
        source_file (str, optional): The source file path, if applicable.
        replaces (str, optional): The replaced file path, if applicable.

    Returns:
        str: The path to the saved metadata file.
    """
    metadata_path = os.path.join(METADATA_DIR, f"{val.version}_metadata.json")

    metadata = {
        "version": val.version,
        "timestamp": val.timestamp,
        "columns": val.data.columns.tolist(),
        "total_rows": len(val.data),
        "is_valid": val.is_valid,
        "source_file": val.path,
        "replaces": val.previous,
        "errors": val.error,
    }

    with open(metadata_path, "w", encoding="utf-8") as metadata_file:
        json.dump(metadata, metadata_file, indent=4)
