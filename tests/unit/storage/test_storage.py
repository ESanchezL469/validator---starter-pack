import pandas as pd
from app.storage.storage import calculate_hash,save_dataframe

# ----------------------------
# Successful tests
# ----------------------------

def test_calculate_hash_consistent():
    df = pd.DataFrame({"id": [1], "name": ["Alice"]})
    h1 = calculate_hash(df)
    h2 = calculate_hash(df)
    assert isinstance(h1,str)
    assert h1 == h2
    assert len(h1)==64

def test_calculate_hash_data_with_changes():
    df1 = pd.DataFrame({"id": [1], "name": ["Alice"]})
    df2 = pd.DataFrame({"id": [1], "name": ["Bob"]})
    h1 = calculate_hash(df1)
    h2 = calculate_hash(df2)
    assert h1 != h2

def test_save_dataframe_file(tmp_path,monkeypatch):
    monkeypatch.setattr("app.storage.storage.DATASETS_DIR",str(tmp_path))
    df = pd.DataFrame({"id": [1, 2], "name": ["Alice", "Bob"]})
    version, timestamp = save_dataframe(df)

    assert version is not None
    assert timestamp is not None

    expected_file = tmp_path / f"{version}_data.csv"
    assert expected_file.exists()

    df_loaded = pd.read_csv(expected_file)
    assert df.equals(df_loaded)


# ----------------------------
# Error tests
# ----------------------------

def test_calculate_hash_invalid_input():
    result = calculate_hash(None)
    assert result is None

def test_save_dataframe_invalid():
    version, timestamp = save_dataframe(None)
    assert version is None
    assert timestamp is None