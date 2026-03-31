from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_profile
from app.db.session import get_db
from app.schemas.common import MessageResponse
from app.schemas.metrics import BodyMetricCreate, BodyMetricRead, BodyMetricUpdate
from app.services.metrics_service import create_body_metric, delete_body_metric, list_body_metrics, update_body_metric


router = APIRouter(prefix="/body-metrics", tags=["body-metrics"])


@router.get("", response_model=list[BodyMetricRead])
def read_body_metrics(db: Session = Depends(get_db), profile=Depends(get_profile)) -> list[BodyMetricRead]:
    return [BodyMetricRead.model_validate(item) for item in list_body_metrics(db, profile)]


@router.post("", response_model=BodyMetricRead)
def create_body_metric_route(payload: BodyMetricCreate, db: Session = Depends(get_db), profile=Depends(get_profile)) -> BodyMetricRead:
    return BodyMetricRead.model_validate(create_body_metric(db, profile, payload))


@router.patch("/{metric_id}", response_model=BodyMetricRead)
def update_body_metric_route(metric_id: int, payload: BodyMetricUpdate, db: Session = Depends(get_db), profile=Depends(get_profile)) -> BodyMetricRead:
    item = update_body_metric(db, profile, metric_id, payload)
    if not item:
        raise HTTPException(status_code=404, detail="Body metric not found")
    return BodyMetricRead.model_validate(item)


@router.delete("/{metric_id}", response_model=MessageResponse)
def delete_body_metric_route(metric_id: int, db: Session = Depends(get_db), profile=Depends(get_profile)) -> MessageResponse:
    if not delete_body_metric(db, profile, metric_id):
        raise HTTPException(status_code=404, detail="Body metric not found")
    return MessageResponse(message="Body metric deleted")
