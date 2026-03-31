from __future__ import annotations

from app.schemas.common import TimestampFields


class ExerciseRead(TimestampFields):
    id: int
    name: str
    day_type: str
    muscle_group: str
    youtube_url: str
    youtube_search_url: str
    instructions_json: list[str]
    common_mistakes_json: list[str]
    tips: str
    matched: bool

