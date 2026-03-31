from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_profile
from app.db.session import get_db
from app.schemas.challenge import ChallengeDayRead, ChallengeDayUpsert, TodaySummary
from app.services.challenge_service import get_today_summary, upsert_manual_challenge_day


router = APIRouter(prefix="/today", tags=["today"])


@router.get("", response_model=TodaySummary)
def read_today(db: Session = Depends(get_db), profile=Depends(get_profile)) -> TodaySummary:
    summary = get_today_summary(db, profile)
    return TodaySummary(**{**summary, "challenge_day": ChallengeDayRead.model_validate(summary["challenge_day"])})


@router.put("/{log_date}", response_model=ChallengeDayRead)
def update_today(
    log_date: str,
    payload: ChallengeDayUpsert,
    db: Session = Depends(get_db),
    profile=Depends(get_profile),
) -> ChallengeDayRead:
    data = payload.model_dump()
    data["date"] = date.fromisoformat(log_date)
    updated = upsert_manual_challenge_day(db, profile, data)
    db.refresh(updated)
    return ChallengeDayRead.model_validate(updated)
