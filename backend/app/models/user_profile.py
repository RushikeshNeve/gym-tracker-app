from __future__ import annotations

from datetime import date

from sqlalchemy import Date, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base, TimestampMixin


class UserProfile(TimestampMixin, Base):
    __tablename__ = "user_profile"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    age: Mapped[int | None] = mapped_column(Integer)
    gender: Mapped[str | None] = mapped_column(String(20))
    height_cm: Mapped[float | None] = mapped_column(Float)
    current_weight_kg: Mapped[float | None] = mapped_column(Float)
    activity_level: Mapped[str | None] = mapped_column(String(32))
    goal: Mapped[str | None] = mapped_column(String(32))
    desired_deficit: Mapped[float | None] = mapped_column(Float)
    challenge_start_date: Mapped[date | None] = mapped_column(Date)
    target_weight_kg: Mapped[float | None] = mapped_column(Float)
    preferred_diet_plan_name: Mapped[str | None] = mapped_column(String(255))

    challenge_days = relationship("ChallengeDay", back_populates="profile", cascade="all, delete-orphan")
    daily_targets = relationship("DailyTarget", back_populates="profile", cascade="all, delete-orphan")
    workouts = relationship("Workout", back_populates="profile", cascade="all, delete-orphan")
    cardio_logs = relationship("CardioLog", back_populates="profile", cascade="all, delete-orphan")
    body_metrics = relationship("BodyMetric", back_populates="profile", cascade="all, delete-orphan")
    nutrition_logs = relationship("NutritionLog", back_populates="profile", cascade="all, delete-orphan")
    hydration_logs = relationship("HydrationLog", back_populates="profile", cascade="all, delete-orphan")
    progress_photos = relationship("ProgressPhoto", back_populates="profile", cascade="all, delete-orphan")
    weekly_reviews = relationship("WeeklyReview", back_populates="profile", cascade="all, delete-orphan")

