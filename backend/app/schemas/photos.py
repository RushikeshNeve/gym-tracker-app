from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field

from app.schemas.common import TimestampFields


class ProgressPhotoCreate(BaseModel):
    date: date
    photo_type: str = Field(default="front")
    file_url: str
    blob_key: str | None = None
    notes: str = ""


class ProgressPhotoRead(ProgressPhotoCreate, TimestampFields):
    id: int
    profile_id: int

