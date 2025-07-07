import pytest
import json
import pandas as pd
from unittest.mock import patch
from app.metadata.metadata import save_metadata
from unittest.mock import MagicMock

# ----------------------------
# Successful Tests
# ----------------------------

def test_save_metadata_success(tmp_path,monkeypatch):

    monkeypatch.setattr('app.metadata.metadata.METADATA_DIR',str(tmp_path))

    mock_validator = MagicMock()
    mock_validator.version = "test123"
    mock_validator.timestamp = "20240630_235959"
    mock_validator.is_valid = True
    mock_validator.error = {}
    mock_validator.path = "input.csv"
    mock_validator.previous = None
    mock_validator.data = pd.DataFrame({"id": [1, 2], "name": ["Alice", "Bob"]})

    save_metadata(mock_validator)

    metadata_file = tmp_path / "test123_metadata.json"
    assert metadata_file.exists()

    with open(metadata_file, "r", encoding="utf-8") as f:
        metadata = json.load(f)
        assert metadata["version"] == "test123"
        assert metadata["timestamp"] == "20240630_235959"
        assert metadata["columns"] == ["id", "name"]
        assert metadata["total_rows"] == 2
        assert metadata["is_valid"] is True
        assert metadata["source_file"] == "input.csv"
        assert metadata["replaces"] is None
        assert metadata["errors"] == {}

# ----------------------------
# Error Tests
# ---------------------------- 

def test_save_metadata_fail(tmp_path,monkeypatch):
    pass