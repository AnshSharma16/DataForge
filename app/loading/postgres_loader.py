import pandas as pd
from sqlalchemy.orm import Session

from app.loading.repositories.customer_repository import upsert_customers


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

    try:
        upsert_customers(session, records)
        session.commit()
    except Exception:
        session.rollback()
        raise

    return len(records)
