import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    sessionmaker,
)


# Use a local SQLite file by default.
# DATABASE_URL can later point to another database, such as PostgreSQL.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./5g_core.db")


# SQLite normally restricts a connection to one thread.
# FastAPI can handle requests across multiple threads, so this must be disabled.
connect_args = (
    {"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {}
)


# The engine manages connections between SQLAlchemy and the database.
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
)


# SessionLocal is a factory that creates database sessions.
# A session is used to read, create, update, and delete database records.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


# Every SQLAlchemy database model inherits from this base class.
class Base(DeclarativeBase):
    pass


# This Python class represents the subscriptions database table.
class SubscriptionRecord(Base):
    __tablename__ = "subscriptions"

    # Tell SQLite never to reuse previously generated numeric IDs.
    __table_args__ = {"sqlite_autoincrement": True}

    # Internal database ID. SQLite generates 1, 2, 3, and so on.
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    # Information supplied when a subscription is created.
    ue_id: Mapped[str]
    event_type: Mapped[str]
    callback_url: Mapped[str]

    # New subscriptions are active unless another status is provided.
    status: Mapped[str] = mapped_column(default="active")


# Create any database tables that do not already exist.
# Existing tables and records are not deleted.
def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


# Give each API request its own database session.
# The with block automatically closes the session after the request finishes.
def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session