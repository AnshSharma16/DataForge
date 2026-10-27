from unittest.mock import MagicMock

import pandas as pd
import pytest
from sqlalchemy import create_engine

from app.loading.database import (
    create_database_engine,
    create_session_factory,
    create_tables,
)
from app.loading.models import Base
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


def test_create_session_factory():
    engine = create_engine("sqlite:///:memory:")

    try:
        session_factory = create_session_factory(engine)

        assert session_factory.kw["bind"] is engine
        assert session_factory.kw["autoflush"] is False
        assert session_factory.kw["expire_on_commit"] is False
    finally:
        engine.dispose()


def test_create_tables():
    engine = create_engine("sqlite:///:memory:")

    try:
        create_tables(engine)

        assert "customers" in Base.metadata.tables

        from sqlalchemy import inspect

        assert inspect(engine).has_table("customers")
    finally:
        engine.dispose()


def test_create_database_engine(monkeypatch):
    monkeypatch.setattr(
        "app.loading.database.get_database_url",
        lambda: "sqlite:///:memory:",
    )

    engine = create_database_engine()

    try:
        assert engine.pool._pre_ping is True
        with engine.connect() as connection:
            assert connection.exec_driver_sql("SELECT 1").scalar() == 1
    finally:
        engine.dispose()



