from __future__ import annotations

from datetime import date

from sqlalchemy import Date, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base, TimestampMixin


class ChallengeDay(TimestampMixin, Base):
    __tablename__ = "challenge_days"
    __table_args__ = (UniqueConstraint("profile_id", "date", name="uq_challenge_days_profile_date"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("user_profile.id", ondelete="CASCADE"), index=True)
    date: Mapped[date] = mapped_column(Date, index=True)
    challenge_day_number: Mapped[int | None] = mapped_column(Integer)
    workout_1_completed: Mapped[bool] = mapped_column(default=False)
    workout_2_completed: Mapped[bool] = mapped_column(default=False)
    one_workout_outdoors: Mapped[bool] = mapped_column(default=False)
    followed_diet: Mapped[bool] = mapped_column(default=False)
    no_cheat_meals: Mapped[bool] = mapped_column(default=True)
    no_alcohol: Mapped[bool] = mapped_column(default=True)
    water_goal_completed: Mapped[bool] = mapped_column(default=False)
    progress_picture_taken: Mapped[bool] = mapped_column(default=False)
    body_weight: Mapped[float | None] = mapped_column(Float)
    steps: Mapped[int] = mapped_column(Integer, default=0)
    sleep_hours: Mapped[float] = mapped_column(Float, default=0.0)
    mood: Mapped[str] = mapped_column(String(120), default="")
    energy_level: Mapped[int] = mapped_column(Integer, default=0)
    notes: Mapped[str] = mapped_column(Text, default="")
    selected_diet_plan: Mapped[str] = mapped_column(String(255), default="")
    diet_followed: Mapped[bool] = mapped_column(default=False)
    cheat_meal: Mapped[bool] = mapped_column(default=False)
    junk_food: Mapped[bool] = mapped_column(default=False)
    sugary_drinks: Mapped[bool] = mapped_column(default=False)
    hunger_level: Mapped[int] = mapped_column(Integer, default=0)
    cravings_level: Mapped[int] = mapped_column(Integer, default=0)
    binge_urge: Mapped[int] = mapped_column(Integer, default=0)
    diet_notes: Mapped[str] = mapped_column(Text, default="")
    day_status: Mapped[str] = mapped_column(String(32), default="incomplete")
    compliance_score: Mapped[float] = mapped_column(Float, default=0.0)

    profile = relationship("UserProfile", back_populates="challenge_days")

