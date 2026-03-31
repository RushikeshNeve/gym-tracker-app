from __future__ import annotations

from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base, TimestampMixin


class ExerciseLibrary(TimestampMixin, Base):
    __tablename__ = "exercise_library"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    day_type: Mapped[str] = mapped_column(String(64), index=True)
    muscle_group: Mapped[str] = mapped_column(String(128), index=True)
    youtube_url: Mapped[str] = mapped_column(String(1024), default="")
    youtube_search_url: Mapped[str] = mapped_column(String(1024), default="")
    instructions_json: Mapped[list[str]] = mapped_column(JSONB, default=list)
    common_mistakes_json: Mapped[list[str]] = mapped_column(JSONB, default=list)
    tips: Mapped[str] = mapped_column(Text, default="")
    matched: Mapped[bool] = mapped_column(Boolean, default=False)

