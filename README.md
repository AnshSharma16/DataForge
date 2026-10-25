# DataForge — Data Ingestion & Validation Pipeline

A Python-based data engineering project for ingesting data from CSV files and REST APIs, validating schemas, transforming records, and loading reliable, structured data into PostgreSQL.

## Overview

DataForge is designed to demonstrate practical data engineering and backend development principles through a modular, testable ETL pipeline. It focuses on data quality, reliable ingestion, database integrity, and failure recovery.

The pipeline separates ingestion, validation, transformation, loading, and reporting into independent components.

## Architecture

```text
CSV Files / REST APIs
         |
         v
  Ingestion Layer
         |
         v
 Schema Validation
         |
         v
 Transformation & Cleaning
         |
         v
  Deduplication
         |
         v
   +-----+------+
   |            |
   v            v
Valid Records  Invalid Records
   |            |
   v            v
PostgreSQL   Quarantine Table
   |
   v
Run History & Quality Reports
```

## Key Features

- **Multi-source ingestion:** Read structured data from CSV files and REST APIs.
- **Schema validation:** Validate required fields, data types, constraints, and malformed records.
- **Data transformation:** Normalize values, parse dates, handle missing values, and standardize records.
- **Deduplication:** Identify duplicate records using configurable business keys.
- **Batch loading:** Load validated data into PostgreSQL using SQLAlchemy.
- **Idempotent processing:** Design reruns to avoid duplicate records through unique constraints and upserts.
- **Error handling:** Apply request timeouts, configurable retries, and structured error reporting.
- **Data quarantine:** Preserve invalid records and their validation errors for investigation.
- **Pipeline observability:** Track execution status, record counts, processing duration, and failures.
- **Automated testing:** Test validation rules, transformations, duplicate handling, and database behavior.
- **Continuous integration:** Run automated checks through GitHub Actions.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Pipeline implementation |
| Pandas | Tabular data processing |
| Pydantic | Schema and configuration validation |
| HTTPX | REST API ingestion |
| SQLAlchemy 2.x | Database access |
| PostgreSQL | Persistent storage |
| pytest | Automated testing |
| GitHub Actions | CI and quality checks |

## Project Structure

```text
dataforge/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── csv_reader.py
│   │   └── api_client.py
│   ├── validation/
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── transformations/
│   │   ├── __init__.py
│   │   └── cleaning.py
│   ├── loading/
│   │   ├── __init__.py
│   │   └── postgres_loader.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── pipeline.py
│   └── reporting/
│       ├── __init__.py
│       └── metrics.py
├── tests/
│   ├── test_ingestion.py
│   ├── test_validation.py
│   ├── test_transformations.py
│   ├── test_loading.py
│   └── test_pipeline.py
├── data/
│   └── sample.csv
├── reports/
├── .github/
│   └── workflows/
│       └── ci.yml
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.12 or later
- Git
- A PostgreSQL database for database integration and end-to-end testing

Development can be performed in GitHub Codespaces or another cloud IDE without installing a local database server.

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd dataforge
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

On Linux or macOS:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file based on `.env.example`.

Example:

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:5432/DATABASE
API_TIMEOUT_SECONDS=15
MAX_RETRIES=3
BATCH_SIZE=500
LOG_LEVEL=INFO
```

Replace the database placeholders with valid credentials. Never commit `.env` or real credentials to Git.

### 5. Run the tests

```bash
pytest -v
```

The tests should run without a production database where suitable unit tests and mocks are used. Database integration tests require a configured test database.

## Pipeline Execution

The intended execution sequence is:

1. Read records from the configured CSV file or REST API.
2. Validate input fields and convert values to expected types.
3. Transform and normalize valid records.
4. Separate invalid records and capture their validation errors.
5. Load valid records into PostgreSQL in batches.
6. Record run metadata, row counts, failures, and processing duration.
7. Generate a summary report.

A command-line entry point will be documented here once implemented.

## Reliability and Data Quality

The project is designed to address common ingestion failures:

- Missing or malformed input fields.
- Duplicate records and repeated pipeline executions.
- API timeouts and transient HTTP errors.
- Invalid dates and inconsistent data types.
- Database errors during batch loading.
- Partial processing and failed pipeline runs.

Database constraints, transactional writes, bounded retries, and idempotent upserts should be used where appropriate. Retries should distinguish transient failures from permanent validation errors.

## Testing Strategy

The test suite should cover:

- CSV parsing and malformed input.
- REST API responses, timeouts, and retry behavior.
- Schema validation and invalid-record quarantine.
- Transformation correctness and deduplication.
- Database inserts and upserts.
- Idempotent reruns.
- Transaction rollback and pipeline failure handling.
- End-to-end execution against a test database.

## Continuous Integration

GitHub Actions will automate:

- Dependency installation.
- Code linting and formatting checks.
- Unit tests.
- Database integration tests where configured.
- Build and configuration validation.

The CI workflow should fail when required checks fail.

## Roadmap

- [ ] Implement CSV ingestion.
- [ ] Implement REST API ingestion with HTTPX.
- [ ] Add Pydantic schemas and validation rules.
- [ ] Implement cleaning and transformation functions.
- [ ] Add PostgreSQL models and database configuration.
- [ ] Implement batch inserts and idempotent upserts.
- [ ] Add invalid-record quarantine and run history.
- [ ] Implement retry and timeout policies.
- [ ] Add unit and integration tests.
- [ ] Configure GitHub Actions CI.
- [ ] Add benchmark results and sample data-quality reports.
- [ ] Publish a reproducible end-to-end demonstration.

## Engineering Principles

DataForge follows these principles:

- Separation of concerns and modular design.
- Explicit schema validation.
- Deterministic and testable transformations.
- Database integrity and transactional consistency.
- Idempotent data loading.
- Observable pipeline execution.
- Secure configuration and credential management.

