from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_profile
from app.db.session import get_db
from app.schemas.profile import ProfileWithSummary, UserProfileRead, UserProfileUpdate
from app.schemas.targets import DailyTargetRead, DailyTargetUpsert
from app.services.profile_service import get_or_create_daily_target, get_profile_summary, update_profile, upsert_daily_target


router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=ProfileWithSummary)
def read_profile(profile=Depends(get_profile)) -> ProfileWithSummary:
    return ProfileWithSummary(profile=UserProfileRead.model_validate(profile), summary=get_profile_summary(profile))


@router.put("", response_model=ProfileWithSummary)
def update_profile_route(payload: UserProfileUpdate, db: Session = Depends(get_db), profile=Depends(get_profile)) -> ProfileWithSummary:
    updated = update_profile(db, profile, payload)
    return ProfileWithSummary(profile=UserProfileRead.model_validate(updated), summary=get_profile_summary(updated))


@router.get("/targets/{target_date}", response_model=DailyTargetRead)
def read_daily_target(target_date: str, db: Session = Depends(get_db), profile=Depends(get_profile)) -> DailyTargetRead:
    return DailyTargetRead.model_validate(get_or_create_daily_target(db, profile, date.fromisoformat(target_date)))


@router.put("/targets/{target_date}", response_model=DailyTargetRead)
def upsert_daily_target_route(
    target_date: str,
    payload: DailyTargetUpsert,
    db: Session = Depends(get_db),
    profile=Depends(get_profile),
) -> DailyTargetRead:
    data = payload.model_dump()
    data["date"] = date.fromisoformat(target_date)
    return DailyTargetRead.model_validate(upsert_daily_target(db, profile, data))

