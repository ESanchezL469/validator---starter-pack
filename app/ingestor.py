import pandas as pd

def load_csv(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.
    
    :param file_path: Path to the CSV file.
    :return: DataFrame containing the CSV data.
    """
    try:
        df: pd.DataFrame = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error
    
def load_excel(file_path: str) -> pd.DataFrame:
    """
    Load an Excel file into a pandas DataFrame.
    
    :param file_path: Path to the Excel file.
    :return: DataFrame containing the Excel data.
    """
    try:
        df: pd.DataFrame = pd.read_excel(file_path)
        return df
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error