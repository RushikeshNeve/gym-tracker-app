from fastapi import Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user_profile import UserProfile
from app.services.profile_service import ensure_profile


def get_profile(
    profile_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
) -> UserProfile:
    return ensure_profile(db, profile_id=profile_id)

