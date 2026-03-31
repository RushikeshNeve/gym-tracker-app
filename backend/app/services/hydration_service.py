from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.hydration_logs import HydrationLog
from app.models.user_profile import UserProfile
from app.schemas.hydration import HydrationLogCreate
from app.services.profile_service import get_or_create_daily_target


def create_hydration_log(db: Session, profile: UserProfile, payload: HydrationLogCreate) -> HydrationLog:
    item = HydrationLog(profile_id=profile.id, **payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def delete_hydration_log(db: Session, profile: UserProfile, log_id: int) -> bool:
    item = db.scalar(select(HydrationLog).where(HydrationLog.id == log_id, HydrationLog.profile_id == profile.id))
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True


def get_daily_hydration(db: Session, profile: UserProfile, log_date: date) -> dict:
    logs = list(
        db.scalars(
            select(HydrationLog)
            .where(HydrationLog.profile_id == profile.id, HydrationLog.date == log_date)
            .order_by(HydrationLog.id.desc())
        ).all()
    )
    target = get_or_create_daily_target(db, profile, log_date)
    total_ml = sum(log.amount_ml for log in logs)
    target_ml = int(float(target.water_target_liters or 0) * 1000)
    return {
        "date": log_date,
        "logs": logs,
        "target_liters": float(target.water_target_liters or 0),
        "target_ml": target_ml,
        "total_ml": total_ml,
        "remaining_ml": max(0, target_ml - total_ml),
        "bottle_count": round(total_ml / 500, 1) if total_ml else 0,
        "progress_pct": min(100.0, round((total_ml / target_ml) * 100, 1)) if target_ml else 0.0,
    }


def get_weekly_hydration(db: Session, profile: UserProfile, end_date: date | None = None) -> list[dict]:
    end = end_date or date.today()
    start = end - timedelta(days=6)
    rows = db.execute(
        select(HydrationLog.date, func.coalesce(func.sum(HydrationLog.amount_ml), 0))
        .where(
            HydrationLog.profile_id == profile.id,
            HydrationLog.date.between(start, end),
        )
        .group_by(HydrationLog.date)
        .order_by(HydrationLog.date.asc())
    ).all()
    chart = []
    for row in rows:
        target = get_or_create_daily_target(db, profile, row[0])
        target_ml = int(float(target.water_target_liters or 0) * 1000)
        total_ml = int(row[1] or 0)
        chart.append(
            {
                "date": row[0],
                "total_ml": total_ml,
                "target_ml": target_ml,
                "adherence_pct": round(min(100.0, (total_ml / target_ml) * 100), 2) if target_ml else 0.0,
            }
        )
    return chart

