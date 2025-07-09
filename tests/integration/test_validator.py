from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from app.api.validator import DatasetValidator  # Ajusta el path real


@pytest.fixture
def test_df():
    return pd.DataFrame(
        {
            "id": [1, 2],
            "email": ["a@a.com", "b@b.com"],
            "age": [25, 30],
            "name": ["Ana", "Luis"],
        }
    )


@pytest.fixture
def valid_rules():
    return [
        {"column": "name", "rule": "not_null"},
        {"column": "age", "rule": "range", "min": 18, "max": 99},
    ]


@patch("app.api.validator.os.path.exists", return_value=True)
@patch("app.api.validator.load_file")
@patch("app.api.validator.validate_rule_structure")
@patch("app.api.validator.DataframeValidator")
@patch("app.api.validator.enrich_dataframe")
@patch("app.api.validator.calculate_hash")
@patch("app.api.validator.version_exists")
@patch("app.api.validator.save_dataframe")
@patch("app.api.validator.generate_profile")
@patch("app.api.validator.generate_report")
@patch("app.api.validator.find_previous_version")
@patch("app.api.validator.save_metadata")
def test_run_pipeline_valid_flow(
    mock_save_metadata,
    mock_find_previous_version,
    mock_generate_report,
    mock_generate_profile,
    mock_save_dataframe,
    mock_version_exists,
    mock_calculate_hash,
    mock_enrich_dataframe,
    mock_DataframeValidator,
    mock_validate_rule_structure,
    mock_load_file,
    mock_path_exists,
    test_df,
    valid_rules,
):
    # Configurar mocks
    mock_load_file.return_value = (test_df, "csv")
    mock_validate_rule_structure.return_value = []

    mock_validator_instance = MagicMock()
    mock_validator_instance.apply_rules.return_value = []
    mock_DataframeValidator.return_value = mock_validator_instance

    mock_enrich_dataframe.return_value = test_df
    mock_calculate_hash.return_value = "mocked_hash"
    mock_version_exists.return_value = False
    mock_save_dataframe.return_value = ("mocked_hash", "2025-07-07T00:00:00")
    mock_find_previous_version.return_value = "prev_hash"

    # Ejecutar el pipeline
    validator = DatasetValidator(path="dummy_path.csv", enableProfile=True)
    validator.load_rules = MagicMock(return_value=valid_rules)
    result = validator.run_pipeline()

    # Verifica retorno final
    assert result == "File dummy_path.csv has been validated"

    # Verifica estado interno
    assert validator.is_valid is True
    assert validator.version == "mocked_hash"
    assert validator.timestamp == "2025-07-07T00:00:00"
    assert validator.previous == "prev_hash"
    assert validator.error == []
    assert isinstance(validator.data, pd.DataFrame)

    # Verifica llamadas clave
    mock_path_exists.assert_called_once()
    mock_load_file.assert_called_once_with("dummy_path.csv")
    mock_validate_rule_structure.assert_called_once_with(valid_rules)
    mock_DataframeValidator.assert_called_once()
    mock_validator_instance.apply_rules.assert_called_once_with(valid_rules)
    mock_enrich_dataframe.assert_called_once_with(test_df)
    mock_calculate_hash.assert_called_once_with(test_df)
    mock_version_exists.assert_called_once_with("mocked_hash")
    mock_save_dataframe.assert_called_once_with(test_df)
    mock_generate_report.assert_called_once_with(
        "mocked_hash", True, [], "2025-07-07T00:00:00", test_df
    )
    mock_generate_profile.assert_called_once_with(test_df, "mocked_hash")
    mock_find_previous_version.assert_called_once_with("mocked_hash")
    mock_save_metadata.assert_called_once_with(validator)


@patch("app.api.validator.load_file")
@patch("app.api.validator.validate_rule_structure")
def test_run_pipeline_invalid_rules(
    mock_validate_rule_structure, mock_load_file, test_df
):
    mock_load_file.return_value = (test_df, "csv")
    mock_validate_rule_structure.return_value = ["Regla inválida"]

    validator = DatasetValidator(path="files/sample.csv")
    validator.load_rules = lambda _="": [{"column": "email", "rule": "regex"}]
    result = validator.run_pipeline()

    assert result == "Error in rules"
    assert validator.rules_error == ["Regla inválida"]


@patch("app.api.validator.os.path.exists")
def test_run_pipeline_file_not_found(mock_exists):
    mock_exists.return_value = False

    validator = DatasetValidator(path="nonexistent.csv")
    result = validator.run_pipeline()

    assert result == "File nonexistent.csv does not exist."
