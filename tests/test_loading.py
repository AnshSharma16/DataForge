from unittest.mock import MagicMock

import pandas as pd
import pytest

from app.loading.postgres_loader import load_customers


def sample_dataframe():
    return pd.DataFrame(
        [
            {
                "id": 1,
                "name": "Aarav",
                "email": "aarav@example.com",
                "age": 24,
            }
        ]
    )


def test_empty_dataframe_returns_zero():
    session = MagicMock()

    result = load_customers(
        pd.DataFrame(columns=["id", "name", "email", "age"]),
        session,
    )

    assert result == 0
    session.commit.assert_not_called()
    session.rollback.assert_not_called()


def test_load_customers_commits_successfully():
    session = MagicMock()

    result = load_customers(sample_dataframe(), session)

    assert result == 1
    session.commit.assert_called_once()
    session.rollback.assert_not_called()


def test_load_customers_rolls_back_on_failure(monkeypatch):
    session = MagicMock()

    def fail_upsert(session_arg, records):
        raise RuntimeError("Database failure")

    monkeypatch.setattr(
        "app.loading.postgres_loader.upsert_customers",
        fail_upsert,
    )

    with pytest.raises(RuntimeError, match="Database failure"):
        load_customers(sample_dataframe(), session)

    session.rollback.assert_called_once()
    session.commit.assert_not_called()
