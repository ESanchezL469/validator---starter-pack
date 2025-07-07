import pandas as pd
from app.validators.schema import validate_dataframe

# ----------------------------
# Successful Tests
# ----------------------------

def test_validate_dataframe_success():
    df = pd.DataFrame({
        "id": [1],
        "name": ["Alice"],
        "email": ["alice@example.com"],
        "age": [30],
        "created_at": ["2023-01-01"],
        "is_active": [True]
    })
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
    is_valid, errors = validate_dataframe(df)
    assert is_valid is True
    assert errors == {}

# ----------------------------
# Error Tests
# ---------------------------- 