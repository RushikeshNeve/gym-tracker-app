from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.workout_timetable import WorkoutTimetableRead
from app.services.workout_timetable_service import get_workout_timetable


router = APIRouter(prefix="/workout-timetable", tags=["workout-timetable"])


@router.get("", response_model=WorkoutTimetableRead)
def read_workout_timetable(db: Session = Depends(get_db)) -> WorkoutTimetableRead:
    return WorkoutTimetableRead.model_validate(get_workout_timetable(db))
