import os
import pandas as pd
from datetime import datetime

REPORTS_DIR = 'reports'
os.makedirs(REPORTS_DIR, exist_ok=True)

def generate_report(version: str, is_valid: bool, errors: any, total_rows: int, 
                    timestamp: str, df: pd.DataFrame) -> None:
    report_path = os.path.join(REPORTS_DIR, f"{version}_report.txt")

    with open(report_path, 'w', encoding='utf-8') as report_file:
        report_file.write(f"Version: {version}\n")
        report_file.write(f"Generated: {datetime.now().isoformat()}\n")
        report_file.write(f"Version: {version}\n")
        report_file.write(f"Timestamp: {timestamp}\n")
        report_file.write(f"Total Rows: {total_rows}\n")

        if not is_valid:
            total_issues = sum(len(err) for err in errors.values())
            report_file.write(f"Total Issues: {total_issues}\n")

            for column, issues in errors.items():
                report_file.write(f"\nColumn: {column}\n")
                for issue in issues:
                    report_file.write(f"  - {issue['failure_case']} (Check: {issue['check']})\n")
        else:
            report_file.write("DataFrame is valid.\n")
            report_file.write("Consider running statistical analysis on the data.\n")
            if df is not None:
                report_file.write(f"Basic statistics:\n")
                report_file.write(f"{df.describe().to_string()}\n")