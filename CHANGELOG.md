# 📦 Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Endpoint `/validate/` with API key auth
- Rule engine: `range`, `regex`, `not_null`, `unique`
- JSON-based rule configuration
- Version control with hash
- Profiling report with `ydata-profiling`
- Full test suite (unit & integration)
- Code coverage with `pytest-cov`

---

## [1.0.0] - 2025-07-07

### Added
- Initial public release
- FastAPI backend
- Upload and validate CSV
- Rule file loading from `validation_rules/`
