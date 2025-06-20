# db.py
from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
DEBUG_MODE = os.getenv("DEBUG", "false").lower() == "true"

# Create the SQLModel engine
engine = create_engine(DATABASE_URL, echo=DEBUG_MODE)


def init_db():
    """
    Initialize the database by creating all tables.
    Call this once on application startup.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Dependency for FastAPI endpoints.
    Yields a database session and closes it after use.
    """
    with Session(engine) as session:
        yield session
