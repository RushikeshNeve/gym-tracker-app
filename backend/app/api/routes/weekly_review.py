from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_profile
from app.db.session import get_db
from app.schemas.weekly_review import WeeklyReviewRead, WeeklyReviewSummary, WeeklyReviewUpsert
from app.services.weekly_review_service import get_weekly_review_record, get_weekly_summary, upsert_weekly_review


router = APIRouter(prefix="/weekly-review", tags=["weekly-review"])


@router.get("/{week_start}", response_model=WeeklyReviewSummary)
def read_weekly_summary(week_start: str, db: Session = Depends(get_db), profile=Depends(get_profile)) -> WeeklyReviewSummary:
    return WeeklyReviewSummary(**get_weekly_summary(db, profile, date.fromisoformat(week_start)))


@router.get("/{week_start}/record", response_model=WeeklyReviewRead | None)
def read_weekly_review_record(week_start: str, db: Session = Depends(get_db), profile=Depends(get_profile)) -> WeeklyReviewRead | None:
    item = get_weekly_review_record(db, profile, date.fromisoformat(week_start))
    return WeeklyReviewRead.model_validate(item) if item else None


@router.put("/{week_start}", response_model=WeeklyReviewRead)
def upsert_weekly_review_route(week_start: str, payload: WeeklyReviewUpsert, db: Session = Depends(get_db), profile=Depends(get_profile)) -> WeeklyReviewRead:
    item = upsert_weekly_review(db, profile, {**payload.model_dump(), "week_start": date.fromisoformat(week_start)})
    return WeeklyReviewRead.model_validate(item)

