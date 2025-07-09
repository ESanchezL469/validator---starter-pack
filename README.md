# 🧪 Validator - Starter Pack

![Python](https://img.shields.io/badge/python-3.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://img.shields.io/badge/tests-pytest%20%2B%20httpx-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-pytest--cov-yellow)

A robust and extensible **Data Quality as a Service (DQaaS)** platform built with FastAPI and Pandas. This project enables you to upload and validate datasets against configurable rules, version them intelligently, and generate profiling and validation reports — all accessible via a clean, documented API.

---

## 🚀 Features

- 📤 Upload and validate CSV datasets via API
- 🔐 API key authentication for all endpoints
- 📐 Rule-based validation (`range`, `not_null`, `regex`, `unique`, etc.)
- 📊 Data profiling using `ydata-profiling`
- 🧠 Intelligent versioning using file content hashes
- 📝 Auto-generation of reports and metadata
- 🧪 Full unit + integration test suite
- ✅ CI-ready with GitHub Actions and pre-commit hooks

---

## 📁 Project Structure

```
validator-starter/
├── api/
│   ├── main.py                  # FastAPI app entrypoint
│   ├── routes/                  # API endpoints (validate, datasets, etc.)
│   └── utils/                   # File/path helpers
├── datasets/                   # Validated CSVs (versioned by hash)
├── metadatas/                  # Validation metadata (.json)
├── reports/                    # HTML reports (validation results)
├── profilers/                  # HTML profiling reports
├── tests/                      # Unit & integration tests
├── validation_rules/           # JSON rules applied to datasets
├── Makefile                    # CLI commands for setup, tests, coverage
├── .pre-commit-config.yaml     # Code quality automation
├── .github/workflows/ci.yml    # GitHub Actions CI workflow
├── .env.example                # Example env for local setup
└── requirements.txt            # Python dependencies
```

---

## ⚙️ Local Setup

```bash
# 1. Create virtual environment & install deps
make install

# 2. Create folders if missing
mkdir -p datasets metadatas reports profilers

# 3. Run the API locally
make run
```

The API will be available at:
📍 `http://0.0.0.0:8080`

---

## 🔐 Authentication

All endpoints require an API key via headers:

```
x-api-key: your_api_key_here
```

You can set the key using an `.env` file or default it in `config.py`.

---

## 📤 POST /validate/

Validate a CSV file against a set of rules and generate versioned artifacts.

### Headers
- `x-api-key: your_api_key_here`
- `Content-Type: multipart/form-data`

### Body (form-data)

| Field | Type | Description        |
|-------|------|--------------------|
| file  | File | CSV file to upload |

### Example using curl

```bash
curl -X POST http://localhost:8080/validate/   -H "x-api-key: your_api_key_here"   -F "file=@path/to/your.csv"
```

---

## 📂 Other Endpoints

All responses require authentication with the same header.

### 📄 `GET /datasets/history`

Returns a list of all validated dataset versions with basic metadata.

---

### 🔍 `GET /datasets/{hash}`

Returns detailed metadata (columns, rules applied, row counts, etc.) for a dataset by hash.

---

### 📦 `GET /datasets/file/{hash}`

Returns the original validated CSV file.

---

### 📊 `GET /reports/{hash}`

Returns the HTML validation report (auto-generated).

---

### 🧠 `GET /profilers/{hash}`

Returns the HTML profiling report (`ydata-profiling`).

---

## ✅ Validation Rules

Rules are defined as JSON files in `validation_rules/`.

Example: `validation_rules/customer.json`

```json
[
  { "column": "id", "rule": "not_null" },
  { "column": "email", "rule": "regex", "pattern": "^[^@\s]+@[^@\s]+\.[^@\s]+$" },
  { "column": "age", "rule": "range", "min": 18, "max": 99 },
  { "column": "name", "rule": "unique" }
]
```

Each file is automatically applied based on the uploaded filename (e.g., `customer.csv` → `customer.json`).

---

## 🧪 Testing

### Run unit tests

```bash
make test-unit
```

### Run integration/API tests

```bash
make test-api
```

### Run all tests

```bash
make test-all
```

---

## 📊 Code Coverage

```bash
make coverage
```

---

## 🔁 Pre-commit & Linting

Run checks (black, isort, flake8):

```bash
make run-checks
```

Install pre-commit hooks:

```bash
make setup-pre-commit
```

---

## 📌 Roadmap

- [x] Upload and validate CSV datasets via API
- [x] Autogenerate reports and metadata
- [x] Version datasets by content hash
- [x] Protect endpoints with API key
- [x] Pre-commit and CI via GitHub Actions
- [x] Retrieve datasets and reports via endpoints
- [ ] Add basic frontend UI (Streamlit / Gradio)
- [ ] Add Docker support
- [ ] Add deploy to Render or Railway
- [ ] CLI usage: `python -m validator file.csv`

---

## 📃 License

Licensed under the MIT License.

---

## 👨‍💻 Author

Built with ❤️ by **Santiago Sanchez** — open to feedback and contributions.
