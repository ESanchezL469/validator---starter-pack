import sys
import os

sys.path.insert(0,os.path.abspath("."))

import pandas as pd
from app.validator import validate_dataframe

def test_validate_dataframe_ok():
    df = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'email': ['alice@example.com', 'bob@example.com', 'charlie@example.com'],
        'age': [25, 30, 22],
        'created_at': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03']),
        'is_active': [True, False, True]
    })
    is_valid, errors = validate_dataframe(df)
    assert is_valid is True
    assert errors == {}

def test_validate_dataframe_invalid():
    df = pd.DataFrame({
        'id': [1, 2, -3],  # Invalid id
        'name': ['Alice', '', None],  # Invalid name
        'email': ['alice@example.com', 'bob.com', ''],
        'age': [25, 30, None],
        'created_at': ['not a date', None, '2023-01-03'],
        'is_active': [True, 'no', None]
    })
    is_valid, errors = validate_dataframe(df)
    assert is_valid is False
    assert errors == {
        'id': ['Invalid id'],
        'name': ['Invalid name'],
        'email': ['Invalid email'],
        'age': ['Invalid age'],
        'created_at': ['Invalid created_at'],
        'is_active': ['Invalid is_active']
    }