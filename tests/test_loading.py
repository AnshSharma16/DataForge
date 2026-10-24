from unittest.mock import MagicMock

import pandas as pd

from app.loading.postgres_loader import load_customers


def test_empty_dataframe_returns_zero():
    session = MagicMock()
    dataframe = pd.DataFrame(columns=["id", "name", "email", "age"])

    result = load_customers(dataframe, session)

    assert result == 0
    session.execute.assert_not_called()
    session.commit.assert_not_called()


def test_load_customers_executes_upsert():
    session = MagicMock()
    dataframe = pd.DataFrame(
        [
            {
                "id": 1,
                "name": "Aarav",
                "email": "aarav@example.com",
                "age": 24,
            }
        ]
    )

    result = load_customers(dataframe, session)

    assert result == 1
    session.execute.assert_called_once()
    session.commit.assert_called_once()
    session.rollback.assert_not_called()


def test_load_customers_rolls_back_on_failure():
    session = MagicMock()
    session.execute.side_effect = RuntimeError("Database failure")
    dataframe = pd.DataFrame(
        [
            {
                "id": 1,
                "name": "Aarav",
                "email": "aarav@example.com",
                "age": 24,
            }
        ]
    )

    try:
        load_customers(dataframe, session)
    except RuntimeError as exc:
        assert str(exc) == "Database failure"
    else:
        raise AssertionError("Expected database failure")

    session.rollback.assert_called_once()
    session.commit.assert_not_called()
