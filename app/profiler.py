from ydata_profiling import ProfileReport
import os

PROFILES_DIR = 'profiles'

def generate_profile_report(df, file_name: str) -> str:
    """
    Generate a profile report for the given data and save it to a file.
    """
    os.makedirs(PROFILES_DIR, exist_ok=True)
    output_file = os.path.join(PROFILES_DIR, f"{file_name}_profile.html")
    
    profile = ProfileReport(df, title=f"Data Profile Report", explorative=True)
    profile.to_file(output_file)
    
    return output_file