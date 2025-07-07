# Validator - Starter Pack

![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A robust Data Quality as a Service (DQaaS) platform that enables you to:

- Upload a CSV, Excel, JSON or Parquet dataset
- Automatically validate schema with [Pandera](https://pandera.readthedocs.io/)
- Enrich the dataset with business rules (e.g. age groups)
- Generate profiling reports with [YData Profiling](https://github.com/ydataai/ydata-profiling)
- Version and store validated data
- Expose everything via a FastAPI endpoint

---

## 🚀 Quickstart

### 1. Clone and install dependencies
```bash
git clone https://github.com/your-org/validator-starter-pack.git
cd validator-starter-pack
pip install -r requirements.txt
```

### 2. Set up environment variables
Create a `.env` file in the root directory:
```env
DATASETS_DIR=datasets
METADATA_DIR=metadatas
REPORTS_DIR=reports
PROFILES_DIR=profiles
API_PORT=8080
```

### 3. Run the API
```bash
make run
```

Visit http://localhost:8080/docs for the interactive API docs.

---

## 🧪 Run Tests
```bash
make test
```

---

## 🧱 Project Structure
```
validator-starter-pack/
├── app/
│   ├── api/             # FastAPI router + main app
│   ├── core/            # DatasetValidator orchestrator
│   ├── validators/      # Pandera schema definitions
│   ├── enrichers/       # Data enrichment logic
│   ├── reporters/       # Plain text report generator
│   ├── profilers/       # ydata_profiling integration
│   ├── metadata/        # Metadata generation & tracking
│   ├── storage/         # File I/O, hashing, versioning
│   ├── config.py        # .env config loader
│   └── setup.py         # Directory initializer
├── datasets/            # Stored validated datasets (CSV/Parquet)
├── profiles/            # Generated HTML profiling reports
├── reports/             # Plaintext validation reports
├── metadatas/           # JSON metadata files
├── files/               # Example or temporary uploaded files
├── tests/               # Unit tests
├── .env                 # Environment variables
├── run.py               # Startup script
├── Makefile             # Development commands
├── requirements.txt     # Dependencies
└── README.md            # This file
```

---

## 📎 Sample CSV File
Save the following content in `files/sample.csv`:
```csv
id,name,email,age,created_at,is_active
1,Alice,alice@example.com,30,2023-01-01,True
2,Bob,bob@example.com,45,2022-06-15,False
3,Carol,carol@example.com,22,2024-03-10,True
```

Upload via Postman:
- Method: `POST`
- URL: `http://localhost:8080/validate/`
- Body: `form-data`
  - Key: `file`
  - Type: `File`
  - Value: select your `sample.csv`

---

## 📡 API Endpoint

### `POST /validate/`
Upload a dataset and run validation pipeline.

#### Form-Data
- `file`: your dataset file (CSV, Excel, JSON, Parquet)

#### Example Response
```json
{
  "status": "success",
  "message": "File sample.csv has validate",
  "is_valid": true,
  "hash": "abc123...",
  "total_rows": 3,
  "errors": {},
  "report_url": "/report/abc123",
  "metadata_url": "/metadata/abc123",
  "profile_url": "/profile/abc123"
}
```

---

## 🧰 Makefile Commands

| Command       | Description                           |
|---------------|---------------------------------------|
| `make run`    | Launch the API server                 |
| `make test`   | Run unit tests with Pytest            |
| `make clean`  | Clean up `.pyc`, `__pycache__`, etc.  |

---

## 📜 License
MIT License