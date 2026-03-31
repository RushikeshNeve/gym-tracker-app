from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.body_metrics import BodyMetric
from app.models.user_profile import UserProfile
from app.schemas.metrics import BodyMetricCreate, BodyMetricUpdate


def create_body_metric(db: Session, profile: UserProfile, payload: BodyMetricCreate) -> BodyMetric:
    item = BodyMetric(profile_id=profile.id, **payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def list_body_metrics(db: Session, profile: UserProfile) -> list[BodyMetric]:
    return list(
        db.scalars(
            select(BodyMetric)
            .where(BodyMetric.profile_id == profile.id)
            .order_by(BodyMetric.date.desc(), BodyMetric.id.desc())
        ).all()
    )


def update_body_metric(db: Session, profile: UserProfile, metric_id: int, payload: BodyMetricUpdate) -> BodyMetric | None:
    item = db.scalar(select(BodyMetric).where(BodyMetric.id == metric_id, BodyMetric.profile_id == profile.id))
    if not item:
        return None

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def delete_body_metric(db: Session, profile: UserProfile, metric_id: int) -> bool:
    item = db.scalar(select(BodyMetric).where(BodyMetric.id == metric_id, BodyMetric.profile_id == profile.id))
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True
