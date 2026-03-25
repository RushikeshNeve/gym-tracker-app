from __future__ import annotations

import json
from pathlib import Path

DATA_PATH = Path("data/enriched_exercises.json")


def load_enriched_exercises(path: Path = DATA_PATH) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def get_exercise_by_name(exercises: list[dict], name: str) -> dict | None:
    return next((exercise for exercise in exercises if exercise.get("name") == name), None)


def get_preview_image_urls(exercise: dict) -> tuple[str, str]:
    return exercise.get("image_1_url", ""), exercise.get("image_2_url", "")


def search_and_filter_exercises(
    exercises: list[dict],
    query: str = "",
    day_types: list[str] | None = None,
    muscle_groups: list[str] | None = None,
    equipment: list[str] | None = None,
    levels: list[str] | None = None,
    categories: list[str] | None = None,
    matched_only: bool = False,
) -> list[dict]:
    results = exercises
    if query:
        q = query.lower().strip()
        results = [e for e in results if q in e.get("name", "").lower() or q in (e.get("source_name") or "").lower()]
    if day_types:
        results = [e for e in results if e.get("day_type") in day_types]
    if muscle_groups:
        results = [e for e in results if e.get("muscle_group") in muscle_groups]
    if equipment:
        results = [e for e in results if (e.get("equipment") or "Unknown") in equipment]
    if levels:
        results = [e for e in results if (e.get("level") or "Unknown") in levels]
    if categories:
        results = [e for e in results if (e.get("category") or "Unknown") in categories]
    if matched_only:
        results = [e for e in results if e.get("matched", False)]
    return results


def filter_values(exercises: list[dict], key: str) -> list[str]:
    values = sorted({(exercise.get(key) or "Unknown") for exercise in exercises})
    return values
