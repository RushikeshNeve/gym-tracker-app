from __future__ import annotations

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base, TimestampMixin


class DietPlanTemplate(TimestampMixin, Base):
    __tablename__ = "diet_plan_templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    day_name: Mapped[str] = mapped_column(String(16), index=True)
    meal_type: Mapped[str] = mapped_column(String(64), index=True)
    option_1: Mapped[str | None] = mapped_column(String(255))
    option_2: Mapped[str | None] = mapped_column(String(255))
    option_3: Mapped[str | None] = mapped_column(String(255))
    option_4: Mapped[str | None] = mapped_column(String(255))
    notes: Mapped[str] = mapped_column(Text, default="")

