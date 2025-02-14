import uuid
from typing import Optional

from datetime import datetime, timezone
from sqlmodel import Field, SQLModel


class BaseModel(SQLModel, table=False):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex, primary_key=True)


class DateTimeModel(SQLModel, table=False):
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
