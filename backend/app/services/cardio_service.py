from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.cardio_logs import CardioLog
from app.models.user_profile import UserProfile
from app.schemas.cardio import CardioLogCreate
from app.utils.calculations import estimate_calories_burned


def create_cardio_log(db: Session, profile: UserProfile, payload: CardioLogCreate) -> CardioLog:
    estimated_burn = payload.estimated_calories_burned
    if estimated_burn is None:
        estimated_burn = estimate_calories_burned(payload.cardio_type, payload.duration_min, float(profile.current_weight_kg or 0))
    item = CardioLog(profile_id=profile.id, estimated_calories_burned=estimated_burn, **payload.model_dump(exclude={"estimated_calories_burned"}))
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def list_cardio_logs(db: Session, profile: UserProfile) -> list[CardioLog]:
    return list(
        db.scalars(
            select(CardioLog)
            .where(CardioLog.profile_id == profile.id)
            .order_by(CardioLog.date.desc(), CardioLog.id.desc())
        ).all()
    )


def delete_cardio_log(db: Session, profile: UserProfile, log_id: int) -> bool:
    item = db.scalar(select(CardioLog).where(CardioLog.id == log_id, CardioLog.profile_id == profile.id))
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True

