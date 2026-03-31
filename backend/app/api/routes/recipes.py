from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.recipes import RecipeRead
from app.services.recipe_service import list_recipes


router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get("", response_model=list[RecipeRead])
def read_recipes(meal_type: str | None = None, db: Session = Depends(get_db)) -> list[RecipeRead]:
    return [RecipeRead.model_validate(item) for item in list_recipes(db, meal_type)]

