from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_profile
from app.db.session import get_db
from app.schemas.common import MessageResponse
from app.schemas.nutrition import NutritionDailySummary, NutritionLogCreate, NutritionLogRead, NutritionLogUpdate
from app.services.nutrition_service import copy_nutrition_logs, create_nutrition_log, delete_nutrition_log, get_daily_nutrition, update_nutrition_log


router = APIRouter(prefix="/nutrition", tags=["nutrition"])


@router.get("/{log_date}", response_model=NutritionDailySummary)
def read_daily_nutrition(log_date: str, db: Session = Depends(get_db), profile=Depends(get_profile)) -> NutritionDailySummary:
    data = get_daily_nutrition(db, profile, date.fromisoformat(log_date))
    return NutritionDailySummary(
        date=data["date"],
        totals=data["totals"],
        remaining=data["remaining"],
        targets=data["targets"],
        meals=[NutritionLogRead.model_validate(item) for item in data["meals"]],
        compliance_inputs=data["compliance_inputs"],
    )


@router.post("", response_model=NutritionLogRead)
def create_nutrition_route(payload: NutritionLogCreate, db: Session = Depends(get_db), profile=Depends(get_profile)) -> NutritionLogRead:
    return NutritionLogRead.model_validate(create_nutrition_log(db, profile, payload))


@router.patch("/{log_id}", response_model=NutritionLogRead)
def update_nutrition_route(log_id: int, payload: NutritionLogUpdate, db: Session = Depends(get_db), profile=Depends(get_profile)) -> NutritionLogRead:
    item = update_nutrition_log(db, profile, log_id, payload)
    if item is None:
        raise HTTPException(status_code=404, detail="Nutrition log not found")
    return NutritionLogRead.model_validate(item)


@router.delete("/{log_id}", response_model=MessageResponse)
def delete_nutrition_route(log_id: int, db: Session = Depends(get_db), profile=Depends(get_profile)) -> MessageResponse:
    if not delete_nutrition_log(db, profile, log_id):
        raise HTTPException(status_code=404, detail="Nutrition log not found")
    return MessageResponse(message="Nutrition log deleted")


@router.post("/duplicate", response_model=MessageResponse)
def duplicate_meals(source_date: str, target_date: str, db: Session = Depends(get_db), profile=Depends(get_profile)) -> MessageResponse:
    copied = copy_nutrition_logs(db, profile, date.fromisoformat(source_date), date.fromisoformat(target_date))
    return MessageResponse(message=f"Copied {copied} meals")

