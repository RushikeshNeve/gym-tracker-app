"""Helpers for enriched exercise metadata and YouTube handling."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DATA_PATH = Path("data/exercise_videos.json")


def load_exercise_data() -> list[dict[str, Any]]:
    if not DATA_PATH.exists():
        return []
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def search_exercises(
    exercises: list[dict[str, Any]],
    query: str = "",
    day_types: list[str] | None = None,
    muscle_groups: list[str] | None = None,
) -> list[dict[str, Any]]:
    day_types = day_types or []
    muscle_groups = muscle_groups or []
    query = query.strip().lower()

    filtered = []
    for item in exercises:
        if day_types and item["day_type"] not in day_types:
            continue
        if muscle_groups and item["muscle_group"] not in muscle_groups:
            continue
        if query and query not in item["name"].lower():
            continue
        filtered.append(item)

    return filtered


def get_exercise_by_name(exercises: list[dict[str, Any]], name: str) -> dict[str, Any] | None:
    return next((item for item in exercises if item["name"] == name), None)


def resolve_video_link(exercise: dict[str, Any]) -> tuple[str, str]:
    youtube_url = exercise.get("youtube_url", "") or ""
    youtube_search_url = exercise.get("youtube_search_url", "") or ""
    return youtube_url, youtube_search_url
