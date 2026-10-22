
import pandas as pd


def clean_records(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Trim text fields and normalize email addresses."""
    cleaned = dataframe.copy()

    for column in cleaned.select_dtypes(include=["object", "string"]):
        cleaned[column] = cleaned[column].map(
            lambda value: value.strip() if isinstance(value, str) else value
        )

    if "email" in cleaned.columns:
        cleaned["email"] = cleaned["email"].map(
            lambda value: value.lower() if isinstance(value, str) else value
        )

    return cleaned
