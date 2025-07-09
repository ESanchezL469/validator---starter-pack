import pandas as pd


class DataframeValidator:
    """
    Applies a set of validation rules to a pandas DataFrame and records fails.

    Attributes:
        df (pd.DataFrame): The input DataFrame to validate.
        violations (List[Dict]): List of rule fails found.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initialize the validator with a DataFrame.

        Args:
            df (pd.DataFrame): The dataset to validate.
        """
        self.df: pd.DataFrame = df
        self.violations: list[dict] = []

    def validate_not_null(self, column: str) -> None:
        """
        Check that a column does not contain null values.

        Args:
            column (str): The name of the column to check.
        """
        invalid_rows: pd.DataFrame = self.df[self.df[column].isnull()]
        if not invalid_rows.empty:
            self.violations.append(
                {
                    "column": column,
                    "rule": "not_null",
                    "description": f"Null values in column '{column}'",
                    "invalid_count": len(invalid_rows),
                    "sample_invalid_values": [None],
                }
            )

    def validate_range(self, column: str, min_val: float, max_val: float):
        """
        Check that a numeric column falls within a specific range.

        Args:
            column (str): Column name.
            min_val (float): Minimum valid value.
            max_val (float): Maximum valid value.
        """
        mask = self.df[column].between(min_val, max_val)
        invalid_rows: pd.DataFrame = self.df.loc[~mask].copy()
        if not invalid_rows.empty:
            self.violations.append(
                {
                    "column": column,
                    "rule": "range",
                    "description": f"Out of range ({min_val}-{max_val})'",
                    "invalid_count": len(invalid_rows),
                    "sample_invalid_values": invalid_rows[column]
                    .dropna()
                    .unique()
                    .tolist()[:5],
                }
            )

    def validate_regex(self, column: str, pattern: str) -> None:
        """
        Check that a column's values match a regular expression pattern.

        Args:
            column (str): Column name.
            pattern (str): Regex pattern to match.
        """
        invalid_rows: pd.DataFrame = self.df[
            ~self.df[column].astype(str).str.match(pattern)
        ]
        if not invalid_rows.empty:
            self.violations.append(
                {
                    "column": column,
                    "rule": "regex",
                    "description": f"No found pattern '{pattern}'",
                    "invalid_count": len(invalid_rows),
                    "sample_invalid_values": invalid_rows[column]
                    .dropna()
                    .unique()
                    .tolist()[:5],
                }
            )

    def validate_unique(self, column: str) -> None:
        """
        Check that a column contains only unique values.

        Args:
            column (str): Column name.
        """
        duplicated: pd.DataFrame = self.df[
            self.df.duplicated(subset=[column], keep=False)
        ]
        if not duplicated.empty:
            self.violations.append(
                {
                    "column": column,
                    "rule": "unique",
                    "description": f"Duplicate found in '{column}'",
                    "invalid_count": len(duplicated),
                    "sample_invalid_values": duplicated[column]
                    .dropna()
                    .unique()
                    .tolist()[:5],
                }
            )

    def apply_rules(self, rules: list[dict]) -> list[dict]:
        """
        Apply a list of validation rules to the DataFrame.

        Args:
            rules (List[Dict]): A list of rule dictionaries.

        Returns:
            List[Dict]: List of violations found.
        """
        for rule in rules:
            type = rule["rule"]
            col = rule["column"]

            match type:
                case "not_null":
                    self.validate_not_null(col)
                case "range":
                    self.validate_range(col, rule["min"], rule["max"])
                case "regex":
                    self.validate_regex(col, rule["pattern"])
                case "unique":
                    self.validate_unique(col)
                case _:
                    continue

        return self.violations
