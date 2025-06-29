import glob
import os
from app.ingestor import load_csv, load_excel
from app.enricher import enrich_dataframe
from app.profiler import generate_profile_report
from app.validator import validate_dataframe
from app.tracker import find_previous_version, version_exists
from app.reporter import generate_report
from app.metadata import save_metadata
from app.storage import save_dataframe
import pandas as pd
import argparse

def get_files_from_directory(directory: str) -> list[str]:
    """
    Returns a list of files in the given directory.
    Filters files to include only those with .csv, .xlsx, or .xls extensions.
    Args:
        directory (str): The directory to search for files.
    Returns:
        list[str]: A list of file paths that match the specified extensions.
    """
    valid_extensions = ('.csv', '.xlsx', '.xls')
    return [f for f in glob.glob(os.path.join(directory, "*")) if f.lower().endswith(valid_extensions)]

def process_file(path: str, enable_profile: bool):
    if not os.path.exists(path):
        print(f"File {path} does not exist.")
        return
    
    try:
        ext = os.path.splitext(path)[1].lower()
        if ext == '.csv':
            df = load_csv(path)
        elif ext in ['.xlsx', '.xls']:
            df = load_excel(path)
        else:
            print(f"Unsupported file format: {ext}")
            return

        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        is_valid, errors = validate_dataframe(df)
        df = enrich_dataframe(df)
        version, timestamp = save_dataframe(df, is_valid, errors)

        if version_exists(version):
            print(f"Version {version} already exists. Please try again with a different file.")
            return

        if enable_profile:
            profile_path = generate_profile_report(df, version)
            print(f"Profile report generated at: {profile_path}")

        generate_report(version, is_valid, errors, len(df), timestamp, df)
        previous = find_previous_version(version)
        save_metadata(version, timestamp, df.columns.tolist(), len(df), is_valid, errors, source_file=os.path.basename(path), replaces=previous)
        print(f"Data processed successfully for file: {path}")
    except Exception as e:
        print(f"An error occurred while processing the file {path}: {e}")
        return

def main():

    parser = argparse.ArgumentParser(description="Data Ingestion and Processing Tool")
    parser.add_argument('--input','-i', type=str, help='Path to the CSV or Excel file')
    parser.add_argument('--input-folder', '-f', type=str, help='Directory to search for files', default='.')
    parser.add_argument('--profile', '-j', action='store_true', help='Enable profile report generation')
    args = parser.parse_args()

    input_path = []

    if args.input_folder:
        if not os.path.isdir(args.input_folder):
            print(f"Directory {args.input_folder} does not exist.")
            return
        input_path = get_files_from_directory(args.input_folder)
        if not input_path:
            print(f"No valid files found in directory {args.input_folder}.")
            return
    elif args.input:
        input_path = args.input
    else:
        input_path = [input("Ingrese ruta del archivo o directorio: ").strip()]

    for path in input_path:
        process_file(path, args.profile)

if __name__ == "__main__":
    main()