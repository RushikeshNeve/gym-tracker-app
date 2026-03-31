from __future__ import annotations

from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base, TimestampMixin


class WeeklyReview(TimestampMixin, Base):
    __tablename__ = "weekly_reviews"
    __table_args__ = (UniqueConstraint("profile_id", "week_start", name="uq_weekly_reviews_profile_week"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("user_profile.id", ondelete="CASCADE"), index=True)
    week_start: Mapped[date] = mapped_column(Date, index=True)
    what_went_well: Mapped[str] = mapped_column(Text, default="")
    what_was_difficult: Mapped[str] = mapped_column(Text, default="")
    focus_for_next_week: Mapped[str] = mapped_column(Text, default="")
    notes: Mapped[str] = mapped_column(Text, default="")

    profile = relationship("UserProfile", back_populates="weekly_reviews")

