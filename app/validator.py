import pandera as pa
from pandera import Column, DataFrameSchema, Check

schema: DataFrameSchema = DataFrameSchema({
    "id": Column(pa.Int, Check(lambda x: x > 0), nullable=False),
    "name": Column(pa.String, Check(lambda x: x.str.len() > 0), nullable=False),
    "email": Column(pa.String, Check(lambda x: x.str.contains("@")), nullable=False),
    "age": Column(pa.Int, Check(lambda x: (x >= 18) & (x <= 99)), nullable=True),
    "created_at": Column(pa.DateTime, nullable=False),
    "is_active": Column(pa.Bool, nullable=False)
})

def validate_dataframe(df) -> tuple[bool, any]:
    """
    Validate the DataFrame against the schema.
    
    Args:
        df (pd.DataFrame): The DataFrame to validate.
    
    Returns:
        pd.DataFrame: The validated DataFrame.
    
    Raises:
        pa.errors.SchemaError: If the DataFrame does not conform to the schema.
    """
    try:
        schema.validate(df)
        return True, {}
    except pa.errors.SchemaError as e:
        return False, e.errors
