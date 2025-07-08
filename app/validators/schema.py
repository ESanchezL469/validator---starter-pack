import pandas as pd
import re

class DataframeValidator:

    def __init__(self, df:pd.DataFrame):
        self.df: pd.DataFrame = df
        self.violations: list[dict] = []

    def validate_not_null(self, column:str) -> None:
        invalid_rows: pd.DataFrame = self.df[self.df[column].isnull()]
        if not invalid_rows.empty:
            self.violations.append({
                "column": column,
                "rule": "not_null",
                "description": f"Null values in column '{column}'",
                "invalid_count": len(invalid_rows),
                "sample_invalid_values": [None]
            })

    def validate_range(self, column:str, min_val:float, max_val:float) -> None:
        invalid_rows: pd.DataFrame = self.df[~self.df[column].between(min_val, max_val)]
        if not invalid_rows.empty:
            self.violations.append({
                "column": column,
                "rule": "range",
                "description": f"Out of range ({min_val}-{max_val}) in '{column}'",
                "invalid_count": len(invalid_rows),
                "sample_invalid_values": invalid_rows[column].dropna().unique().tolist()[:5]
            })

    def validate_regex(self, column:str, pattern:str) -> None:
        invalid_rows: pd.DataFrame = self.df[~self.df[column].astype(str).str.match(pattern)]
        if not invalid_rows.empty:
            self.violations.append({
                "column": column,
                "rule": "regex",
                "description": f"No found pattern '{pattern}' in '{column}'",
                "invalid_count": len(invalid_rows),
                "sample_invalid_values": invalid_rows[column].dropna().unique().tolist()[:5]
            })

    def validate_unique(self, column:str) -> None:
        duplicated: pd.DataFrame = self.df[self.df.duplicated(subset=[column], keep=False)]
        if not duplicated.empty:
            self.violations.append({
                "column": column,
                "rule": "unique",
                "description": f"Duplicate found in '{column}'",
                "invalid_count": len(duplicated),
                "sample_invalid_values": duplicated[column].dropna().unique().tolist()[:5]
            })

    def apply_rules(self, rules:list[dict]) -> list[dict]:

        for rule in rules:
            
            type = rule["rule"]
            col = rule["column"]

            match type:
                case "not_null":
                    self.validate_not_null(col)
                case "range":
                    self.validate_range(col,rule["min"],rule["max"])
                case "regex":
                    self.validate_regex(col,rule["pattern"])
                case "unique":
                    self.validate_unique(col)
                case _:
                    continue

        return self.violations