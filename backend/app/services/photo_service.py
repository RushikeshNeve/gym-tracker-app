from __future__ import annotations

import json
from pathlib import Path
from urllib import error, request
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import UploadFile

from app.core.config import settings
from app.models.progress_photos import ProgressPhoto
from app.models.user_profile import UserProfile
from app.schemas.photos import ProgressPhotoCreate


def create_progress_photo(db: Session, profile: UserProfile, payload: ProgressPhotoCreate) -> ProgressPhoto:
    item = ProgressPhoto(profile_id=profile.id, **payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def list_progress_photos(db: Session, profile: UserProfile, log_date=None) -> list[ProgressPhoto]:
    statement = select(ProgressPhoto).where(ProgressPhoto.profile_id == profile.id)
    if log_date is not None:
        statement = statement.where(ProgressPhoto.date == log_date)
    return list(db.scalars(statement.order_by(ProgressPhoto.date.desc(), ProgressPhoto.id.desc())).all())


def save_progress_photo_file(upload: UploadFile, profile_id: int, photo_type: str, log_date) -> tuple[str, str]:
    if settings.storage_backend == "vercel_blob":
        return _save_progress_photo_to_vercel_blob(upload, profile_id, photo_type, log_date)
    return _save_progress_photo_to_local_disk(upload, profile_id, photo_type, log_date)


def _save_progress_photo_to_local_disk(upload: UploadFile, profile_id: int, photo_type: str, log_date) -> tuple[str, str]:
    extension = Path(upload.filename or "photo.jpg").suffix.lower() or ".jpg"
    safe_type = (photo_type or "front").strip().lower()
    target_dir = Path(settings.media_root) / "progress-photos" / str(profile_id) / log_date.isoformat()
    target_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{safe_type}-{uuid4().hex}{extension}"
    target_path = target_dir / filename

    with target_path.open("wb") as file_handle:
        upload.file.seek(0)
        file_handle.write(upload.file.read())

    relative_blob_key = str(target_path.relative_to(Path(settings.media_root))).replace("\\", "/")
    file_url = f"{settings.media_url_prefix.rstrip('/')}/{relative_blob_key}"
    return relative_blob_key, file_url


def _save_progress_photo_to_vercel_blob(upload: UploadFile, profile_id: int, photo_type: str, log_date) -> tuple[str, str]:
    if not settings.blob_read_write_token:
        raise RuntimeError("FITNESS_BLOB_READ_WRITE_TOKEN is required when FITNESS_STORAGE_BACKEND=vercel_blob")

    extension = Path(upload.filename or "photo.jpg").suffix.lower() or ".jpg"
    safe_type = (photo_type or "front").strip().lower()
    pathname = f"progress-photos/{profile_id}/{log_date.isoformat()}/{safe_type}-{uuid4().hex}{extension}"

    upload.file.seek(0)
    content = upload.file.read()
    req = request.Request(
        f"{settings.blob_api_base_url.rstrip('/')}/{pathname}?access=public",
        data=content,
        method="PUT",
        headers={
            "Authorization": f"Bearer {settings.blob_read_write_token}",
            "Content-Type": upload.content_type or "application/octet-stream",
            "x-add-random-suffix": "0",
        },
    )

    try:
        with request.urlopen(req) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Vercel Blob upload failed: {detail or exc.reason}") from exc

    blob_key = str(payload.get("pathname") or pathname)
    file_url = str(payload.get("url") or "")
    if not file_url:
        raise RuntimeError("Vercel Blob upload did not return a file URL")
    return blob_key, file_url
