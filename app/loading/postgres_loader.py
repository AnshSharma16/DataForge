import pandas as pd
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.loading.models import Customer


def load_customers(
    dataframe: pd.DataFrame,
    session: Session,
) -> int:
    """Insert customers or update existing records by email."""
    if dataframe.empty:
        return 0

    records = dataframe[["id", "name", "email", "age"]].to_dict(
        orient="records"
    )

    statement = insert(Customer).values(records)
    statement = statement.on_conflict_do_update(
        index_elements=["email"],
        set_={
            "name": statement.excluded.name,
            "age": statement.excluded.age,
        },
    )

    try:
        session.execute(statement)
        session.commit()
    except Exception:
        session.rollback()
        raise

    return len(records)
