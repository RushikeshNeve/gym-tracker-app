from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_profile
from app.db.session import get_db
from app.schemas.cardio import CardioLogCreate, CardioLogRead
from app.schemas.common import MessageResponse
from app.services.cardio_service import create_cardio_log, delete_cardio_log, list_cardio_logs


router = APIRouter(prefix="/cardio", tags=["cardio"])


@router.get("", response_model=list[CardioLogRead])
def read_cardio_logs(db: Session = Depends(get_db), profile=Depends(get_profile)) -> list[CardioLogRead]:
    return [CardioLogRead.model_validate(item) for item in list_cardio_logs(db, profile)]


@router.post("", response_model=CardioLogRead)
def create_cardio_route(payload: CardioLogCreate, db: Session = Depends(get_db), profile=Depends(get_profile)) -> CardioLogRead:
    return CardioLogRead.model_validate(create_cardio_log(db, profile, payload))


@router.delete("/{log_id}", response_model=MessageResponse)
def delete_cardio_route(log_id: int, db: Session = Depends(get_db), profile=Depends(get_profile)) -> MessageResponse:
    if not delete_cardio_log(db, profile, log_id):
        raise HTTPException(status_code=404, detail="Cardio log not found")
    return MessageResponse(message="Cardio log deleted")

