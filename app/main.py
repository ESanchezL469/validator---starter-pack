import os
from app.validator import validate_dataframe
from app.reporter import generate_report
from app.storage import save_dataframe
import pandas as pd

def main():

    path = input("Ingrese ruta del archivo CSV: ").strip()

    if not os.path.exists(path):
        print(f"File {path} does not exist.")
        return

    try:
        df = pd.read_csv(path)
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        is_valid, errors = validate_dataframe(df)
        version, timestamp = save_dataframe(df, is_valid, errors)
        generate_report(version, is_valid, errors, len(df), timestamp)
        print(f"Data processed successfully.")
    except Exception as e:
        print(f"An error occurred while processing the file: {e}")
        return

if __name__ == "__main__":
    main()