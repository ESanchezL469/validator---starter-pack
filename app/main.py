import os
from app.validator import validate_dataframe
from app.reporter import generate_report
from app.storage import save_dataframe
import pandas as pd

def main():

    path = 'datasets/data.csv'

    if not os.path.exists(path):
        print(f"File {path} does not exist.")
        return

    df = pd.read_csv(path)
    is_valid, errors = validate_dataframe(df)
    version, timestamp = save_dataframe(df,is_valid,errors)
    generate_report(version, is_valid, errors, len(df), timestamp)

if __name__ == "__main__":
    main()
    print("Data processing completed successfully.")
else:
    print("This script is intended to be run as the main module.")
    print("Please run it directly.")
    print("Exiting without processing.")
    exit(1)