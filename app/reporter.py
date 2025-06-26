import os
import json

REPORTS_DIR = 'reports'
METADATA_DIR = 'metadata'

os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(METADATA_DIR, exist_ok=True)

def generate_report(version: str, is_valid: bool, errors: any, total_rows: int, timestamp: str) -> str:
    report_path = os.path.join(REPORTS_DIR, f"{version}_report.json")
    metadata_path = os.path.join(METADATA_DIR, f"{version}_metadata.json")

    with open(report_path, 'w') as report_file:
        report_data = {
            "is_valid": is_valid,
            "errors": errors
        }
        json.dump(report_data, report_file, indent=2)

    with open(metadata_path, 'w') as metadata_file:
        metadata_data = {
            "version": version,
            "timestamp": timestamp,
            "total_rows": total_rows,
            "is_valid": is_valid
        }
        json.dump(metadata_data, metadata_file, indent=2)