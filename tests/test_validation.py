import pandas as pd
import pytest

from app.validation.validator import validate_records


def test_valid_records_pass():
    df = pd.DataFrame([
        {
            "id": 1,
            "name": "Aarav",
            "email": "aarav@example.com",
            "age": 24,
        }
    ])

    valid, invalid = validate_records(df)

    assert len(valid) == 1
    assert invalid == []


def test_invalid_email_is_rejected():
    df = pd.DataFrame([
        {
            "id": 1,
            "name": "Aarav",
            "email": "invalid",
            "age": 24,
        }
    ])

    valid, invalid = validate_records(df)

    assert valid.empty
    assert len(invalid) == 1
    assert invalid[0]["row_number"] == 2


def test_missing_column_raises_error():
    df = pd.DataFrame([{"id": 1, "name": "Aarav"}])

    with pytest.raises(ValueError, match="Missing required columns"):
        validate_records(df)


def test_invalid_age_is_rejected():
    df = pd.DataFrame([
        {
            "id": 1,
            "name": "Aarav",
            "email": "aarav@example.com",
            "age": 150,
        }
    ])

    valid, invalid = validate_records(df)

    assert valid.empty
    assert len(invalid) == 1
