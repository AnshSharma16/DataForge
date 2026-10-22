from pathlib import Path

import pandas as pd

from app.ingestion.csv_reader import read_csv_file
from app.reporting.invalid_records import save_invalid_records
from app.transformations.cleaning import clean_records
from app.validation.validator import validate_records


def run_pipeline(
    file_path: str | Path,
) -> tuple[pd.DataFrame, list[dict]]:
    """Ingest a CSV file and separate valid and invalid records."""
    dataframe = read_csv_file(file_path)
    cleaned_dataframe = clean_records(dataframe)
    valid_records, invalid_records = validate_records(cleaned_dataframe)

    save_invalid_records(invalid_records)

    return valid_records, invalid_records
