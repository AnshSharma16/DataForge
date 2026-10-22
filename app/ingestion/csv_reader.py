from pathlib import Path

import pandas as pd


class CSVIngestionError(Exception):
    """Raised when a CSV file cannot be ingested."""


def read_csv_file(file_path: str | Path) -> pd.DataFrame:
    """Read a CSV file and return its contents as a DataFrame."""
    path = Path(file_path)

    if not path.exists():
        raise CSVIngestionError(f"CSV file does not exist: {path}")

    if not path.is_file():
        raise CSVIngestionError(f"Path is not a file: {path}")

    if path.suffix.lower() != ".csv":
        raise CSVIngestionError(
            f"Expected a CSV file, received: {path.suffix}"
        )

    try:
        return pd.read_csv(path)
    except (
        pd.errors.ParserError,
        UnicodeDecodeError,
        OSError,
    ) as exc:
        raise CSVIngestionError(
            f"Failed to read CSV file: {path}"
        ) from exc
