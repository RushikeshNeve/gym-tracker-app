from datetime import date

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_profile
from app.db.session import get_db
from app.schemas.photos import ProgressPhotoCreate, ProgressPhotoRead
from app.services.photo_service import create_progress_photo, list_progress_photos, save_progress_photo_file


router = APIRouter(prefix="/progress-photos", tags=["progress-photos"])


@router.get("", response_model=list[ProgressPhotoRead])
def read_progress_photos(log_date: str | None = None, db: Session = Depends(get_db), profile=Depends(get_profile)) -> list[ProgressPhotoRead]:
    parsed = date.fromisoformat(log_date) if log_date else None
    return [ProgressPhotoRead.model_validate(item) for item in list_progress_photos(db, profile, parsed)]


@router.post("", response_model=ProgressPhotoRead)
def create_progress_photo_route(payload: ProgressPhotoCreate, db: Session = Depends(get_db), profile=Depends(get_profile)) -> ProgressPhotoRead:
    return ProgressPhotoRead.model_validate(create_progress_photo(db, profile, payload))


@router.post("/upload", response_model=ProgressPhotoRead)
def upload_progress_photo_route(
    request: Request,
    photo: UploadFile = File(...),
    log_date: str = Form(...),
    photo_type: str = Form(...),
    notes: str = Form(default=""),
    db: Session = Depends(get_db),
    profile=Depends(get_profile),
) -> ProgressPhotoRead:
    parsed_date = date.fromisoformat(log_date)
    content_type = (photo.content_type or "").lower()
    if content_type not in {"image/jpeg", "image/jpg", "image/png", "image/webp"}:
        raise HTTPException(status_code=400, detail="Only jpg, png, and webp images are supported")

    try:
        blob_key, file_url = save_progress_photo_file(photo, profile.id, photo_type, parsed_date)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    if file_url.startswith("/"):
        base_url = str(request.base_url).rstrip("/")
        file_url = f"{base_url}{file_url}"

    payload = ProgressPhotoCreate(
        date=parsed_date,
        photo_type=photo_type.strip().lower(),
        file_url=file_url,
        blob_key=blob_key,
        notes=notes,
    )
    item = create_progress_photo(db, profile, payload)
    return ProgressPhotoRead.model_validate(item)
