# models.py
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB

class Conversation(SQLModel, table=True):
    """
    Stores an ideation conversation snapshot.

    Fields:
      - id: Auto-increment primary key
      - name: User-defined session name
      - summary: 1–2 sentence project summary
      - context: Enriched context text
      - draft: Full requirements JSON blob
      - created_at: Timestamp of creation
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    summary: str
    context: str
    draft: dict = Field(sa_column=Column(JSONB, nullable=False))
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        # Allow ORM mode for SQLModel
        orm_mode = True