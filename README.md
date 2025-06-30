# ⚙️ Validator - Starter Pack

![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A modular and reproducible **Data Validation Starter Pack** for data engineers and analysts.
Easily validate CSV datasets, enrich and profile data, generate quality reports, and track metadata and versions — all from a single command.

---

## 🚀 Features

* ✅ Schema Validation with custom rules
* ✅ Automatic Data Enrichment
* ✅ Exploratory Profiling (`ydata-profiling`)
* ✅ Quality Report Generation
* ✅ Metadata Versioning (via content hashing)
* ✅ Modular CLI Execution
* ✅ Docker Support
* ✅ Test Suite with Pytest

---

## 📁 Project Structure

```text
validator-starter-pack/
├── app/
│   ├── main.py                 # Entry point
│   ├── validator.py            # Validation logic (with Pandera)
│   ├── enricher.py             # Adds derived fields
│   ├── reporter.py             # Generates .txt reports
│   ├── profiler.py             # Profiling with ydata-profiling
│   ├── metadata_writer.py      # Metadata JSON generation
│   ├── storage.py              # File handling & versioning
│   ├── ingestor.py             # Loaders
│   └── source_tracker.py       # Hashing & tracking
├── datasets/                   # Input files
├── reports/                    # Quality reports (.txt)
├── metadata/                   # Metadata files (.json)
├── profiles/                   # Exploratory profiles (.html)
├── tests/                      # Pytest-based test suite
│   ├── test_pipeline_input_file.py
│   └── test_pipeline_input_folder.py
├── .env
├── .gitignore
├── requirements.txt
├── Dockerfile
├── Makefile
└── README.md
```

---

## 🔍 Validation Rules (Example Schema)

* `id`: Positive integer
* `name`: Non-empty string
* `email`: Valid email format
* `age`: Between 18 and 99
* `created_at`: Valid datetime
* `is_active`: Boolean

---

## 🧠 Automatic Enrichment

Automatically computed columns:

* `age_group`: Classified as `"young"`, `"adult"`, or `"senior"`
* `signup_year`: Derived from `created_at`

---

## 📄 Output Files

* `datasets/`: Validated CSV files, renamed with `{hash}_data.csv`
* `reports/`: Text reports `{hash}_report.txt`
* `metadata/`: Metadata JSON `{hash}_metadata.json`
* `profiles/`: Exploratory profile `{hash}_profile.html`

---

## ⚙️ How to Use

### ✅ Option 1: Run Locally

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the validator:

```bash
python app/main.py
```

3. Provide the path to your CSV file when prompted.

---

### 🛣️ Option 2: Run with Docker

1. Build the image:

```bash
docker build -t dataops-validator .
```

2. Run it with mounted volume:

```bash
docker run -it -v $(pwd)/datasets:/app/datasets dataops-validator
```

> Optional: Mount `reports/`, `metadata/` and `profiles/` for result persistence:

```bash
docker run -it \
  -v $(pwd)/datasets:/app/datasets \
  -v $(pwd)/reports:/app/reports \
  -v $(pwd)/metadata:/app/metadata \
  -v $(pwd)/profiles:/app/profiles \
  dataops-validator
```

---

## 🤖 Run Tests

```bash
pytest tests/
```

---

## 🛠️ Makefile Shortcuts

```bash
make install        # Install dependencies
make run            # Run the validator
make test           # Run tests
make docker-build   # Build the Docker image
make docker-run     # Run with Docker
```

---

## 📌 Tech Stack

* Python 3.11
* Pandas
* Pandera (schema validation)
* ydata-profiling
* Pytest
* Docker
* Make (optional)

---

## 🔮 Next Steps (Planned Roadmap)

* 🌐 REST API with FastAPI (for DQaaS model)
* 🧪 Integration of `great_expectations` for extended validation
* ☁️ Cloud storage support (S3, GCS)
* 📊 Orchestration with Airflow or Dagster
* 📊 Streamlit UI for simplified reporting
* 🗂️ PostgreSQL for metadata persistence
* 🔔 Slack/Email alerting for failures

---

## 📣 Contributions & Feedback

This project is open for contributions! Feel free to open issues, pull requests, or share feature ideas.

---

## 📄 License

Licensed under the MIT License.
