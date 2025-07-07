import pandas as pd
import os
import logging

from ydata_profiling import ProfileReport
from app.config import PROFILES_DIR

logging.getLogger("ydata_profiling").setLevel(logging.CRITICAL)

def generate_profile(df: pd.DataFrame, file_name: str) -> str:
    """
    Generate a profile report for the given data and save it to a file.
    """
    output_file = os.path.join(PROFILES_DIR, f"{file_name}_profile.html")
    
    profile = ProfileReport(df, title=f"Data Profile Report", explorative=True)
    profile.to_file(output_file)
    
    return output_file