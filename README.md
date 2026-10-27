# DataForge — Data Ingestion & Validation Pipeline

DataForge is a modular Python ETL pipeline that ingests CSV data, cleans and validates records, separates invalid records for investigation, calculates data-quality metrics, and optionally loads valid customer records into PostgreSQL.

The project demonstrates practical data engineering techniques, including schema validation, transactional database loading, conflict-aware upserts, structured logging, and automated testing.

## Key Features

- **CSV ingestion:** Read structured records from CSV files using Pandas.
- **Data cleaning:** Trim whitespace and normalize email addresses.
- **Schema validation:** Validate customer records using Pydantic, including field constraints and email validation.
- **Invalid-record reporting:** Save invalid records and their validation errors to a CSV report.
- **PostgreSQL loading:** Load valid customer records using SQLAlchemy.
- **Conflict-aware upserts:** Insert new customers and update existing records based on email conflicts.
- **Transaction handling:** Commit successful loads and roll back failed operations.
- **Pipeline metrics:** Calculate total, valid, and invalid record counts and the validation success rate.
- **Automated tests:** Test ingestion, transformations, validation, loading, reporting, pipeline behavior, and database integration.

## Architecture

```text
CSV File
   |
   v
CSV Ingestion
   |
   v
Data Cleaning
   |
   v
Pydantic Validation
   |
   +--------------------+
   |                    |
   v                    v
Valid Records      Invalid Records
   |                    |
   |                    v
   |             Invalid-record CSV
   |
   +---- If a database session is provided
   |
   v
PostgreSQL Upsert
   |
   v
Pipeline Metrics & Logs
```

The pipeline can also run without a database session. In that mode, it returns valid and invalid records and writes the invalid-record report without loading customers into PostgreSQL.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Pipeline implementation |
| Pandas | CSV and tabular data processing |
| Pydantic | Schema validation |
| SQLAlchemy 2.x | Database access and ORM |
| PostgreSQL | Persistent customer storage |
| Psycopg | PostgreSQL driver |
| pytest | Automated testing |
| pytest-cov | Test coverage reporting |
| Ruff | Linting and import checks |
| GitHub Actions | Continuous integration workflow |

## Project Structure

```text
DataForge/
├── app/
│   ├── config.py
│   ├── ingestion/
│   │   ├── api_client.py
│   │   ├── base.py
│   │   └── csv_reader.py
│   ├── loading/
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── postgres_loader.py
│   │   └── repositories/
│   │       └── customer_repository.py
│   ├── reporting/
│   │   ├── invalid_records.py
│   │   └── metrics.py
│   ├── services/
│   │   └── pipeline.py
│   ├── transformations/
│   │   └── cleaning.py
│   ├── validation/
│   │   ├── schemas.py
│   │   └── validator.py
│   ├── utils/
│   │   └── logging.py
│   └── main.py
├── data/
│   └── sample.csv
├── reports/
├── tests/
│   ├── test_ingestion.py
│   ├── test_loading.py
│   ├── test_metrics.py
│   ├── test_pipeline.py
│   ├── test_postgres_integration.py
│   ├── test_reporting.py
│   ├── test_transformations.py
│   └── test_validation.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── .env.example
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.12 or later
- Git
- PostgreSQL for database integration testing and database-backed pipeline execution

The pipeline's CSV processing and unit tests can run without a live PostgreSQL database. PostgreSQL integration tests require a configured database.

### 1. Clone the repository

```bash
git clone https://github.com/AnshSharma16/DataForge.git
cd DataForge
```

### 2. Create and activate a virtual environment

Linux or macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create a local `.env` file using `.env.example` as a reference.

Set the database connection string:

```dotenv
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:5432/DATABASE
```

Replace the placeholders with your actual PostgreSQL credentials. Never commit `.env` or expose database credentials.

## Running the Pipeline

The pipeline is exposed through the `run_pipeline()` function in `app/services/pipeline.py`. There is currently no implemented command-line entry point.

Example invocation from the repository root:

```python
from app.services.pipeline import run_pipeline

valid_records, invalid_records = run_pipeline("data/sample.csv")

print(f"Valid records: {len(valid_records)}")
print(f"Invalid records: {len(invalid_records)}")
```

This processes the CSV, cleans and validates its records, saves invalid records to the report location, and returns the valid and invalid results.

### Loading records into PostgreSQL

To load valid records, create a database engine and session using the project's database helpers:

```python
from app.loading.database import (
    create_database_engine,
    create_session_factory,
)
from app.services.pipeline import run_pipeline

engine = create_database_engine()

try:
    session_factory = create_session_factory(engine)

    with session_factory() as session:
        valid_records, invalid_records = run_pipeline(
            "data/sample.csv",
            session=session,
        )
finally:
    engine.dispose()
```

The `customers` table must exist before loading. It can be created using the existing database helper:

```python
from app.loading.database import create_database_engine, create_tables

engine = create_database_engine()

try:
    create_tables(engine)
finally:
    engine.dispose()
```

Run these examples from the repository root after installing the dependencies and configuring the environment.

## Testing and Code Quality

Run the full test suite:

```bash
pytest -v
```

Run tests with coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

Check code quality with Ruff:

```bash
ruff check .
```

The latest recorded test run reported **25 passing tests and 97% overall coverage**. Results can change as the project evolves. PostgreSQL integration tests must be verified against a reachable database to confirm real database behavior.

## Current Scope and Future Improvements

The current implementation focuses on CSV-based customer ingestion, cleaning, validation, invalid-record reporting, metrics, logging, and optional PostgreSQL loading.

Potential future improvements include:

- Implement and test REST API ingestion.
- Add configurable retry policies for transient API failures.
- Introduce batch-size configuration for larger datasets.
- Add pipeline run-history persistence and processing-duration metrics.
- Expand tests for failure paths and database transaction behavior.
- Add a documented command-line entry point.
- Publish reproducible sample runs and data-quality reports.

## Engineering Principles

- Separation of concerns through modular components.
- Explicit schema validation and actionable error reporting.
- Deterministic data transformations.
- Transactional database writes.
- Conflict-aware, repeatable data loading.
- Secure environment-based configuration.
- Automated tests and code-quality checks.