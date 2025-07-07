import pytest
import pandas as pd
from app.profilers.profiler import generate_profile

# ----------------------------
# Successful Tests
# ----------------------------

def test_profiler_success(tmp_path,monkeypatch):

    monkeypatch.setattr('app.profilers.profiler.PROFILES_DIR',str(tmp_path))

    df = pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Carol"],
        "age": [25, 30, 35]
    })

    file_name = "test_profile"
    output_file = generate_profile(df, file_name)

    expected_path = tmp_path / f"{file_name}_profile.html"
    assert output_file == str(expected_path)
    assert expected_path.exists()
    assert expected_path.stat().st_size > 0

# ----------------------------
# Error Tests
# ---------------------------- 

def test_profiler_fail(tmp_path,monkeypatch):

    monkeypatch.setattr('app.profilers.profiler.PROFILES_DIR',str(tmp_path))

    class Broken:
        def __repr__(self):
            raise ValueError("Broken repr")

    df = pd.DataFrame({"col": [Broken()]})

    with pytest.raises(Exception):
        generate_profile(df, "broken_file")