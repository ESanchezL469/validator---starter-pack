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
    total_rows: int = len(df)

    with open(report_path, "w", encoding="utf-8") as report_file:
        report_file.write(f"Version: {version}\n")
        report_file.write(f"Generated: {datetime.now().isoformat()}\n")
        report_file.write(f"Version: {version}\n")
        report_file.write(f"Timestamp: {timestamp}\n")
        report_file.write(f"Total Rows: {total_rows}\n")

        if not is_valid:
            total_issues = sum(len(err) for err in errors)
            report_file.write(f"Total Issues: {total_issues}")

            for err in errors:
                for column, issues in err.items():
                    report_file.write(f"\nColumn: {column}")
                    for issue in issues:
                        report_file.write(
                            f" - {issue['failure_case']} - {issue['check']}"
                        )

        else:
            report_file.write("DataFrame is valid.")
            report_file.write("Consider running statistical analysis.")
            if not df.empty:
                report_file.write("Basic statistics:\n")
                report_file.write(f"{df.describe().to_string()}\n")
