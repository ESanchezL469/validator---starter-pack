import os
import hashlib
import pandas as pd
from datetime import datetime

from app.config import DATASETS_DIR
from app.core.logger import logger

def calculate_hash(df) -> str:
    """
    Calculate the SHA-256 hash of the DataFrame's raw bytes.
    This is used to check if the DataFrame has changed.
    
    Args:
        df (pandas.DataFrame): The DataFrame to hash.
    Returns:
        str: The SHA-256 hash of the DataFrame's raw bytes.
    """
    try:
        raw_bytes = df.to_csv(index=False).encode('utf-8')
        return hashlib.sha256(raw_bytes).hexdigest()
    except Exception as e:
        logger.exception(f'Error calculating hash: {str(e)}')
        return None

def save_dataframe(df: pd.DataFrame, format: str = 'csv') -> tuple[str, str]:
    """
    Save the DataFrame to a CSV file and return the file path.
    """
    try:
        version: str = calculate_hash(df)
        if version is None:
            raise ValueError("Failed to calculate hash for the DataFrame.")
        timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")

        file_path: str = os.path.join(DATASETS_DIR, f"{version}_data.{format}")
        if format == 'csv':
            df.to_csv(file_path, index=False)
        elif format == 'parquet':
            df.to_parquet(file_path,index=False)

        return version, timestamp
    except Exception as e:
        logger.exception(f'Error saving DataFrame: {str(e)}')
        return None, None