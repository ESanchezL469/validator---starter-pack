import json
import os
from typing import List

METADATA_DIR = 'metadata'
os.makedirs(METADATA_DIR, exist_ok=True)

def save_metadata(version: str, timestamp: str, columns: List[str], total_rows: int, 
                  is_valid: bool, errors: dict) -> None:
    """
    Save metadata to a JSON file.
    
    Args:
        version (str): The version of the dataset.
        timestamp (str): The timestamp when the dataset was processed.
        total_rows (int): The total number of rows in the dataset.
        is_valid (bool): Whether the dataset is valid or not.
        errors (dict): A dictionary containing validation errors, if any.
    
    Returns:
        str: The path to the saved metadata file.
    """
    metadata_path = os.path.join(METADATA_DIR, f"{version}_metadata.json")
    
    metadata = {
        "version": version,
        "timestamp": timestamp,
        "columns": columns,
        "total_rows": total_rows,
        "is_valid": is_valid,
        "errors": errors
    }

    with open(metadata_path, 'w', encoding='utf-8') as metadata_file:
        json.dump(metadata, metadata_file, indent=4)