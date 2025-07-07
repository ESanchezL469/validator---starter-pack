import pandas as pd

def enrich_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enrich the DataFrame with additional columns.
    
    Args:
        df (pd.DataFrame): The input DataFrame to enrich.
        
    Returns:
        pd.DataFrame: The enriched DataFrame.
    """
    df = df.copy()

    if 'age' in df.columns:
        df['age_group'] = pd.cut(
            df['age'],
            bins=[0, 25, 45, 120],
            labels=['joven', 'adulto', 'senior'],
            right=False
        )

    if 'created_at' in df.columns:
        df['signup_year'] = pd.to_datetime(df['created_at'], errors='coerce').dt.year

    return df