from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.diet_plan_templates import DietPlanTemplate
from app.models.recipe_library import RecipeLibrary


def list_recipes(db: Session, meal_type: str | None = None) -> list[RecipeLibrary]:
    statement = select(RecipeLibrary).order_by(RecipeLibrary.meal_type.asc(), RecipeLibrary.recipe_name.asc())
    if meal_type:
        statement = statement.where(RecipeLibrary.meal_type == meal_type)
    return list(db.scalars(statement).all())


def get_recipe_by_name(db: Session, recipe_name: str) -> RecipeLibrary | None:
    return db.scalar(select(RecipeLibrary).where(RecipeLibrary.recipe_name == recipe_name))


def get_meal_plan_for_date(db: Session, target_date: date) -> list[DietPlanTemplate]:
    return list(
        db.scalars(
            select(DietPlanTemplate)
            .where(DietPlanTemplate.day_name == target_date.strftime("%A"))
            .order_by(DietPlanTemplate.id.asc())
        ).all()
    )
