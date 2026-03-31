from __future__ import annotations

from datetime import date

from sqlalchemy import Date, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base, TimestampMixin


class CardioLog(TimestampMixin, Base):
    __tablename__ = "cardio_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("user_profile.id", ondelete="CASCADE"), index=True)
    date: Mapped[date] = mapped_column(Date, index=True)
    cardio_type: Mapped[str] = mapped_column(String(128))
    duration_min: Mapped[int] = mapped_column(Integer)
    calories: Mapped[int | None] = mapped_column(Integer)
    intensity: Mapped[str | None] = mapped_column(String(32))
    notes: Mapped[str] = mapped_column(Text, default="")
    is_outdoor: Mapped[bool] = mapped_column(default=False)
    distance_km: Mapped[float] = mapped_column(Float, default=0.0)
    pace_text: Mapped[str] = mapped_column(String(64), default="")
    estimated_calories_burned: Mapped[float] = mapped_column(Float, default=0.0)

    profile = relationship("UserProfile", back_populates="cardio_logs")

