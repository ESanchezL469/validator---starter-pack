# 🧪 Validator - Starter Pack

![Python](https://img.shields.io/badge/python-3.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://img.shields.io/badge/tests-pytest%20%2B%20httpx-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-pytest--cov-yellow)

A robust and extensible **Data Quality as a Service (DQaaS)** platform built with FastAPI and Pandas. This project enables you to upload and validate datasets against configurable rules, version them intelligently, and generate profiling and validation reports — all accessible via a clean, documented API.

## 🚀 Features

- 📤 Upload and validate CSV datasets via API
- 🔐 API key authentication for all endpoints
- 📐 Rule-based validation (`range`, `not_null`, `regex`, `unique`, etc.)
- 📊 Data profiling using `ydata-profiling`
- 🧠 Intelligent versioning using file content hashes
- 📝 Auto-generation of reports and metadata
- 🧪 Full unit + integration test suite
- ✅ CI-ready with GitHub Actions and pre-commit hooks

## 🧱 Project Structure

```
validator-starter/
├── app/                        # Backend core (FastAPI, logic, validation)
├── frontend/                   # Streamlit frontend UI
├── datasets/                   # Validated CSVs (versioned)
├── metadatas/                  # JSON validation metadata
├── reports/                    # Validation HTML reports
├── profilers/                  # Profiling HTML reports
├── tests/                      # Unit + integration tests
├── Makefile                    # Dev workflow commands
├── .env.example                # Environment config sample
├── requirements.txt            # Global/shared dependencies
```

## ⚙️ Local Setup

```bash
make venv           # Create both backend/frontend virtualenvs
make install        # Install all backend/frontend dependencies
make run-backend    # Run the FastAPI backend
make run-ui         # Run the Streamlit frontend
```

## 🔐 Authentication

All endpoints require a header:

```
x-api-key: your_api_key_here
```

Defined via `.env` or directly in `config.py`.

## 📤 Validation Endpoint

**POST /validate?rules_file=your_rules.json**

- `file`: CSV (multipart/form-data)
- `rules_file`: JSON file name in `validation_rules/`

## ✅ Example Rules (JSON)

```json
[
  { "column": "id", "rule": "not_null" },
  { "column": "email", "rule": "regex", "pattern": "^[^@\s]+@[^@\s]+\.[^@\s]+$" },
  { "column": "age", "rule": "range", "min": 18, "max": 99 },
  { "column": "name", "rule": "unique" }
]
```

## ✅ Run Tests

```bash
make test-unit
make test-api
make coverage
```

## 📦 Ready to Deploy

- [x] Add Docker support
- [ ] Deploy to Render/Railway
- [ ] CLI usage: `python -m validator file.csv`
