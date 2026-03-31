"""Build enriched exercise metadata with YouTube links and coaching notes."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import quote_plus

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from seed_exercises import EXERCISES

OUTPUT_PATH = Path("data/exercise_videos.json")

# Add direct links here as you curate exact videos for your most-used movements.
# matched=True only when an exercise has a direct YouTube watch URL.
CURATED_YOUTUBE_URLS: dict[str, str] = {
    # Example:
    # "Flat Dumbbell Press": "https://www.youtube.com/watch?v=VmB1G1K7v94",
}

INSTRUCTION_LIBRARY = {
    "Push": [
        "Set your shoulders down and back before each rep.",
        "Lower with control and keep wrists stacked.",
        "Drive through the full range without bouncing.",
    ],
    "Pull": [
        "Start each rep by bracing your core.",
        "Pull with elbows, not just your hands.",
        "Control the return phase for better tension.",
    ],
    "Legs": [
        "Keep your feet planted and stable.",
        "Move through a comfortable full range.",
        "Maintain a neutral spine while you lift.",
    ],
    "Full Body": [
        "Brace your core before every rep.",
        "Use smooth tempo and controlled breathing.",
        "Stop each set with 1–2 reps in reserve.",
    ],
    "Cardio": [
        "Start with an easy warm-up pace.",
        "Keep posture tall and breathing steady.",
        "Finish with a short cooldown.",
    ],
    "Upper": [
        "Keep your torso stable throughout each set.",
        "Control both lifting and lowering phases.",
        "Match your range of motion rep to rep.",
    ],
    "Lower": [
        "Keep knees tracking over toes.",
        "Push through your mid-foot and heel.",
        "Avoid rushing the eccentric phase.",
    ],
}

MISTAKE_LIBRARY = {
    "Push": ["Flaring elbows too hard.", "Dropping the weight too fast.", "Cutting range of motion short."],
    "Pull": ["Rounding your lower back.", "Using momentum to swing reps.", "Shrugging shoulders up every rep."],
    "Legs": ["Knees collapsing inward.", "Losing balance at the bottom.", "Lifting with your back first."],
    "Full Body": ["Holding your breath too long.", "Rushing reps without control.", "Ignoring setup between sets."],
    "Cardio": ["Starting too fast.", "Poor posture as fatigue builds.", "Skipping warm-up and cooldown."],
    "Upper": ["Going too heavy too soon.", "Uneven left-right movement.", "Shortening reps near fatigue."],
    "Lower": ["Letting hips shift side to side.", "Locking knees aggressively.", "Not controlling the lowering phase."],
}

TIP_LIBRARY = {
    "Push": "Think chest up, shoulders packed, and smooth reps.",
    "Pull": "Pause for a beat at peak contraction to feel your back work.",
    "Legs": "Record a side-view set to check depth and spine position.",
    "Full Body": "Stay technical first; intensity comes after good form.",
    "Cardio": "Use a pace you can sustain before pushing intensity.",
    "Upper": "Keep reps repeatable and progress load gradually.",
    "Lower": "Stability first, then add weight week by week.",
}


def build_youtube_search_url(exercise_name: str) -> str:
    return f"https://www.youtube.com/results?search_query={quote_plus(exercise_name + ' form')}"


def enrich_record(item: dict[str, str]) -> dict[str, object]:
    name = item["name"]
    day_type = item["day_type"]
    youtube_url = CURATED_YOUTUBE_URLS.get(name, "")

    return {
        "name": name,
        "day_type": day_type,
        "muscle_group": item["muscle_group"],
        "youtube_url": youtube_url,
        "youtube_search_url": build_youtube_search_url(name),
        "instructions": INSTRUCTION_LIBRARY.get(day_type, INSTRUCTION_LIBRARY["Full Body"]),
        "common_mistakes": MISTAKE_LIBRARY.get(day_type, MISTAKE_LIBRARY["Full Body"]),
        "tips": TIP_LIBRARY.get(day_type, TIP_LIBRARY["Full Body"]),
        "matched": bool(youtube_url),
    }


def main() -> None:
    enriched = [enrich_record(item) for item in EXERCISES]
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(enriched, indent=2), encoding="utf-8")
    matched_count = sum(1 for item in enriched if item["matched"])
    print(f"Wrote {len(enriched)} records to {OUTPUT_PATH} (curated matches: {matched_count}).")


if __name__ == "__main__":
    main()
