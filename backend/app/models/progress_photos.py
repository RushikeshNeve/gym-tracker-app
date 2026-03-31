from __future__ import annotations

from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base, TimestampMixin


class ProgressPhoto(TimestampMixin, Base):
    __tablename__ = "progress_photos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("user_profile.id", ondelete="CASCADE"), index=True)
    date: Mapped[date] = mapped_column(Date, index=True)
    photo_type: Mapped[str] = mapped_column(String(32), default="front")
    file_url: Mapped[str] = mapped_column(String(1024))
    blob_key: Mapped[str | None] = mapped_column(String(512))
    notes: Mapped[str] = mapped_column(Text, default="")

    profile = relationship("UserProfile", back_populates="progress_photos")

