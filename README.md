# 🧪 Validator - Starter Pack

![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://img.shields.io/badge/tests-pytest%20%2B%20httpx-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-pytest--cov-yellow)

A robust and extensible **Data Quality as a Service (DQaaS)** platform built with FastAPI and Pandas. This project enables you to upload datasets, validate them against configurable rules, track dataset versions, and generate data profiling reports.

---

## 🚀 Features

- 📤 Upload and validate CSV datasets via API  
- 🔐 API key authentication  
- 📐 Rule-based validation (e.g., `range`, `not_null`, `regex`, `unique`)  
- 📊 Data profiling using `ydata-profiling`  
- 🧠 Intelligent versioning using content-based hashing  
- 📝 Automatic report and metadata generation  
- ✅ Full test suite (unit & integration)  
- 🧪 Code coverage with `pytest-cov`  

---

## 📁 Project Structure

```
validator/
├── app/
│   ├── api/               # FastAPI routes and security
│   ├── config.py          # Global paths and config
│   ├── validators/        # Rule engine & schema validators
│   ├── enrichers/         # Optional data enrichment
│   ├── profilers/         # Generates profiling reports
│   ├── reporters/         # Builds validation reports
│   ├── storage/           # File storage and hashing
│   ├── metadata/          # Version tracking and metadata
├── tests/                 # Unit & integration tests
├── validation_rules/      # JSON rule definitions
├── scripts/               # Helper scripts (e.g., init_dirs.py)
├── requirements.txt       # Dependencies
├── Makefile               # CLI commands for dev & testing
└── run.py                 # Entry point to launch the API
```

---

## ⚙️ Setup

```bash
# 1. Install dependencies
make install

# 2. Create necessary directories
python scripts/init_dirs.py

# 3. Run the API
make run
```

The API will be available at:  
📍 `http://0.0.0.0:8080/validate/`

---

## 🔐 API Authentication

All requests must include an API key header:

```
x-api-key: your_api_key_here
```

---

## 📤 API Usage: `POST /validate/`

### Headers

- `x-api-key: your_api_key_here`
- `Content-Type: multipart/form-data`

### Body (form-data)

| Field | Type | Description        |
|-------|------|--------------------|
| file  | File | CSV file to upload |

### Example using `curl`

```bash
curl -X POST http://0.0.0.0:8080/validate/ \
  -H "x-api-key: your_api_key_here" \
  -F "file=@path/to/your.csv"
```

---

## ✅ Validation Rules

Validation rules must be defined in JSON format and placed in the `validation_rules/` directory.

Example `validation_rules/customer.json`:

```json
[
  { "column": "id", "rule": "not_null" },
  { "column": "age", "rule": "range", "min": 18, "max": 99 },
  { "column": "email", "rule": "regex", "pattern": "^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$" },
  { "column": "name", "rule": "unique" }
]
```

---

## 🧪 Testing

### Run unit tests
```bash
make test-unit
```

### Run API tests
```bash
make test-api
```

### Run all tests
```bash
make test-all
```

---

## 📊 Code Coverage

To check code coverage in the terminal:
```bash
make coverage
```

---

## 🐍 Requirements

- Python 3.11+
- pip (or virtualenv/conda)
- See `requirements.txt` for all dependencies

---

## 📌 TODO / Roadmap

- [ ] Add CLI usage: `python -m validator file.csv`
- [ ] Add rule chaining / conditional logic
- [ ] Add history endpoint: `/history?filename=...`
- [ ] Dockerize the project
- [ ] Add basic UI (Streamlit or Gradio)
- [ ] Deploy to cloud (Render, Railway, etc.)

---

## 📃 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

Built by Santiago Sanchez — open to feedback, improvements, or collaboration!