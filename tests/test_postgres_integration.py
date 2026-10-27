import os
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.config import get_database_url
from app.loading.models import Base, Customer
from app.loading.repositories.customer_repository import upsert_customers

DATABASE_URL = os.getenv("DATABASE_URL")

pytestmark = pytest.mark.skipif(
    not DATABASE_URL,
    reason="DATABASE_URL is not configured",
)


@pytest.fixture
def db_session():
    engine = create_engine(get_database_url())

    try:
        Base.metadata.create_all(engine)

        with Session(engine) as session:
            yield session
            session.rollback()
    finally:
        engine.dispose()


def test_postgres_upsert_inserts_and_updates_customer(db_session):
    email = f"dataforge-{uuid4().hex}@example.com"

    try:
        upsert_customers(
            db_session,
            [
                {
                    "id": 900001,
                    "name": "DataForge Test",
                    "email": email,
                    "age": 25,
                }
            ],
        )
        db_session.commit()

        customer = db_session.scalar(
            select(Customer).where(Customer.email == email)
        )
        assert customer is not None
        assert customer.name == "DataForge Test"
        assert customer.age == 25

        upsert_customers(
            db_session,
            [
                {
                    "id": 900001,
                    "name": "DataForge Updated",
                    "email": email,
                    "age": 26,
                }
            ],
        )
        db_session.commit()

        customer = db_session.scalar(
            select(Customer).where(Customer.email == email)
        )
        assert customer is not None
        assert customer.name == "DataForge Updated"
        assert customer.age == 26

    finally:
        db_session.rollback()
        db_session.query(Customer).filter_by(email=email).delete()
        db_session.commit()

