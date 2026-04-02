from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.user_profile import UserProfile
from app.models.workouts import Workout, WorkoutExercise
from app.schemas.workouts import WorkoutCreate
from app.utils.calculations import estimate_calories_burned


def calculate_pr_status(
    db: Session,
    profile: UserProfile,
    exercise_name: str,
    weight: float,
    reps: int,
    duration_seconds: int | None = None,
) -> str:
    rows = db.execute(
        select(WorkoutExercise.weight, WorkoutExercise.reps, WorkoutExercise.duration_seconds)
        .join(Workout, Workout.id == WorkoutExercise.workout_id)
        .where(
            Workout.profile_id == profile.id,
            WorkoutExercise.exercise_name == exercise_name,
        )
        .order_by(Workout.date.asc(), WorkoutExercise.id.asc())
    ).all()
    if not rows:
        return "First"
    max_weight = max(float(row.weight or 0) for row in rows)
    best_reps_at_max = max(int(row.reps or 0) for row in rows if float(row.weight or 0) == max_weight)
    best_duration_at_max = max(int(row.duration_seconds or 0) for row in rows if float(row.weight or 0) == max_weight)
    current_duration = int(duration_seconds or 0)
    if (
        weight > max_weight
        or (weight == max_weight and reps > best_reps_at_max)
        or (weight == max_weight and reps == best_reps_at_max and current_duration > best_duration_at_max)
    ):
        return "PR"
    return ""


def create_workout(db: Session, profile: UserProfile, payload: WorkoutCreate) -> Workout:
    estimated_burn = payload.estimated_calories_burned
    if estimated_burn is None:
        estimated_burn = estimate_calories_burned(payload.day_type, payload.duration_min, float(profile.current_weight_kg or 0))
    workout = Workout(
        profile_id=profile.id,
        date=payload.date,
        day_type=payload.day_type,
        session_type=payload.session_type,
        is_outdoor=payload.is_outdoor,
        duration_min=payload.duration_min,
        start_time=payload.start_time,
        end_time=payload.end_time,
        session_notes=payload.session_notes,
        estimated_calories_burned=estimated_burn,
    )
    db.add(workout)
    db.flush()
    for item in payload.exercises:
        pr_status = calculate_pr_status(
            db,
            profile,
            item.exercise_name,
            float(item.weight),
            int(item.reps),
            item.duration_seconds,
        )
        volume = float(item.weight) * int(item.reps) * int(item.sets)
        db.add(
            WorkoutExercise(
                workout_id=workout.id,
                exercise_name=item.exercise_name,
                muscle_group=item.muscle_group,
                weight=item.weight,
                reps=item.reps,
                sets=item.sets,
                duration_seconds=item.duration_seconds,
                volume=volume,
                near_failure=item.near_failure,
                new_pr=pr_status,
                notes=item.notes,
            )
        )
    db.commit()
    return get_workout(db, workout.id)


def list_workouts(db: Session, profile: UserProfile) -> list[Workout]:
    return list(
        db.scalars(
            select(Workout)
            .where(Workout.profile_id == profile.id)
            .options(selectinload(Workout.exercises))
            .order_by(Workout.date.desc(), Workout.id.desc())
        ).all()
    )


def get_workout(db: Session, workout_id: int) -> Workout | None:
    return db.scalar(select(Workout).where(Workout.id == workout_id).options(selectinload(Workout.exercises)))


def delete_workout(db: Session, profile: UserProfile, workout_id: int) -> bool:
    workout = db.scalar(select(Workout).where(Workout.id == workout_id, Workout.profile_id == profile.id))
    if not workout:
        return False
    db.delete(workout)
    db.commit()
    return True


def recent_activity(db: Session, profile: UserProfile, limit: int = 10) -> list[dict]:
    rows = db.execute(
        select(
            Workout.date,
            Workout.day_type,
            Workout.session_type,
            Workout.is_outdoor,
            WorkoutExercise.exercise_name,
            WorkoutExercise.weight,
            WorkoutExercise.reps,
            WorkoutExercise.sets,
            WorkoutExercise.duration_seconds,
            WorkoutExercise.new_pr,
        )
        .join(WorkoutExercise, WorkoutExercise.workout_id == Workout.id)
        .where(Workout.profile_id == profile.id)
        .order_by(Workout.date.desc(), Workout.id.desc(), WorkoutExercise.id.desc())
        .limit(limit)
    ).all()
    return [
        {
            "date": row.date,
            "day_type": row.day_type,
            "session_type": row.session_type,
            "is_outdoor": row.is_outdoor,
            "exercise_name": row.exercise_name,
            "weight": float(row.weight or 0),
            "reps": int(row.reps or 0),
            "sets": int(row.sets or 0),
            "new_pr": row.new_pr or "",
        }
        for row in rows
    ]


def recent_prs(db: Session, profile: UserProfile, limit: int = 10) -> list[dict]:
    rows = db.execute(
        select(
            Workout.date,
            WorkoutExercise.exercise_name,
            WorkoutExercise.weight,
            WorkoutExercise.reps,
            WorkoutExercise.new_pr,
        )
        .join(WorkoutExercise, WorkoutExercise.workout_id == Workout.id)
        .where(
            Workout.profile_id == profile.id,
            WorkoutExercise.new_pr.in_(["PR", "First"]),
        )
        .order_by(Workout.date.desc(), WorkoutExercise.id.desc())
        .limit(limit)
    ).all()
    return [
        {
            "date": row.date,
            "exercise_name": row.exercise_name,
            "weight": float(row.weight or 0),
            "reps": int(row.reps or 0),
            "new_pr": row.new_pr,
        }
        for row in rows
    ]


def exercise_history(db: Session, profile: UserProfile, exercise_name: str, limit: int = 3) -> list[dict]:
    rows = db.execute(
        select(
            Workout.date,
            Workout.session_type,
            Workout.is_outdoor,
            WorkoutExercise.weight,
            WorkoutExercise.reps,
            WorkoutExercise.sets,
            WorkoutExercise.duration_seconds,
            WorkoutExercise.new_pr,
        )
        .join(WorkoutExercise, WorkoutExercise.workout_id == Workout.id)
        .where(
            Workout.profile_id == profile.id,
            WorkoutExercise.exercise_name == exercise_name,
        )
        .order_by(Workout.date.desc(), WorkoutExercise.id.desc())
        .limit(limit)
    ).all()
    return [
        {
            "date": row.date,
            "exercise_name": exercise_name,
            "weight": float(row.weight or 0),
            "reps": int(row.reps or 0),
            "sets": int(row.sets or 0),
            "duration_seconds": int(row.duration_seconds) if row.duration_seconds is not None else None,
            "new_pr": row.new_pr or "",
            "session_type": row.session_type or "Workout 1",
            "is_outdoor": bool(row.is_outdoor),
        }
        for row in rows
    ]
