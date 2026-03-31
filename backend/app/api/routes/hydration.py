from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_profile
from app.db.session import get_db
from app.schemas.common import MessageResponse
from app.schemas.hydration import HydrationChartPoint, HydrationDailySummary, HydrationLogCreate, HydrationLogRead
from app.services.hydration_service import create_hydration_log, delete_hydration_log, get_daily_hydration, get_weekly_hydration


router = APIRouter(prefix="/hydration", tags=["hydration"])


@router.get("/weekly/{end_date}", response_model=list[HydrationChartPoint])
def read_weekly_hydration(end_date: str, db: Session = Depends(get_db), profile=Depends(get_profile)) -> list[HydrationChartPoint]:
    return [HydrationChartPoint(**item) for item in get_weekly_hydration(db, profile, date.fromisoformat(end_date))]


@router.get("/{log_date}", response_model=HydrationDailySummary)
def read_daily_hydration(log_date: str, db: Session = Depends(get_db), profile=Depends(get_profile)) -> HydrationDailySummary:
    data = get_daily_hydration(db, profile, date.fromisoformat(log_date))
    return HydrationDailySummary(
        date=data["date"],
        total_ml=data["total_ml"],
        target_ml=data["target_ml"],
        target_liters=data["target_liters"],
        remaining_ml=data["remaining_ml"],
        bottle_count=data["bottle_count"],
        progress_pct=data["progress_pct"],
        logs=[HydrationLogRead.model_validate(item) for item in data["logs"]],
    )


@router.post("", response_model=HydrationLogRead)
def create_hydration_route(payload: HydrationLogCreate, db: Session = Depends(get_db), profile=Depends(get_profile)) -> HydrationLogRead:
    return HydrationLogRead.model_validate(create_hydration_log(db, profile, payload))


@router.delete("/{log_id}", response_model=MessageResponse)
def delete_hydration_route(log_id: int, db: Session = Depends(get_db), profile=Depends(get_profile)) -> MessageResponse:
    if not delete_hydration_log(db, profile, log_id):
        raise HTTPException(status_code=404, detail="Hydration log not found")
    return MessageResponse(message="Hydration log deleted")
