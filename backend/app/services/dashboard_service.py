from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.body_metrics import BodyMetric
from app.models.cardio_logs import CardioLog
from app.models.challenge_days import ChallengeDay
from app.models.user_profile import UserProfile
from app.models.workouts import Workout, WorkoutExercise
from app.services.calorie_service import calculate_daily_energy_balance, get_weekly_energy_balance
from app.services.challenge_service import get_today_summary
from app.services.hydration_service import get_daily_hydration, get_weekly_hydration
from app.services.nutrition_service import get_daily_nutrition, get_weekly_nutrition
from app.services.weekly_review_service import get_weekly_summary
from app.services.workout_service import recent_activity, recent_prs


def get_dashboard_metrics(db: Session, profile: UserProfile) -> dict:
    today = date.today()
    week_start = today - timedelta(days=6)
    weekly_workouts = len({row[0] for row in db.execute(select(Workout.date).where(Workout.profile_id == profile.id, Workout.date >= week_start)).all()})
    weekly_volume = float(
        db.scalar(
            select(func.coalesce(func.sum(WorkoutExercise.volume), 0.0))
            .join(Workout, Workout.id == WorkoutExercise.workout_id)
            .where(Workout.profile_id == profile.id, Workout.date >= week_start)
        ) or 0.0
    )
    weekly_prs = len(
        db.execute(
            select(WorkoutExercise.id)
            .join(Workout, Workout.id == WorkoutExercise.workout_id)
            .where(Workout.profile_id == profile.id, Workout.date >= week_start, WorkoutExercise.new_pr.in_(["PR", "First"]))
        ).all()
    )
    cardio_rows = list(db.scalars(select(CardioLog).where(CardioLog.profile_id == profile.id, CardioLog.date >= week_start)).all())
    cardio_mins = sum(int(item.duration_min or 0) for item in cardio_rows)
    cardio_cals = sum(int(item.calories or 0) for item in cardio_rows)
    latest_weight_row = db.scalar(select(BodyMetric).where(BodyMetric.profile_id == profile.id).order_by(BodyMetric.date.desc()).limit(1))
    latest_weight = float(latest_weight_row.body_weight) if latest_weight_row and latest_weight_row.body_weight is not None else None
    challenge_rows = list(db.scalars(select(ChallengeDay).where(ChallengeDay.profile_id == profile.id)).all())
    perfect_days = sum(1 for row in challenge_rows if row.day_status == "perfect")
    failed_days = sum(1 for row in challenge_rows if row.day_status == "failed")
    consistency_pct = min(100, int((weekly_workouts / 5) * 100))
    weekly_score = min(100, min(40, weekly_workouts * 8) + min(25, (cardio_mins // 10) * 2) + (20 if latest_weight_row and latest_weight_row.date >= week_start else 0) + min(15, weekly_prs * 5))
    return {
        "streak": get_today_summary(db, profile)["current_streak"],
        "weekly_workouts": weekly_workouts,
        "weekly_volume": round(weekly_volume, 2),
        "weekly_prs": weekly_prs,
        "cardio_mins": cardio_mins,
        "cardio_cals": cardio_cals,
        "latest_weight": latest_weight,
        "weekly_score": weekly_score,
        "consistency_pct": consistency_pct,
        "perfect_days": perfect_days,
        "failed_days": failed_days,
    }


def get_dashboard_summary(db: Session, profile: UserProfile) -> dict:
    today = date.today()
    metrics = get_dashboard_metrics(db, profile)
    energy = calculate_daily_energy_balance(db, profile, today)
    nutrition = get_daily_nutrition(db, profile, today)
    hydration = get_daily_hydration(db, profile, today)
    challenge = get_today_summary(db, profile, today)
    weekly_energy_chart, _ = get_weekly_energy_balance(db, profile, today)
    weekly_nutrition_chart, _ = get_weekly_nutrition(db, profile, today)
    weekly_hydration_chart = get_weekly_hydration(db, profile, today)
    return {
        "metrics": metrics,
        "energy": energy,
        "nutrition": {"totals": nutrition["totals"], "remaining": nutrition["remaining"], "targets": nutrition["targets"]},
        "hydration": {
            "date": hydration["date"],
            "total_ml": hydration["total_ml"],
            "target_ml": hydration["target_ml"],
            "target_liters": hydration["target_liters"],
            "remaining_ml": hydration["remaining_ml"],
            "bottle_count": hydration["bottle_count"],
            "progress_pct": hydration["progress_pct"],
        },
        "challenge": {"day_status": challenge["day_status"], "compliance_score": challenge["compliance_score"], "pending_tasks": challenge["pending_tasks"], "split_plan": challenge["split_plan"], "weekly_summary": get_weekly_summary(db, profile)},
        "recent_activity": recent_activity(db, profile),
        "recent_prs": recent_prs(db, profile),
        "weekly_energy_chart": weekly_energy_chart,
        "weekly_nutrition_chart": weekly_nutrition_chart,
        "weekly_hydration_chart": weekly_hydration_chart,
    }
