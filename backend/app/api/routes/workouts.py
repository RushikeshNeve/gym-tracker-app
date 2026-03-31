from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_profile
from app.db.session import get_db
from app.schemas.common import MessageResponse
from app.schemas.workouts import WorkoutCreate, WorkoutHistoryEntry, WorkoutRead
from app.services.workout_service import create_workout, delete_workout, exercise_history, list_workouts


router = APIRouter(prefix="/workouts", tags=["workouts"])


@router.get("", response_model=list[WorkoutRead])
def read_workouts(db: Session = Depends(get_db), profile=Depends(get_profile)) -> list[WorkoutRead]:
    return [WorkoutRead.model_validate(item) for item in list_workouts(db, profile)]


@router.post("", response_model=WorkoutRead)
def create_workout_route(payload: WorkoutCreate, db: Session = Depends(get_db), profile=Depends(get_profile)) -> WorkoutRead:
    return WorkoutRead.model_validate(create_workout(db, profile, payload))


@router.get("/history/{exercise_name}", response_model=list[WorkoutHistoryEntry])
def read_exercise_history(exercise_name: str, db: Session = Depends(get_db), profile=Depends(get_profile)) -> list[WorkoutHistoryEntry]:
    return [WorkoutHistoryEntry(**item) for item in exercise_history(db, profile, exercise_name)]


@router.delete("/{workout_id}", response_model=MessageResponse)
def delete_workout_route(workout_id: int, db: Session = Depends(get_db), profile=Depends(get_profile)) -> MessageResponse:
    if not delete_workout(db, profile, workout_id):
        raise HTTPException(status_code=404, detail="Workout not found")
    return MessageResponse(message="Workout deleted")

