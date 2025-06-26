import os
import hashlib
from datetime import datetime

DATASETS_DIR = 'datasets'
os.makedirs(DATASETS_DIR, exist_ok=True)

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
        print(f"Error calculating hash: {e}")
        return None
    
def save_dataframe(df, filename: str) -> tuple[str, str]:
    """
    Save the DataFrame to a CSV file and return the file path.
    """
    try:
        version: str = calculate_hash(df)
        if version is None:
            raise ValueError("Failed to calculate hash for the DataFrame.") 
        timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path: str = os.path.join(DATASETS_DIR, f"{version}_data.csv")
        df.to_csv(file_path, index=False)
        return version, timestamp
    except Exception as e:
        print(f"Error saving DataFrame: {e}")
        return None, None