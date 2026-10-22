from pathlib import Path

import pandas as pd

from app.ingestion.csv_reader import read_csv_file
from app.validation.validator import validate_records


def run_pipeline(
    file_path: str | Path,
) -> tuple[pd.DataFrame, list[dict]]:
    """Ingest a CSV file and separate valid and invalid records."""
    dataframe = read_csv_file(file_path)
    valid_records, invalid_records = validate_records(dataframe)

    return valid_records, invalid_records
