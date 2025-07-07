from pathlib import Path
import pandas as pd

def load_file(file_path: str) -> tuple[pd.DataFrame,str]:
    """
    Load a file into a pandas DataFrame based on its extension.
    args:
        file_path (str): Path to the file to be loaded.
    returns:
        pd.DataFrame: DataFrame containing the loaded data.
    Raises:
        ValueError: If the file extension is not supported.
        Exception: If there is an error loading the file.
    """

    ext: str = Path(file_path).suffix.lower()

    try:
        match ext:
            case '.csv':
                return pd.read_csv(file_path), ext
            case '.xlsx' | '.xls':
                return pd.read_excel(file_path), ext
            case '.json':
                return pd.read_json(file_path), ext
            case '.parquet':
                return pd.read_parquet(file_path), ext
            case _:
                return pd.DataFrame(),f"Unsupported file extension: {ext}"
    except Exception as e:
        print(f"Error loading file {file_path}: {e}")
        return pd.DataFrame(), ''