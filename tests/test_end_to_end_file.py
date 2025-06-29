import subprocess
import os
import glob
import shutil

def test_full_pipeline_file(tmp_path):

    input_file = tmp_path / "test.csv"
    input_file.write_text(
        "id,name,email,age,created_at,is_active\n"
        "1,John Doe,john@example.com,30,2023-01-01,True\n"
        "2,Bob Smith,bob@example.com,25,2023-01-02,False\n"
    )

    env = os.environ.copy()
    env["PYTHONPATH"] = "."

    for folder in ["datasets", "reports", "metadata","profiles"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)

    result = subprocess.run(
        ["python", "app/main.py", "--input", str(input_file)],
        capture_output=True,
        text=True,
        env=env
    )
    assert f'''Data processed successfully for file: {input_file}''' in result.stdout, "File processing did not complete successfully."

    assert len(glob.glob('datasets/*_data.csv')) > 0, "Not all datasets were created."
    assert len(glob.glob('reports/*_report.txt')) > 0, "No report files were created."
    assert len(glob.glob('metadata/*_metadata.json')) > 0, "No metadata files were created."

def test_full_pipeline_file_profile(tmp_path):

    input_file = tmp_path / "test.csv"
    input_file.write_text(
        "id,name,email,age,created_at,is_active\n"
        "1,John Doe,john@example.com,30,2023-01-01,True\n"
        "2,Bob Smith,bob@example.com,25,2023-01-02,False\n"
    )

    env = os.environ.copy()
    env["PYTHONPATH"] = "."

    for folder in ["datasets", "reports", "metadata","profiles"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)

    result = subprocess.run(
        ["python", "app/main.py", "--input", str(input_file), "--profile"],
        capture_output=True,
        text=True,
        env=env
    )
    assert f'''Data processed successfully for file: {input_file}''' in result.stdout, "File processing did not complete successfully."

    assert len(glob.glob('datasets/*_data.csv')) > 0, "Not all datasets were created."
    assert len(glob.glob('reports/*_report.txt')) > 0, "No report files were created."
    assert len(glob.glob('metadata/*_metadata.json')) > 0, "No metadata files were created."
    assert len(glob.glob('profiles/*_profile.html')) > 0, "No profile report files were created."