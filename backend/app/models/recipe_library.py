from __future__ import annotations

from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base, TimestampMixin


class RecipeLibrary(TimestampMixin, Base):
    __tablename__ = "recipe_library"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recipe_name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    meal_type: Mapped[str] = mapped_column(String(64), index=True)
    ingredients_json: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    steps_json: Mapped[list[str]] = mapped_column(JSONB, default=list)
    calories: Mapped[float] = mapped_column(Float, default=0.0)
    protein: Mapped[float] = mapped_column(Float, default=0.0)
    carbs: Mapped[float] = mapped_column(Float, default=0.0)
    fats: Mapped[float] = mapped_column(Float, default=0.0)
    fiber: Mapped[float] = mapped_column(Float, default=0.0)
    portion_note: Mapped[str] = mapped_column(String(255), default="")
    is_spicy: Mapped[bool] = mapped_column(Boolean, default=False)
    is_vegetarian: Mapped[bool] = mapped_column(Boolean, default=False)
    is_egg_based: Mapped[bool] = mapped_column(Boolean, default=False)
    is_soya_based: Mapped[bool] = mapped_column(Boolean, default=False)

