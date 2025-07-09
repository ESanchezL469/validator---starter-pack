import os
from datetime import datetime

from pandas import DataFrame

from app.config import REPORTS_DIR


def generate_report(
    version: str,
    is_valid: bool,
    errors: list[dict],
    timestamp: str,
    df: DataFrame = None,
) -> None:
    report_path: str = os.path.join(REPORTS_DIR, f"{version}_report.txt")
    total_rows: int = len(df) if df is not None else 0

    with open(report_path, "w", encoding="utf-8") as report_file:
        report_file.write(f"Version: {version}\n")
        report_file.write(f"Generated: {datetime.now().isoformat()}\n")
        report_file.write(f"Timestamp: {timestamp}\n")
        report_file.write(f"Total Rows: {total_rows}\n")

        if not is_valid and errors:
            total_issues = sum(error.get("invalid_count", 0) for error in errors)
            report_file.write(f"Total Issues: {total_issues}\n")

            for err in errors:
                column = err.get("column", "Unknown column")
                rule = err.get("rule", "Unknown rule")
                description = err.get("description", "")
                count = err.get("invalid_count", 0)
                samples = err.get("sample_invalid_values", [])

                report_file.write(f"\nColumn: {column}")
                report_file.write(f"\n - Rule Violated: {rule}")
                report_file.write(f"\n - Description: {description}")
                report_file.write(f"\n - Invalid Count: {count}")
                report_file.write(f"\n - Sample Invalid Values: {samples}\n")
        else:
            report_file.write("\nDataFrame is valid.\n")
            report_file.write("Consider running statistical analysis.\n")
            if df is not None and not df.empty:
                report_file.write("Basic statistics:\n")
                report_file.write(f"{df.describe().to_string()}\n")
