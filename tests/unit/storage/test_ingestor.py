import pandas as pd

from app.storage.ingestor import load_file

# ----------------------------
# Successful Load Tests
# ----------------------------


def test_load_csv(tmp_path):
    file = tmp_path / "test.csv"
    file.write_text("col1,col2\n1,2\n3,4")
    df, ext = load_file(file)
    assert df.shape == (2, 2)
    assert df.columns.tolist() == ["col1", "col2"]
    assert ext == ".csv"


def test_load_excel(tmp_path):
    file = tmp_path / "test.xlsx"
    pd.DataFrame({"id": [1], "name": ["Alice"]}).to_excel(file, index=False)
    df, ext = load_file(file)
    assert df.shape == (1, 2)
    assert ext == ".xlsx"


def test_load_json(tmp_path):
    file = tmp_path / "data.json"
    file.write_text('[{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]')
    df, ext = load_file(file)
    assert df.shape == (2, 2)
    assert ext == ".json"


def test_load_parquet(tmp_path):
    file = tmp_path / "data.parquet"
    pd.DataFrame({"id": [1], "name": ["Alice"]}).to_parquet(file)
    df, ext = load_file(file)
    assert df.shape == (1, 2)
    assert ext == ".parquet"


# ----------------------------
# Error Handling Tests
# ----------------------------


def test_load_unsupported_extension(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("id|name\n1|Alice")
    df, ext = load_file(file)
    assert df.empty


def test_load_file_not_found(tmp_path):
    df, ext = load_file("nonexistent.parquet")
    assert df.empty
