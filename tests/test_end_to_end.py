import subprocess
import os
import glob
import shutil

def test_full_pipeline(tmp_path):

    input_dir = tmp_path / "input_folder"
    input_dir.mkdir()
    
    content = "id,name,email,age,created_at,is_active\n"
    content1 = content + "1,John Doe,john@example.com,30,2023-01-01,True\n"
    content2 = content + "2,Bob Smith,bob@example.com,25,2023-01-02,False\n"

    (input_dir / "test_1.csv").write_text(content1)
    (input_dir / "test_2.csv").write_text(content2)

    for folder in ["datasets", "reports", "metadata"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)

    env = os.environ.copy()
    env["PYTHONPATH"] = "."

    result = subprocess.run(
        ["python", "app/main.py", "--input-folder", str(input_dir)],
        capture_output=True,
        text=True,
        env=env
    )

    for i in range(2):
        assert f'Data processed successfully for file: {input_dir / f"test_{i+1}.csv"}' in result.stdout, "File processing did not complete successfully."

    assert len(glob.glob('datasets/*_data.csv')) == 2, "Not all datasets were created."
    assert len(glob.glob('reports/*_report.txt')) == 2, "No report files were created."
    assert len(glob.glob('metadata/*_metadata.json')) == 2, "No metadata files were created."