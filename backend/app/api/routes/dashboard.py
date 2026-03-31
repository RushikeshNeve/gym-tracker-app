from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_profile
from app.db.session import get_db
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import get_dashboard_summary


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardResponse)
def read_dashboard(db: Session = Depends(get_db), profile=Depends(get_profile)) -> DashboardResponse:
    return DashboardResponse(**get_dashboard_summary(db, profile))

