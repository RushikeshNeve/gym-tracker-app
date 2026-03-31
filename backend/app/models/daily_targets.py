from __future__ import annotations

from datetime import date

from sqlalchemy import Date, Float, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base, TimestampMixin


class DailyTarget(TimestampMixin, Base):
    __tablename__ = "daily_targets"
    __table_args__ = (UniqueConstraint("profile_id", "date", name="uq_daily_targets_profile_date"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("user_profile.id", ondelete="CASCADE"), index=True)
    date: Mapped[date] = mapped_column(Date, index=True)
    calorie_target: Mapped[float] = mapped_column(Float, default=2200)
    protein_target: Mapped[float] = mapped_column(Float, default=180)
    carbs_target: Mapped[float] = mapped_column(Float, default=200)
    fats_target: Mapped[float] = mapped_column(Float, default=70)
    fiber_target: Mapped[float] = mapped_column(Float, default=30)
    water_target_liters: Mapped[float] = mapped_column(Float, default=4.0)

    profile = relationship("UserProfile", back_populates="daily_targets")

