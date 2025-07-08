import pandas as pd
import pytest

from app.validators.schema import DataframeValidator


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "id": [1, 2, 2, None],
            "email": ["a@a.com", "invalid", None, "b@b.com"],
            "age": [20, 17, 105, 30],
            "name": ["Ana", None, "Luis", "Carlos"],
        }
    )


def test_validate_not_null(sample_df):
    validator = DataframeValidator(sample_df)
    validator.validate_not_null("name")

    assert len(validator.violations) == 1
    assert validator.violations[0]["rule"] == "not_null"
    assert validator.violations[0]["column"] == "name"
    assert validator.violations[0]["invalid_count"] == 1


def test_validate_range(sample_df):
    validator = DataframeValidator(sample_df)
    validator.validate_range("age", 18, 99)

    assert len(validator.violations) == 1
    assert validator.violations[0]["rule"] == "range"
    assert validator.violations[0]["invalid_count"] == 2
    assert 17 in validator.violations[0]["sample_invalid_values"]


def test_validate_regex(sample_df):
    validator = DataframeValidator(sample_df)
    validator.validate_regex("email", r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    assert len(validator.violations) == 1
    assert validator.violations[0]["rule"] == "regex"
    assert "invalid" in validator.violations[0]["sample_invalid_values"]


def test_validate_unique(sample_df):
    validator = DataframeValidator(sample_df)
    validator.validate_unique("id")

    assert len(validator.violations) == 1
    assert validator.violations[0]["rule"] == "unique"
    assert validator.violations[0]["invalid_count"] == 2


def test_apply_rules(sample_df):
    rules = [
        {"column": "name", "rule": "not_null"},
        {"column": "age", "rule": "range", "min": 18, "max": 99},
        {"column": "email", "rule": "regex", "pattern": r"[^@]+@[^@]+\.[^@]+"},
        {"column": "id", "rule": "unique"},
    ]

    validator = DataframeValidator(sample_df)
    result = validator.apply_rules(rules)

    assert len(result) == 4
    assert any(v["rule"] == "not_null" for v in result)
    assert any(v["rule"] == "range" for v in result)
    assert any(v["rule"] == "regex" for v in result)
    assert any(v["rule"] == "unique" for v in result)
