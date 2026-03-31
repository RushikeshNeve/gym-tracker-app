from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.exercise_library import ExerciseLibrary


def list_exercises(
    db: Session,
    *,
    search: str | None = None,
    day_type: str | None = None,
    muscle_group: str | None = None,
) -> list[ExerciseLibrary]:
    statement = select(ExerciseLibrary).order_by(ExerciseLibrary.muscle_group.asc(), ExerciseLibrary.name.asc())
    if search:
        statement = statement.where(ExerciseLibrary.name.ilike(f"%{search}%"))
    if day_type:
        statement = statement.where(ExerciseLibrary.day_type == day_type)
    if muscle_group:
        statement = statement.where(ExerciseLibrary.muscle_group == muscle_group)
    return list(db.scalars(statement).all())


def get_exercise(db: Session, exercise_id: int) -> ExerciseLibrary | None:
    return db.get(ExerciseLibrary, exercise_id)

