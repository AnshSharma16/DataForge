from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.loading.models import Customer


def upsert_customers(session: Session, records: list[dict]) -> None:
    """Insert customers or update existing customers by email."""
    if not records:
        return

    statement = insert(Customer).values(records)
    statement = statement.on_conflict_do_update(
        index_elements=[Customer.email],
        set_={
            "name": statement.excluded.name,
            "age": statement.excluded.age,
        },
    )

    session.execute(statement)
