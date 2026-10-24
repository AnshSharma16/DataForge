import pandas as pd

from app.transformations.cleaning import clean_records


def test_clean_records_trims_whitespace():
    dataframe = pd.DataFrame(
        {
            "name": ["  Aarav  "],
            "email": ["  AARAV@EXAMPLE.COM  "],
        }
    )

    cleaned = clean_records(dataframe)

    assert cleaned.iloc[0]["name"] == "Aarav"
    assert cleaned.iloc[0]["email"] == "aarav@example.com"


def test_clean_records_preserves_original():
    dataframe = pd.DataFrame({"name": ["  Meera  "]})

    clean_records(dataframe)

    assert dataframe.iloc[0]["name"] == "  Meera  "


def test_clean_records_handles_missing_email_column():
    dataframe = pd.DataFrame({"name": ["  Rohan  "]})

    cleaned = clean_records(dataframe)

    assert cleaned.iloc[0]["name"] == "Rohan"
