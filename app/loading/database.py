from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import get_database_url
from app.loading.models import Base


def create_database_engine():
    """Create a SQLAlchemy engine from the configured database URL."""
    return create_engine(
        get_database_url(),
        pool_pre_ping=True,
    )


def create_session_factory(engine):
    """Create a factory for database sessions."""
    return sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )


def create_tables(engine) -> None:
    """Create all registered tables if they do not exist."""
    Base.metadata.create_all(engine)
