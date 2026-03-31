from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {file_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_source_repo_path() -> Path:
    workspace_root = Path(__file__).resolve().parents[3]
    source_repo = workspace_root / "gym-tracker-app"
    if not source_repo.exists():
        raise FileNotFoundError("Expected sibling source repo at ../gym-tracker-app")
    return source_repo


def load_seed_sources():
    source_repo = get_source_repo_path()
    seed_exercises = _load_module("source_seed_exercises", source_repo / "seed_exercises.py")
    seed_nutrition = _load_module("source_seed_nutrition", source_repo / "seed_nutrition_data.py")
    return seed_exercises, seed_nutrition
