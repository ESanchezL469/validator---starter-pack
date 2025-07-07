import pandas as pd
from unittest.mock import patch
from app.api.validator import DatasetValidator

@patch("app.api.validator.save_metadata")
@patch("app.api.validator.find_previous_version")
@patch("app.api.validator.generate_report")
@patch("app.api.validator.generate_profile")
@patch("app.api.validator.save_dataframe")
@patch("app.api.validator.version_exists")
@patch("app.api.validator.calculate_hash")
@patch("app.api.validator.enrich_dataframe")
@patch("app.api.validator.validate_dataframe")
@patch("app.api.validator.load_file")
def test_dataset_validator_pipeline(mock_load, mock_validate, mock_enrich, mock_hash, mock_exists,
                                    mock_save, mock_profile, mock_report, mock_previous, mock_metadata,
                                    tmp_path):

    csv_path = tmp_path / "data.csv"
    df = pd.DataFrame({"id": [1], "name": ["Alice"], "email": ["alice@example.com"],
                       "age": [30], "created_at": ["2023-01-01"], "is_active": [True]})
    df.to_csv(csv_path, index=False)

    # Mocks
    mock_load.return_value = (df, "csv")
    mock_validate.return_value = (True, {})
    mock_enrich.return_value = df
    mock_hash.return_value = "abc123"
    mock_exists.return_value = False
    mock_save.return_value = ("abc123", "20240630_150000")
    mock_previous.return_value = None

    # Ejecutar
    validator = DatasetValidator(path=str(csv_path), enableProfile=True)
    result = validator.run_pipeline()

    # Verificación
    assert result == f"File {csv_path} has validate"
    assert validator.version == "abc123"
    assert validator.is_valid is True
    assert validator.typeFile == "csv"
    assert validator.error == {}


@patch("app.api.validator.version_exists", return_value=True)
@patch("app.api.validator.calculate_hash", return_value="abc123")
@patch("app.api.validator.validate_dataframe")
@patch("app.api.validator.load_file")
def test_dataset_validator_already_validated(mock_load, mock_validate, mock_hash, mock_exists, tmp_path):
    csv_path = tmp_path / "data.csv"
    df = pd.DataFrame({"id": [1], "name": ["Alice"], "email": ["alice@example.com"],
                       "age": [30], "created_at": ["2023-01-01"], "is_active": [True]})
    df.to_csv(csv_path, index=False)

    mock_load.return_value = (df, "csv")
    mock_validate.return_value = (True, {})

    validator = DatasetValidator(path=str(csv_path))
    result = validator.run_pipeline()

    assert result == f"File {csv_path} was already validate"

def test_dataset_validator_file_not_found(tmp_path):
    missing_path = tmp_path / "missing.csv"
    validator = DatasetValidator(path=str(missing_path))
    result = validator.run_pipeline()
    assert result == f"File {missing_path} does not exist."
