from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.exercises import ExerciseRead
from app.services.exercise_service import get_exercise, list_exercises


router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.get("", response_model=list[ExerciseRead])
def read_exercises(search: str | None = None, day_type: str | None = None, muscle_group: str | None = None, db: Session = Depends(get_db)) -> list[ExerciseRead]:
    return [ExerciseRead.model_validate(item) for item in list_exercises(db, search=search, day_type=day_type, muscle_group=muscle_group)]


@router.get("/{exercise_id}", response_model=ExerciseRead)
def read_exercise(exercise_id: int, db: Session = Depends(get_db)) -> ExerciseRead:
    item = get_exercise(db, exercise_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return ExerciseRead.model_validate(item)

