import pandera.pandas as pa
import pandas as pd
from pandera import Column, DataFrameSchema, Check
from pandera.errors import SchemaError,SchemaErrors

schema = DataFrameSchema({
    "id": Column(pa.Int, Check(lambda x: x > 0), nullable=False),
    "name": Column(pa.String, Check.str_length(min_value=1), nullable=False),
    "email": Column(pa.String, Check.str_matches(r"^[^@\s]+@[^@\s]+\.[^@\s]+$"), nullable=False),
    "age": Column(pa.Int, Check.in_range(18, 99), nullable=False),
    "created_at": Column(pa.DateTime, nullable=False),
    "is_active": Column(pa.Bool, nullable=False),
})

def validate_dataframe(df:pd.DataFrame):
    """
    Validate a Pandas DataFrame against a predefined schema.
    Args:
        df (pd.DataFrame): The DataFrame to validate.
    Returns:
        tuple: A tuple containing a boolean indicating if the DataFrame is valid and a dictionary of
        errors if any.
    """
    try:
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        schema.validate(df)
        return True, {}
    except (SchemaError,SchemaErrors) as e:
        failure_df = getattr(e, 'failure_cases', None)

        if isinstance(failure_df, pd.DataFrame):
            grouped_errors = {
                column: group[['failure_case', 'check']].to_dict(orient='records')
                for column, group in failure_df.groupby('column')
            }
        else:
            grouped_errors = {"error": str(e)}
            
        return False, grouped_errors
