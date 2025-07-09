import pandas as pd
import pytest

from app.profilers.profiler import generate_profile


def test_profiler_success(tmp_path, monkeypatch):
    monkeypatch.setattr("app.profilers.profiler.PROFILES_DIR", str(tmp_path))

    test_data = {"id": [1, 2], "name": ["Alice", "Bob"], "age": [25, 30]}
    output_file = generate_profile(pd.DataFrame(test_data), "test_profile")

    expected_path = tmp_path / "test_profile_profile.html"
    assert output_file == str(expected_path)
    assert expected_path.exists()
    assert expected_path.stat().st_size > 0


def test_profiler_fail(tmp_path, monkeypatch):
    monkeypatch.setattr("app.profilers.profiler.PROFILES_DIR", str(tmp_path))

    class Broken:
        def __repr__(self):
            raise ValueError("Broken repr")

    df = pd.DataFrame({"col": [Broken()]})

    with pytest.raises(Exception):
        generate_profile(df, "broken_file")
