from __future__ import annotations

from datetime import date

from sqlalchemy import Date, Float, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base, TimestampMixin


class BodyMetric(TimestampMixin, Base):
    __tablename__ = "body_metrics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("user_profile.id", ondelete="CASCADE"), index=True)
    date: Mapped[date] = mapped_column(Date, index=True)
    body_weight: Mapped[float | None] = mapped_column(Float)
    waist: Mapped[float | None] = mapped_column(Float)
    chest: Mapped[float | None] = mapped_column(Float)
    arms: Mapped[float | None] = mapped_column(Float)
    thigh: Mapped[float | None] = mapped_column(Float)
    body_fat_percent: Mapped[float | None] = mapped_column(Float)
    notes: Mapped[str] = mapped_column(Text, default="")
    hips: Mapped[float | None] = mapped_column(Float)
    neck: Mapped[float | None] = mapped_column(Float)
    thighs: Mapped[float | None] = mapped_column(Float)
    progress_notes: Mapped[str] = mapped_column(Text, default="")

    profile = relationship("UserProfile", back_populates="body_metrics")

