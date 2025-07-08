import pandas as pd

from app.enrichers.enricher import enrich_dataframe

# ----------------------------
# Successful Tests
# ----------------------------


def test_enrich_dataframe_age():
    df = pd.DataFrame({"age": [18, 30, 60]})
    enriched = enrich_dataframe(df)
    assert "age_group" in enriched.columns
    assert enriched["age_group"].tolist() == ["joven", "adulto", "senior"]


def test_enrich_dataframe_created():
    df = pd.DataFrame({"created_at": ["2020-01-01", "2021-06-15"]})
    enriched = enrich_dataframe(df)
    assert "signup_year" in enriched.columns
    assert enriched["signup_year"].tolist() == [2020, 2021]


def test_enrich_dataframe_both():
    df = pd.DataFrame({"age": [40], "created_at": ["2019-12-31"]})
    enriched = enrich_dataframe(df)
    assert enriched["age_group"].iloc[0] == "adulto"
    assert enriched["signup_year"].iloc[0] == 2019


# ----------------------------
# Error Tests
# ----------------------------


def test_enrich_with_missing_columns():
    df = pd.DataFrame({"id": [1]})
    enriched = enrich_dataframe(df)
    assert "age_group" not in enriched.columns
    assert "signup_year" not in enriched.columns


def test_enrich_with_invalid_date():
    df = pd.DataFrame({"created_at": ["not-a-date"]})
    enriched = enrich_dataframe(df)
    assert pd.isna(enriched["signup_year"].iloc[0])
