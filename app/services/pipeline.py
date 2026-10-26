import logging
from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

from app.ingestion.csv_reader import read_csv_file
from app.loading.postgres_loader import load_customers
from app.reporting.invalid_records import save_invalid_records
from app.reporting.metrics import calculate_metrics
from app.transformations.cleaning import clean_records
from app.validation.validator import validate_records

logger = logging.getLogger(__name__)


def run_pipeline(
    file_path: str | Path,
    session: Session | None = None,
) -> tuple[pd.DataFrame, list[dict]]:
    """Ingest a CSV file and separate valid and invalid records."""
    dataframe = read_csv_file(file_path)

    cleaned_dataframe = clean_records(dataframe)

    valid_records, invalid_records = validate_records(cleaned_dataframe)
    save_invalid_records(invalid_records)

    metrics = calculate_metrics(
        total_records=len(dataframe),
        valid_records=len(valid_records),
        invalid_records=len(invalid_records),
    )

    if session is not None:
        loaded_count = load_customers(valid_records, session)
        metrics["loaded_records"] = loaded_count

    logger.info("Pipeline metrics: %s", metrics)

    return valid_records, invalid_records
