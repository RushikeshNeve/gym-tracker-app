from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.recipes import MealPlanTemplateRead
from app.services.recipe_service import get_meal_plan_for_date


router = APIRouter(prefix="/meal-plans", tags=["meal-plans"])


@router.get("/{target_date}", response_model=list[MealPlanTemplateRead])
def read_meal_plan(target_date: str, db: Session = Depends(get_db)) -> list[MealPlanTemplateRead]:
    return [MealPlanTemplateRead.model_validate(item) for item in get_meal_plan_for_date(db, date.fromisoformat(target_date))]

