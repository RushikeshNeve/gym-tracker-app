from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.body_metrics import BodyMetric
from app.models.cardio_logs import CardioLog
from app.models.challenge_days import ChallengeDay
from app.models.user_profile import UserProfile
from app.models.weekly_reviews import WeeklyReview
from app.models.workouts import Workout, WorkoutExercise
from app.services.hydration_service import get_weekly_hydration
from app.services.nutrition_service import get_weekly_nutrition


def get_week_start(reference_date: date | None = None) -> date:
    ref = reference_date or date.today()
    return ref - timedelta(days=ref.weekday())


def get_weekly_review_record(db: Session, profile: UserProfile, week_start: date) -> WeeklyReview | None:
    return db.scalar(select(WeeklyReview).where(WeeklyReview.profile_id == profile.id, WeeklyReview.week_start == week_start))


def upsert_weekly_review(db: Session, profile: UserProfile, payload: dict) -> WeeklyReview:
    record = get_weekly_review_record(db, profile, payload["week_start"])
    if record is None:
        record = WeeklyReview(profile_id=profile.id, **payload)
    else:
        for key, value in payload.items():
            setattr(record, key, value)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_weekly_summary(db: Session, profile: UserProfile, week_start: date | None = None) -> dict:
    start = week_start or get_week_start()
    end = start + timedelta(days=6)
    workouts = list(db.scalars(select(Workout).where(Workout.profile_id == profile.id, Workout.date.between(start, end)).order_by(Workout.date.asc())).all())
    cardio = list(db.scalars(select(CardioLog).where(CardioLog.profile_id == profile.id, CardioLog.date.between(start, end)).order_by(CardioLog.date.asc())).all())
    body = list(db.scalars(select(BodyMetric).where(BodyMetric.profile_id == profile.id, BodyMetric.date.between(start, end)).order_by(BodyMetric.date.asc())).all())
    challenge = list(db.scalars(select(ChallengeDay).where(ChallengeDay.profile_id == profile.id, ChallengeDay.date.between(start, end)).order_by(ChallengeDay.date.asc())).all())
    prs = len(
        db.execute(
            select(WorkoutExercise.id)
            .join(Workout, Workout.id == WorkoutExercise.workout_id)
            .where(Workout.profile_id == profile.id, Workout.date.between(start, end), WorkoutExercise.new_pr.in_(["PR", "First"]))
        ).all()
    )
    nutrition_chart, nutrition_summary = get_weekly_nutrition(db, profile, end)
    hydration_chart = get_weekly_hydration(db, profile, end)
    total_workout_volume = float(sum(
        row[0] or 0
        for row in db.execute(
            select(WorkoutExercise.volume)
            .join(Workout, Workout.id == WorkoutExercise.workout_id)
            .where(Workout.profile_id == profile.id, Workout.date.between(start, end))
        ).all()
    ))
    weight_change = 0.0
    waist_change = 0.0
    if len(body) >= 2:
        weight_change = float((body[-1].body_weight or 0) - (body[0].body_weight or 0))
        waist_change = float((body[-1].waist or 0) - (body[0].waist or 0))
    return {
        "week_start": start,
        "week_end": end,
        "avg_calories": nutrition_summary["avg_calories"],
        "avg_protein": nutrition_summary["avg_protein"],
        "water_adherence_pct": round(sum(item["adherence_pct"] for item in hydration_chart) / len(hydration_chart), 2) if hydration_chart else 0.0,
        "workout_consistency": len({item.date for item in workouts}),
        "outdoor_workout_consistency": sum(1 for item in workouts if item.is_outdoor) + sum(1 for item in cardio if item.is_outdoor),
        "weight_change": round(weight_change, 2),
        "waist_change": round(waist_change, 2),
        "perfect_days": sum(1 for item in challenge if item.day_status == "perfect"),
        "incomplete_days": sum(1 for item in challenge if item.day_status == "incomplete"),
        "failed_days": sum(1 for item in challenge if item.day_status == "failed"),
        "prs": prs,
        "total_workout_volume": round(total_workout_volume, 2),
        "cardio_minutes": sum(int(item.duration_min or 0) for item in cardio),
        "nutrition_chart": nutrition_chart,
        "hydration_chart": hydration_chart,
        "challenge_chart": [{"date": item.date, "day_status": item.day_status, "compliance_score": item.compliance_score} for item in challenge],
    }

