from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd
import requests

try:
    from rapidfuzz import fuzz, process
except ImportError:  # pragma: no cover
    from difflib import SequenceMatcher

    class _FallbackFuzz:
        @staticmethod
        def WRatio(a: str, b: str) -> float:
            return SequenceMatcher(None, a.lower(), b.lower()).ratio() * 100

    class _FallbackProcess:
        @staticmethod
        def extractOne(query: str, choices: list[str], scorer):
            best_choice = None
            best_score = 0.0
            for choice in choices:
                score = scorer(query, choice)
                if score > best_score:
                    best_score = score
                    best_choice = choice
            if best_choice is None:
                return None
            return (best_choice, best_score, 0)

    fuzz = _FallbackFuzz()
    process = _FallbackProcess()

from seed_exercises import get_custom_exercises

DATASET_URL = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/dist/exercises.json"
IMAGE_BASE_URL = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/"
DATA_DIR = Path("data")
CACHE_PATH = DATA_DIR / "free_exercise_db.json"
ENRICHED_PATH = DATA_DIR / "enriched_exercises.json"
UNMATCHED_PATH = DATA_DIR / "unmatched_exercises.json"
REPORT_PATH = DATA_DIR / "match_report.csv"

IGNORE_TOKENS = {"machine", "dumbbell", "barbell"}

MANUAL_TARGETS = {
    "Flat Dumbbell Press": ["Dumbbell Bench Press"],
    "Flat Barbell Bench Press": ["Barbell Bench Press - Medium Grip"],
    "Incline Dumbbell Press": ["Incline Dumbbell Press"],
    "Incline Barbell Bench Press": ["Barbell Incline Bench Press Medium-Grip"],
    "Incline Machine Press": ["Machine Chest Press"],
    "Pec Deck Fly": ["Butterfly"],
    "Cable Fly": ["Cable Crossover"],
    "High to Low Cable Crossover": ["Cable Crossover"],
    "Shoulder Press": ["Seated Dumbbell Press"],
    "Dumbbell Shoulder Press": ["Seated Dumbbell Press"],
    "Cable Lateral Raise": ["One-Arm Cable Lateral Raise"],
    "Rope Pushdown": ["Triceps Pushdown - Rope Attachment"],
    "Skull Crushers": ["Lying Triceps Press"],
    "Lat Pulldown": ["Wide-Grip Lat Pulldown"],
    "Wide Grip Lat Pulldown": ["Wide-Grip Lat Pulldown"],
    "Seated Cable Row": ["Seated Cable Rows"],
    "Dumbbell Row": ["One-Arm Dumbbell Row"],
    "Dumbbell Curl": ["Dumbbell Bicep Curl"],
    "Hammer Curl": ["Hammer Curls"],
    "Leg Press": ["Leg Press"],
    "Leg Extension": ["Leg Extensions"],
    "Romanian Deadlift": ["Romanian Deadlift"],
    "Leg Curl": ["Lying Leg Curls"],
    "Calf Raises": ["Standing Calf Raises"],
    "Crunches": ["Crunches"],
    "Plank": ["Plank"],
    "Treadmill Running": ["Running, Treadmill"],
    "Cycling": ["Bicycling, Stationary"],
    "Rowing Machine": ["Rowing, Stationary"],
    "Elliptical": ["Elliptical Trainer"],
}

ALIAS_RULES = {
    "shoulder press": ["seated dumbbell press", "machine shoulder press"],
    "flat dumbbell press": ["dumbbell bench press"],
    "flat barbell bench press": ["barbell bench press"],
    "incline machine press": ["machine chest press", "incline dumbbell press"],
    "cable lateral raise": ["one arm cable lateral raise"],
    "rope pushdown": ["triceps pushdown"],
    "straight bar pushdown": ["triceps pushdown"],
    "skull crushers": ["lying triceps press", "lying triceps extension"],
    "seated machine row wide grip": ["seated cable rows"],
    "seated machine row close grip": ["close grip front lat pulldown"],
    "dumbbell rdl": ["romanian deadlift"],
    "calf raises": ["standing calf raises"],
    "crunches": ["crunches"],
    "outdoor run": ["running treadmill", "running, treadmill"],
    "stairmaster": ["stairmaster"],
}


def normalize_name(name: str, strip_modifiers: bool = False) -> str:
    cleaned = name.lower().replace("&", " and ")
    cleaned = re.sub(r"[^a-z0-9\s]", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if strip_modifiers:
        cleaned = " ".join(token for token in cleaned.split() if token not in IGNORE_TOKENS)
    return cleaned


def load_source_data() -> list[dict]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if CACHE_PATH.exists():
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))

    try:
        response = requests.get(DATASET_URL, timeout=20)
        response.raise_for_status()
        payload = response.json()
        CACHE_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return payload
    except requests.RequestException:
        print("Warning: free-exercise-db fetch failed and no cache found. Continuing with unmatched placeholders.")
        return []


def _best_candidate(query: str, choices: list[str]) -> tuple[str | None, float]:
    result = process.extractOne(query, choices, scorer=fuzz.WRatio)
    if not result:
        return None, 0.0
    return str(result[0]), float(result[1])


def _build_image_urls(images: list[str] | None) -> tuple[str, str]:
    if not images:
        return "", ""
    image_1 = f"{IMAGE_BASE_URL}{images[0]}" if len(images) > 0 else ""
    image_2 = f"{IMAGE_BASE_URL}{images[1]}" if len(images) > 1 else ""
    return image_1, image_2


def _build_source_indexes(source_exercises: list[dict]) -> tuple[dict[str, dict], dict[str, dict], list[str], dict[str, dict]]:
    by_norm: dict[str, dict] = {}
    by_stripped: dict[str, dict] = {}
    name_lookup: dict[str, dict] = {}
    names: list[str] = []

    for exercise in source_exercises:
        source_name = exercise.get("name", "")
        names.append(source_name)
        by_norm[normalize_name(source_name)] = exercise
        by_stripped[normalize_name(source_name, strip_modifiers=True)] = exercise
        name_lookup[source_name] = exercise

    return by_norm, by_stripped, names, name_lookup


def enrich() -> None:
    custom_exercises = get_custom_exercises()
    source_exercises = load_source_data()
    by_norm, by_stripped, source_names, name_lookup = _build_source_indexes(source_exercises)

    enriched: list[dict] = []
    report_rows: list[dict] = []
    unmatched: list[dict] = []

    for custom in custom_exercises:
        custom_name = custom["name"]
        norm = normalize_name(custom_name)
        norm_stripped = normalize_name(custom_name, strip_modifiers=True)
        source_match = None
        confidence = None
        match_stage = "unmatched"

        for manual_target in MANUAL_TARGETS.get(custom_name, []):
            exact_name = next((n for n in source_names if normalize_name(n) == normalize_name(manual_target)), None)
            if exact_name:
                source_match = name_lookup[exact_name]
                confidence = 100.0
                match_stage = "manual"
                break

        if not source_match and norm in by_norm:
            source_match = by_norm[norm]
            confidence = 100.0
            match_stage = "exact"

        if not source_match and norm_stripped in by_stripped:
            source_match = by_stripped[norm_stripped]
            confidence = 94.0
            match_stage = "exact_stripped"

        if not source_match:
            aliases = ALIAS_RULES.get(norm, [])
            for alias in aliases:
                alias_norm = normalize_name(alias)
                if alias_norm in by_norm:
                    source_match = by_norm[alias_norm]
                    confidence = 92.0
                    match_stage = "alias_exact"
                    break
                alias_choice, alias_score = _best_candidate(alias, source_names)
                if alias_choice and alias_score >= 85:
                    source_match = name_lookup[alias_choice]
                    confidence = alias_score
                    match_stage = "alias_fuzzy"
                    break

        if not source_match:
            best_name, score = _best_candidate(custom_name, source_names)
            if best_name:
                source_match = name_lookup[best_name]
                confidence = score
                match_stage = "fuzzy"

        matched = bool(source_match and confidence is not None and confidence >= 85)
        if source_match and confidence is not None and confidence < 70:
            source_match = None
            matched = False
            match_stage = "below_threshold"

        image_1_url, image_2_url = _build_image_urls(source_match.get("images") if source_match else None)

        enriched_record = {
            "name": custom_name,
            "day_type": custom["day_type"],
            "muscle_group": custom["muscle_group"],
            "source_id": source_match.get("id") if source_match else None,
            "source_name": source_match.get("name") if source_match else None,
            "force": source_match.get("force") if source_match else None,
            "level": source_match.get("level") if source_match else None,
            "mechanic": source_match.get("mechanic") if source_match else None,
            "equipment": source_match.get("equipment") if source_match else None,
            "category": source_match.get("category") if source_match else None,
            "primary_muscles": source_match.get("primaryMuscles") if source_match else [],
            "secondary_muscles": source_match.get("secondaryMuscles") if source_match else [],
            "instructions": source_match.get("instructions") if source_match else [],
            "image_1_url": image_1_url,
            "image_2_url": image_2_url,
            "video_url": "",
            "match_confidence": round(confidence, 2) if confidence is not None else None,
            "matched": matched,
        }
        enriched.append(enriched_record)

        report_rows.append(
            {
                "custom_name": custom_name,
                "source_name": enriched_record["source_name"],
                "matched": matched,
                "confidence": enriched_record["match_confidence"],
                "match_stage": match_stage,
            }
        )

        if not matched:
            unmatched.append(enriched_record)

    ENRICHED_PATH.write_text(json.dumps(enriched, indent=2), encoding="utf-8")
    UNMATCHED_PATH.write_text(json.dumps(unmatched, indent=2), encoding="utf-8")
    pd.DataFrame(report_rows).to_csv(REPORT_PATH, index=False)

    print(f"Enriched exercises: {len(enriched)}")
    print(f"Matched (>=85): {sum(1 for row in enriched if row['matched'])}")
    print(f"Needs review: {len(unmatched)}")
    print(f"Saved: {ENRICHED_PATH}, {UNMATCHED_PATH}, {REPORT_PATH}")


if __name__ == "__main__":
    enrich()
