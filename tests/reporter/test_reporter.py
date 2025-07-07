import pandas as pd
from app.reporters.reporter import generate_report

# ----------------------------
# Successful Tests
# ----------------------------

def test_generate_report_success(tmp_path,monkeypatch):

    monkeypatch.setattr('app.reporters.reporter.REPORTS_DIR',str(tmp_path))

    df = pd.DataFrame({"value": [10, 20, 30]})
    version = "v123"
    is_valid = True
    errors = {}
    timestamp = "20240630_120000"

    generate_report(version, is_valid, errors, timestamp, df)

    report_path = tmp_path / f"{version}_report.txt"
    assert report_path.exists()

    content = report_path.read_text()
    assert "DataFrame is valid" in content
    assert "Basic statistics" in content
    assert "value" in content  # Confirm describe output included

# ----------------------------
# Error Tests
# ---------------------------- 

def test_generate_report_fail(tmp_path,monkeypatch):

    monkeypatch.setattr('app.reporters.reporter.REPORTS_DIR',str(tmp_path))

    df = pd.DataFrame({"age": [25, -1, 130]})
    errors = {
        "age": [
            {"failure_case": -1, "check": "age >= 0"},
            {"failure_case": 130, "check": "age <= 120"},
        ]
    }

    version = "v999"
    is_valid = False
    total_rows = len(df)
    timestamp = "20240630_130000"

    generate_report(version, is_valid, errors, timestamp, df)

    report_path = tmp_path / f"{version}_report.txt"
    assert report_path.exists()

    content = report_path.read_text()
    assert "Total Issues: 2" in content
    assert "Column: age" in content
    assert "- -1 (Check: age >= 0)" in content
    assert "- 130 (Check: age <= 120)" in content