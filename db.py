"""Database layer for the 75 Hard gym tracker app."""

from __future__ import annotations

import shutil
import sqlite3
from contextlib import closing
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import pandas as pd

from seed_exercises import EXERCISE_TUPLES
from seed_nutrition_data import DIET_PLAN_TEMPLATES, RECIPE_LIBRARY, SPICY_SNACK_NAMES, USER_PROFILE_DEFAULT

DB_PATH = Path("gym_tracker.db")
UPLOADS_DIR = Path("uploads/progress_photos")

DAY_TYPES = ["Push", "Pull", "Legs", "Upper", "Lower", "Cardio", "Full Body", "Active Recovery"]
WORKOUT_SESSION_TYPES = ["Workout 1", "Workout 2"]
MEAL_TYPES = ["Breakfast", "Lunch", "Dinner", "Snack", "Pre-workout", "Post-workout"]
PHOTO_TYPES = ["front", "side", "back"]
WEEKDAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
ACTIVITY_LEVELS = ["sedentary", "lightly_active", "moderately_active", "very_active"]
GOAL_TYPES = ["fat_loss", "maintenance", "recomp"]

DEFAULT_TARGETS = {
    "calorie_target": 2200,
    "protein_target": 180,
    "carbs_target": 200,
    "fats_target": 70,
    "fiber_target": 30,
    "water_target_liters": 4.0,
}


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def fetch_df(query: str, params: tuple[Any, ...] = ()) -> pd.DataFrame:
    with closing(get_conn()) as conn:
        return pd.read_sql_query(query, conn, params=params)


def _column_exists(conn: sqlite3.Connection, table_name: str, column_name: str) -> bool:
    rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return any(row["name"] == column_name for row in rows)


def _ensure_column(conn: sqlite3.Connection, table_name: str, column_name: str, column_sql: str) -> None:
    if not _column_exists(conn, table_name, column_name):
        conn.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_sql}")


def init_db() -> None:
    with closing(get_conn()) as conn:
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exercise TEXT UNIQUE NOT NULL,
                day_type TEXT NOT NULL,
                muscle_group TEXT NOT NULL
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS workout_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                day_type TEXT NOT NULL,
                exercise TEXT NOT NULL,
                muscle_group TEXT NOT NULL,
                weight REAL DEFAULT 0,
                reps INTEGER DEFAULT 0,
                sets INTEGER DEFAULT 1,
                volume REAL DEFAULT 0,
                near_failure INTEGER DEFAULT 0,
                new_pr TEXT DEFAULT '',
                notes TEXT DEFAULT ''
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS body_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                body_weight REAL,
                waist REAL,
                chest REAL,
                arms REAL,
                thigh REAL,
                body_fat_percent REAL,
                notes TEXT DEFAULT ''
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS cardio_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                cardio_type TEXT NOT NULL,
                duration_min INTEGER NOT NULL,
                calories INTEGER,
                intensity TEXT,
                notes TEXT DEFAULT ''
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS app_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS challenge_days (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT UNIQUE NOT NULL,
                challenge_day_number INTEGER,
                workout_1_completed INTEGER DEFAULT 0,
                workout_2_completed INTEGER DEFAULT 0,
                one_workout_outdoors INTEGER DEFAULT 0,
                followed_diet INTEGER DEFAULT 0,
                no_cheat_meals INTEGER DEFAULT 1,
                no_alcohol INTEGER DEFAULT 1,
                water_goal_completed INTEGER DEFAULT 0,
                progress_picture_taken INTEGER DEFAULT 0,
                body_weight REAL,
                steps INTEGER DEFAULT 0,
                sleep_hours REAL DEFAULT 0,
                mood TEXT DEFAULT '',
                energy_level INTEGER DEFAULT 0,
                notes TEXT DEFAULT '',
                selected_diet_plan TEXT DEFAULT '',
                diet_followed INTEGER DEFAULT 0,
                cheat_meal INTEGER DEFAULT 0,
                junk_food INTEGER DEFAULT 0,
                sugary_drinks INTEGER DEFAULT 0,
                hunger_level INTEGER DEFAULT 0,
                cravings_level INTEGER DEFAULT 0,
                binge_urge INTEGER DEFAULT 0,
                diet_notes TEXT DEFAULT '',
                day_status TEXT DEFAULT 'incomplete',
                compliance_score REAL DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS nutrition_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                meal_type TEXT NOT NULL,
                food_name TEXT NOT NULL,
                quantity TEXT DEFAULT '',
                calories REAL DEFAULT 0,
                protein REAL DEFAULT 0,
                carbs REAL DEFAULT 0,
                fats REAL DEFAULT 0,
                fiber REAL DEFAULT 0,
                notes TEXT DEFAULT '',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS user_profile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                age INTEGER,
                gender TEXT,
                height_cm REAL,
                current_weight_kg REAL,
                activity_level TEXT,
                goal TEXT,
                desired_deficit REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS recipe_library (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_name TEXT UNIQUE NOT NULL,
                meal_type TEXT NOT NULL,
                ingredients_json TEXT NOT NULL,
                steps_json TEXT NOT NULL,
                calories REAL DEFAULT 0,
                protein REAL DEFAULT 0,
                carbs REAL DEFAULT 0,
                fats REAL DEFAULT 0,
                fiber REAL DEFAULT 0,
                portion_note TEXT DEFAULT '',
                is_spicy INTEGER DEFAULT 0,
                is_vegetarian INTEGER DEFAULT 0,
                is_egg_based INTEGER DEFAULT 0,
                is_soya_based INTEGER DEFAULT 0
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS diet_plan_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day_name TEXT NOT NULL,
                meal_type TEXT NOT NULL,
                option_1 TEXT,
                option_2 TEXT,
                option_3 TEXT,
                option_4 TEXT,
                notes TEXT DEFAULT ''
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS exercise_calorie_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                activity_type TEXT NOT NULL,
                duration_min INTEGER DEFAULT 0,
                calories_burned REAL DEFAULT 0,
                source TEXT DEFAULT '',
                notes TEXT DEFAULT '',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS daily_targets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT UNIQUE NOT NULL,
                calorie_target REAL DEFAULT 2200,
                protein_target REAL DEFAULT 180,
                carbs_target REAL DEFAULT 200,
                fats_target REAL DEFAULT 70,
                fiber_target REAL DEFAULT 30,
                water_target_liters REAL DEFAULT 4,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS hydration_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount_ml INTEGER NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS progress_photos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                photo_type TEXT DEFAULT 'front',
                file_path TEXT NOT NULL,
                notes TEXT DEFAULT '',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS weekly_reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                week_start TEXT UNIQUE NOT NULL,
                what_went_well TEXT DEFAULT '',
                what_was_difficult TEXT DEFAULT '',
                focus_for_next_week TEXT DEFAULT '',
                notes TEXT DEFAULT '',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS favorite_meals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                meal_type TEXT NOT NULL,
                food_name TEXT NOT NULL,
                quantity TEXT DEFAULT '',
                calories REAL DEFAULT 0,
                protein REAL DEFAULT 0,
                carbs REAL DEFAULT 0,
                fats REAL DEFAULT 0,
                fiber REAL DEFAULT 0,
                notes TEXT DEFAULT '',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        _ensure_column(conn, "workout_logs", "session_type", "TEXT DEFAULT 'Workout 1'")
        _ensure_column(conn, "workout_logs", "is_outdoor", "INTEGER DEFAULT 0")
        _ensure_column(conn, "workout_logs", "duration_min", "INTEGER DEFAULT 0")
        _ensure_column(conn, "workout_logs", "start_time", "TEXT DEFAULT ''")
        _ensure_column(conn, "workout_logs", "end_time", "TEXT DEFAULT ''")
        _ensure_column(conn, "workout_logs", "session_notes", "TEXT DEFAULT ''")
        _ensure_column(conn, "workout_logs", "estimated_calories_burned", "REAL DEFAULT 0")

        _ensure_column(conn, "cardio_logs", "is_outdoor", "INTEGER DEFAULT 0")
        _ensure_column(conn, "cardio_logs", "distance_km", "REAL DEFAULT 0")
        _ensure_column(conn, "cardio_logs", "pace_text", "TEXT DEFAULT ''")
        _ensure_column(conn, "cardio_logs", "estimated_calories_burned", "REAL DEFAULT 0")

        _ensure_column(conn, "body_metrics", "hips", "REAL")
        _ensure_column(conn, "body_metrics", "neck", "REAL")
        _ensure_column(conn, "body_metrics", "thighs", "REAL")
        _ensure_column(conn, "body_metrics", "progress_notes", "TEXT DEFAULT ''")
        _ensure_column(conn, "nutrition_logs", "serving_count", "REAL DEFAULT 1")
        _ensure_column(conn, "nutrition_logs", "source_type", "TEXT DEFAULT 'manual'")
        _ensure_column(conn, "nutrition_logs", "recipe_name", "TEXT DEFAULT ''")

        conn.commit()


def seed_exercises() -> None:
    with closing(get_conn()) as conn:
        conn.executemany(
            "INSERT OR IGNORE INTO exercises (exercise, day_type, muscle_group) VALUES (?, ?, ?)",
            EXERCISE_TUPLES,
        )
        conn.commit()


def set_setting(key: str, value: Any) -> None:
    with closing(get_conn()) as conn:
        conn.execute(
            "INSERT INTO app_settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, str(value)),
        )
        conn.commit()


def get_setting(key: str, default: Any = None) -> Any:
    df = fetch_df("SELECT value FROM app_settings WHERE key = ?", (key,))
    if df.empty:
        return default
    return df.iloc[0]["value"]


def ensure_challenge_start_date() -> str:
    start_date = get_setting("challenge_start_date")
    if start_date:
        return str(start_date)
    challenge_start = (date.today() + timedelta(days=1)).isoformat()
    set_setting("challenge_start_date", challenge_start)
    return challenge_start


def get_user_profile() -> dict[str, Any]:
    profile = fetch_df("SELECT * FROM user_profile ORDER BY id DESC LIMIT 1")
    if profile.empty:
        return USER_PROFILE_DEFAULT.copy()
    return profile.iloc[0].to_dict()


def save_user_profile(payload: dict[str, Any]) -> None:
    current = fetch_df("SELECT id FROM user_profile ORDER BY id DESC LIMIT 1")
    with closing(get_conn()) as conn:
        if current.empty:
            conn.execute(
                """
                INSERT INTO user_profile (age, gender, height_cm, current_weight_kg, activity_level, goal, desired_deficit, updated_at)
                VALUES (:age, :gender, :height_cm, :current_weight_kg, :activity_level, :goal, :desired_deficit, CURRENT_TIMESTAMP)
                """,
                {**USER_PROFILE_DEFAULT, **payload},
            )
        else:
            conn.execute(
                """
                UPDATE user_profile
                SET age=:age, gender=:gender, height_cm=:height_cm, current_weight_kg=:current_weight_kg,
                    activity_level=:activity_level, goal=:goal, desired_deficit=:desired_deficit, updated_at=CURRENT_TIMESTAMP
                WHERE id=:id
                """,
                {"id": int(current.iloc[0]["id"]), **USER_PROFILE_DEFAULT, **payload},
            )
        conn.commit()


def get_recipe_library() -> pd.DataFrame:
    return fetch_df("SELECT * FROM recipe_library ORDER BY meal_type, recipe_name")


def get_recipe_by_name_db(recipe_name: str) -> dict[str, Any] | None:
    recipe = fetch_df("SELECT * FROM recipe_library WHERE recipe_name = ?", (recipe_name,))
    if recipe.empty:
        return None
    return recipe.iloc[0].to_dict()


def get_diet_plan_template(day_name: str) -> pd.DataFrame:
    return fetch_df("SELECT * FROM diet_plan_templates WHERE day_name = ? ORDER BY id", (day_name,))


def get_spicy_snack_presets() -> pd.DataFrame:
    placeholders = ",".join(["?"] * len(SPICY_SNACK_NAMES))
    return fetch_df(
        f"SELECT * FROM recipe_library WHERE recipe_name IN ({placeholders}) ORDER BY recipe_name",
        tuple(SPICY_SNACK_NAMES),
    )


def insert_exercise_calorie_log(payload: dict[str, Any]) -> None:
    with closing(get_conn()) as conn:
        conn.execute(
            """
            INSERT INTO exercise_calorie_logs (date, activity_type, duration_min, calories_burned, source, notes)
            VALUES (:date, :activity_type, :duration_min, :calories_burned, :source, :notes)
            """,
            payload,
        )
        conn.commit()


def get_daily_exercise_logs(log_date: str) -> pd.DataFrame:
    return fetch_df("SELECT * FROM exercise_calorie_logs WHERE date = ? ORDER BY created_at DESC, id DESC", (log_date,))


def get_exercises() -> pd.DataFrame:
    return fetch_df("SELECT * FROM exercises ORDER BY muscle_group, exercise")


def calculate_pr_status(exercise: str, weight: float, reps: int) -> str:
    history = fetch_df(
        "SELECT weight, reps FROM workout_logs WHERE exercise = ? ORDER BY date ASC, id ASC",
        (exercise,),
    )
    if history.empty:
        return "First"

    max_weight = history["weight"].max()
    max_weight_rows = history[history["weight"] == max_weight]
    best_reps_at_max = int(max_weight_rows["reps"].max()) if not max_weight_rows.empty else 0

    if weight > max_weight:
        return "PR"
    if weight == max_weight and reps > best_reps_at_max:
        return "PR"
    return ""


def insert_workout(payload: dict[str, Any]) -> str:
    pr_status = calculate_pr_status(payload["exercise"], float(payload["weight"]), int(payload["reps"]))
    volume = float(payload["weight"]) * int(payload["reps"]) * int(payload["sets"])

    data = {
        "date": payload["date"],
        "day_type": payload.get("day_type", "Full Body"),
        "exercise": payload["exercise"],
        "muscle_group": payload.get("muscle_group", "Full Body"),
        "weight": float(payload.get("weight", 0) or 0),
        "reps": int(payload.get("reps", 0) or 0),
        "sets": int(payload.get("sets", 1) or 1),
        "volume": volume,
        "near_failure": int(bool(payload.get("near_failure", False))),
        "new_pr": pr_status,
        "notes": payload.get("notes", "") or "",
        "session_type": payload.get("session_type", "Workout 1") or "Workout 1",
        "is_outdoor": int(bool(payload.get("is_outdoor", False))),
        "duration_min": int(payload.get("duration_min", 0) or 0),
        "start_time": payload.get("start_time", "") or "",
        "end_time": payload.get("end_time", "") or "",
        "session_notes": payload.get("session_notes", payload.get("notes", "")) or "",
        "estimated_calories_burned": float(payload.get("estimated_calories_burned", 0) or 0),
    }

    with closing(get_conn()) as conn:
        conn.execute(
            """
            INSERT INTO workout_logs (
                date, day_type, exercise, muscle_group, weight, reps, sets, volume, near_failure,
                new_pr, notes, session_type, is_outdoor, duration_min, start_time, end_time, session_notes, estimated_calories_burned
            )
            VALUES (
                :date, :day_type, :exercise, :muscle_group, :weight, :reps, :sets, :volume, :near_failure,
                :new_pr, :notes, :session_type, :is_outdoor, :duration_min, :start_time, :end_time, :session_notes, :estimated_calories_burned
            )
            """,
            data,
        )
        conn.commit()
    if data["estimated_calories_burned"] > 0:
        insert_exercise_calorie_log(
            {
                "date": data["date"],
                "activity_type": data["day_type"],
                "duration_min": data["duration_min"],
                "calories_burned": data["estimated_calories_burned"],
                "source": "workout",
                "notes": data["exercise"],
            }
        )
    return pr_status


def insert_body_metric(payload: dict[str, Any]) -> None:
    data = {
        "date": payload["date"],
        "body_weight": payload.get("body_weight"),
        "waist": payload.get("waist"),
        "chest": payload.get("chest"),
        "arms": payload.get("arms"),
        "thigh": payload.get("thigh", payload.get("thighs")),
        "body_fat_percent": payload.get("body_fat_percent"),
        "notes": payload.get("notes", "") or "",
        "hips": payload.get("hips"),
        "neck": payload.get("neck"),
        "thighs": payload.get("thighs", payload.get("thigh")),
        "progress_notes": payload.get("progress_notes", payload.get("notes", "")) or "",
    }
    with closing(get_conn()) as conn:
        conn.execute(
            """
            INSERT INTO body_metrics (
                date, body_weight, waist, chest, arms, thigh, body_fat_percent, notes, hips, neck, thighs, progress_notes
            )
            VALUES (
                :date, :body_weight, :waist, :chest, :arms, :thigh, :body_fat_percent, :notes, :hips, :neck, :thighs, :progress_notes
            )
            """,
            data,
        )
        conn.commit()


def insert_cardio(payload: dict[str, Any]) -> None:
    data = {
        "date": payload["date"],
        "cardio_type": payload.get("cardio_type", "Cardio"),
        "duration_min": int(payload.get("duration_min", 0) or 0),
        "calories": int(payload.get("calories", 0) or 0),
        "intensity": payload.get("intensity", "Moderate") or "Moderate",
        "notes": payload.get("notes", "") or "",
        "is_outdoor": int(bool(payload.get("is_outdoor", False))),
        "distance_km": float(payload.get("distance_km", 0) or 0),
        "pace_text": payload.get("pace_text", "") or "",
        "estimated_calories_burned": float(payload.get("estimated_calories_burned", payload.get("calories", 0)) or 0),
    }
    with closing(get_conn()) as conn:
        conn.execute(
            """
            INSERT INTO cardio_logs (
                date, cardio_type, duration_min, calories, intensity, notes, is_outdoor, distance_km, pace_text, estimated_calories_burned
            )
            VALUES (
                :date, :cardio_type, :duration_min, :calories, :intensity, :notes, :is_outdoor, :distance_km, :pace_text, :estimated_calories_burned
            )
            """,
            data,
        )
        conn.commit()
    if data["estimated_calories_burned"] > 0:
        insert_exercise_calorie_log(
            {
                "date": data["date"],
                "activity_type": data["cardio_type"],
                "duration_min": data["duration_min"],
                "calories_burned": data["estimated_calories_burned"],
                "source": "cardio",
                "notes": data["notes"],
            }
        )


def get_or_create_challenge_day(log_date: str) -> dict[str, Any]:
    row = fetch_df("SELECT * FROM challenge_days WHERE date = ?", (log_date,))
    if row.empty:
        save_challenge_day({"date": log_date})
        row = fetch_df("SELECT * FROM challenge_days WHERE date = ?", (log_date,))
    return row.iloc[0].to_dict()


def save_challenge_day(payload: dict[str, Any]) -> None:
    defaults = {
        "challenge_day_number": None,
        "workout_1_completed": 0,
        "workout_2_completed": 0,
        "one_workout_outdoors": 0,
        "followed_diet": 0,
        "no_cheat_meals": 1,
        "no_alcohol": 1,
        "water_goal_completed": 0,
        "progress_picture_taken": 0,
        "body_weight": None,
        "steps": 0,
        "sleep_hours": 0,
        "mood": "",
        "energy_level": 0,
        "notes": "",
        "selected_diet_plan": "",
        "diet_followed": 0,
        "cheat_meal": 0,
        "junk_food": 0,
        "sugary_drinks": 0,
        "hunger_level": 0,
        "cravings_level": 0,
        "binge_urge": 0,
        "diet_notes": "",
        "day_status": "incomplete",
        "compliance_score": 0,
    }
    data = {**defaults, **payload}
    bool_fields = [
        "workout_1_completed",
        "workout_2_completed",
        "one_workout_outdoors",
        "followed_diet",
        "no_cheat_meals",
        "no_alcohol",
        "water_goal_completed",
        "progress_picture_taken",
        "diet_followed",
        "cheat_meal",
        "junk_food",
        "sugary_drinks",
    ]
    for field in bool_fields:
        data[field] = int(bool(data.get(field, 0)))
    with closing(get_conn()) as conn:
        conn.execute(
            """
            INSERT INTO challenge_days (
                date, challenge_day_number, workout_1_completed, workout_2_completed, one_workout_outdoors,
                followed_diet, no_cheat_meals, no_alcohol, water_goal_completed, progress_picture_taken,
                body_weight, steps, sleep_hours, mood, energy_level, notes, selected_diet_plan, diet_followed,
                cheat_meal, junk_food, sugary_drinks, hunger_level, cravings_level, binge_urge, diet_notes,
                day_status, compliance_score, updated_at
            )
            VALUES (
                :date, :challenge_day_number, :workout_1_completed, :workout_2_completed, :one_workout_outdoors,
                :followed_diet, :no_cheat_meals, :no_alcohol, :water_goal_completed, :progress_picture_taken,
                :body_weight, :steps, :sleep_hours, :mood, :energy_level, :notes, :selected_diet_plan, :diet_followed,
                :cheat_meal, :junk_food, :sugary_drinks, :hunger_level, :cravings_level, :binge_urge, :diet_notes,
                :day_status, :compliance_score, CURRENT_TIMESTAMP
            )
            ON CONFLICT(date) DO UPDATE SET
                challenge_day_number=excluded.challenge_day_number,
                workout_1_completed=excluded.workout_1_completed,
                workout_2_completed=excluded.workout_2_completed,
                one_workout_outdoors=excluded.one_workout_outdoors,
                followed_diet=excluded.followed_diet,
                no_cheat_meals=excluded.no_cheat_meals,
                no_alcohol=excluded.no_alcohol,
                water_goal_completed=excluded.water_goal_completed,
                progress_picture_taken=excluded.progress_picture_taken,
                body_weight=excluded.body_weight,
                steps=excluded.steps,
                sleep_hours=excluded.sleep_hours,
                mood=excluded.mood,
                energy_level=excluded.energy_level,
                notes=excluded.notes,
                selected_diet_plan=excluded.selected_diet_plan,
                diet_followed=excluded.diet_followed,
                cheat_meal=excluded.cheat_meal,
                junk_food=excluded.junk_food,
                sugary_drinks=excluded.sugary_drinks,
                hunger_level=excluded.hunger_level,
                cravings_level=excluded.cravings_level,
                binge_urge=excluded.binge_urge,
                diet_notes=excluded.diet_notes,
                day_status=excluded.day_status,
                compliance_score=excluded.compliance_score,
                updated_at=CURRENT_TIMESTAMP
            """,
            data,
        )
        conn.commit()


def get_daily_targets(log_date: str) -> dict[str, Any]:
    row = fetch_df("SELECT * FROM daily_targets WHERE date = ?", (log_date,))
    if not row.empty:
        return row.iloc[0].to_dict()
    latest = fetch_df("SELECT * FROM daily_targets ORDER BY date DESC LIMIT 1")
    if not latest.empty:
        target = latest.iloc[0].to_dict()
        target["date"] = log_date
        return target
    return {"date": log_date, **DEFAULT_TARGETS}


def save_daily_targets(payload: dict[str, Any]) -> None:
    data = {"date": payload["date"], **DEFAULT_TARGETS, **payload}
    with closing(get_conn()) as conn:
        conn.execute(
            """
            INSERT INTO daily_targets (
                date, calorie_target, protein_target, carbs_target, fats_target, fiber_target, water_target_liters, updated_at
            )
            VALUES (
                :date, :calorie_target, :protein_target, :carbs_target, :fats_target, :fiber_target, :water_target_liters, CURRENT_TIMESTAMP
            )
            ON CONFLICT(date) DO UPDATE SET
                calorie_target=excluded.calorie_target,
                protein_target=excluded.protein_target,
                carbs_target=excluded.carbs_target,
                fats_target=excluded.fats_target,
                fiber_target=excluded.fiber_target,
                water_target_liters=excluded.water_target_liters,
                updated_at=CURRENT_TIMESTAMP
            """,
            data,
        )
        conn.commit()


def insert_nutrition_log(payload: dict[str, Any]) -> None:
    data = {
        "date": payload["date"],
        "meal_type": payload["meal_type"],
        "food_name": payload["food_name"],
        "quantity": payload.get("quantity", payload.get("portion_note", "1 serving")) or "1 serving",
        "calories": float(payload.get("calories", 0) or 0),
        "protein": float(payload.get("protein", 0) or 0),
        "carbs": float(payload.get("carbs", 0) or 0),
        "fats": float(payload.get("fats", 0) or 0),
        "fiber": float(payload.get("fiber", 0) or 0),
        "notes": payload.get("notes", "") or "",
        "serving_count": float(payload.get("serving_count", 1) or 1),
        "source_type": payload.get("source_type", "manual") or "manual",
        "recipe_name": payload.get("recipe_name", payload.get("food_name", "")) or "",
    }
    with closing(get_conn()) as conn:
        conn.execute(
            """
            INSERT INTO nutrition_logs (
                date, meal_type, food_name, quantity, calories, protein, carbs, fats, fiber, notes, serving_count, source_type, recipe_name
            )
            VALUES (
                :date, :meal_type, :food_name, :quantity, :calories, :protein, :carbs, :fats, :fiber, :notes, :serving_count, :source_type, :recipe_name
            )
            """,
            data,
        )
        conn.commit()


def update_nutrition_log(log_id: int, payload: dict[str, Any]) -> None:
    with closing(get_conn()) as conn:
        conn.execute(
            """
            UPDATE nutrition_logs
            SET meal_type=:meal_type, food_name=:food_name, quantity=:quantity, calories=:calories,
                protein=:protein, carbs=:carbs, fats=:fats, fiber=:fiber, notes=:notes,
                serving_count=:serving_count, source_type=:source_type, recipe_name=:recipe_name
            WHERE id=:id
            """,
            {"id": log_id, "serving_count": 1, "source_type": "manual", "recipe_name": payload.get("food_name", ""), **payload},
        )
        conn.commit()


def delete_nutrition_log(log_id: int) -> None:
    with closing(get_conn()) as conn:
        conn.execute("DELETE FROM nutrition_logs WHERE id = ?", (log_id,))
        conn.commit()


def copy_nutrition_logs(source_date: str, target_date: str) -> int:
    rows = fetch_df("SELECT * FROM nutrition_logs WHERE date = ? ORDER BY id", (source_date,))
    count = 0
    for _, row in rows.iterrows():
        insert_nutrition_log(
            {
                "date": target_date,
                "meal_type": row["meal_type"],
                "food_name": row["food_name"],
                "quantity": row["quantity"],
                "calories": row["calories"],
                "protein": row["protein"],
                "carbs": row["carbs"],
                "fats": row["fats"],
                "fiber": row["fiber"],
                "notes": row["notes"],
                "serving_count": row["serving_count"] if "serving_count" in row else 1,
                "source_type": row["source_type"] if "source_type" in row else "manual",
                "recipe_name": row["recipe_name"] if "recipe_name" in row else row["food_name"],
            }
        )
        count += 1
    return count


def insert_favorite_meal(payload: dict[str, Any]) -> None:
    with closing(get_conn()) as conn:
        conn.execute(
            """
            INSERT INTO favorite_meals (name, meal_type, food_name, quantity, calories, protein, carbs, fats, fiber, notes)
            VALUES (:name, :meal_type, :food_name, :quantity, :calories, :protein, :carbs, :fats, :fiber, :notes)
            ON CONFLICT(name) DO UPDATE SET
                meal_type=excluded.meal_type,
                food_name=excluded.food_name,
                quantity=excluded.quantity,
                calories=excluded.calories,
                protein=excluded.protein,
                carbs=excluded.carbs,
                fats=excluded.fats,
                fiber=excluded.fiber,
                notes=excluded.notes
            """,
            payload,
        )
        conn.commit()


def insert_hydration_log(payload: dict[str, Any]) -> None:
    with closing(get_conn()) as conn:
        conn.execute(
            "INSERT INTO hydration_logs (date, amount_ml) VALUES (:date, :amount_ml)",
            payload,
        )
        conn.commit()


def delete_hydration_log(log_id: int) -> None:
    with closing(get_conn()) as conn:
        conn.execute("DELETE FROM hydration_logs WHERE id = ?", (log_id,))
        conn.commit()


def save_progress_photo_file(uploaded_file: Any, log_date: str, photo_type: str) -> str:
    extension = Path(uploaded_file.name).suffix or ".jpg"
    target_dir = UPLOADS_DIR / log_date
    target_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%H%M%S")
    file_path = target_dir / f"{photo_type}_{timestamp}{extension}"
    with file_path.open("wb") as handle:
        shutil.copyfileobj(uploaded_file, handle)
    return str(file_path)


def insert_progress_photo(payload: dict[str, Any]) -> None:
    with closing(get_conn()) as conn:
        conn.execute(
            """
            INSERT INTO progress_photos (date, photo_type, file_path, notes)
            VALUES (:date, :photo_type, :file_path, :notes)
            """,
            payload,
        )
        conn.commit()


def get_progress_photos(log_date: str | None = None) -> pd.DataFrame:
    if log_date:
        return fetch_df("SELECT * FROM progress_photos WHERE date = ? ORDER BY created_at DESC", (log_date,))
    return fetch_df("SELECT * FROM progress_photos ORDER BY date DESC, created_at DESC")


def get_weekly_review(week_start: str) -> dict[str, Any]:
    review = fetch_df("SELECT * FROM weekly_reviews WHERE week_start = ?", (week_start,))
    if review.empty:
        return {
            "week_start": week_start,
            "what_went_well": "",
            "what_was_difficult": "",
            "focus_for_next_week": "",
            "notes": "",
        }
    return review.iloc[0].to_dict()


def save_weekly_review(payload: dict[str, Any]) -> None:
    with closing(get_conn()) as conn:
        conn.execute(
            """
            INSERT INTO weekly_reviews (week_start, what_went_well, what_was_difficult, focus_for_next_week, notes, updated_at)
            VALUES (:week_start, :what_went_well, :what_was_difficult, :focus_for_next_week, :notes, CURRENT_TIMESTAMP)
            ON CONFLICT(week_start) DO UPDATE SET
                what_went_well=excluded.what_went_well,
                what_was_difficult=excluded.what_was_difficult,
                focus_for_next_week=excluded.focus_for_next_week,
                notes=excluded.notes,
                updated_at=CURRENT_TIMESTAMP
            """,
            payload,
        )
        conn.commit()


def delete_latest_log(table_name: str) -> None:
    allowed = {
        "workout_logs",
        "body_metrics",
        "cardio_logs",
        "nutrition_logs",
        "hydration_logs",
        "progress_photos",
    }
    if table_name not in allowed:
        raise ValueError(f"Unsupported table: {table_name}")
    with closing(get_conn()) as conn:
        conn.execute(f"DELETE FROM {table_name} WHERE id = (SELECT MAX(id) FROM {table_name})")
        conn.commit()


def get_dashboard_metrics() -> dict[str, Any]:
    today = date.today()
    week_start = today - timedelta(days=6)

    workouts = fetch_df("SELECT * FROM workout_logs")
    cardio = fetch_df("SELECT * FROM cardio_logs")
    body = fetch_df("SELECT * FROM body_metrics ORDER BY date")
    challenge = fetch_df("SELECT * FROM challenge_days")

    if not workouts.empty:
        workouts["date"] = pd.to_datetime(workouts["date"])
        week_workouts = workouts[workouts["date"] >= pd.to_datetime(week_start)]
    else:
        week_workouts = pd.DataFrame()

    if not cardio.empty:
        cardio["date"] = pd.to_datetime(cardio["date"])
        week_cardio = cardio[cardio["date"] >= pd.to_datetime(week_start)]
    else:
        week_cardio = pd.DataFrame()

    lifting_days = (
        sorted(pd.to_datetime(workouts["date"]).dt.date.unique(), reverse=True)
        if not workouts.empty
        else []
    )
    streak = 0
    if lifting_days:
        cursor = today
        lifting_set = set(lifting_days)
        while cursor in lifting_set:
            streak += 1
            cursor = cursor - timedelta(days=1)

    weekly_workouts = int(week_workouts["date"].dt.date.nunique()) if not week_workouts.empty else 0
    weekly_volume = float(week_workouts["volume"].sum()) if not week_workouts.empty else 0
    weekly_prs = int((week_workouts["new_pr"].isin(["PR", "First"])).sum()) if not week_workouts.empty else 0
    cardio_mins = int(week_cardio["duration_min"].sum()) if not week_cardio.empty else 0
    cardio_cals = int(week_cardio["calories"].fillna(0).sum()) if not week_cardio.empty else 0
    latest_weight = float(body.iloc[-1]["body_weight"]) if not body.empty and pd.notna(body.iloc[-1]["body_weight"]) else None
    perfect_days = int((challenge["day_status"] == "perfect").sum()) if not challenge.empty else 0
    failed_days = int((challenge["day_status"] == "failed").sum()) if not challenge.empty else 0

    consistency_pct = min(100, int((weekly_workouts / 5) * 100))
    workout_score = min(40, weekly_workouts * 8)
    cardio_score = min(25, cardio_mins // 10 * 2)
    body_score = 20 if (not body.empty and pd.to_datetime(body.iloc[-1]["date"]).date() >= week_start) else 0
    pr_score = min(15, weekly_prs * 5)
    weekly_score = min(100, workout_score + cardio_score + body_score + pr_score)

    return {
        "streak": streak,
        "weekly_workouts": weekly_workouts,
        "weekly_volume": weekly_volume,
        "weekly_prs": weekly_prs,
        "cardio_mins": cardio_mins,
        "cardio_cals": cardio_cals,
        "latest_weight": latest_weight,
        "weekly_score": weekly_score,
        "consistency_pct": consistency_pct,
        "perfect_days": perfect_days,
        "failed_days": failed_days,
    }


def get_challenge_export_df() -> pd.DataFrame:
    return fetch_df("SELECT * FROM challenge_days ORDER BY date DESC")


def get_nutrition_export_df() -> pd.DataFrame:
    return fetch_df("SELECT * FROM nutrition_logs ORDER BY date DESC, id DESC")


def get_hydration_export_df() -> pd.DataFrame:
    return fetch_df("SELECT * FROM hydration_logs ORDER BY date DESC, id DESC")


def seed_sample_data() -> None:
    ensure_challenge_start_date()
    with closing(get_conn()) as conn:
        c = conn.cursor()
        existing = c.execute("SELECT COUNT(*) AS count FROM workout_logs").fetchone()["count"]
        if existing == 0:
            sample_workouts = [
                ("2026-03-16", "Push", "Incline Machine Press", "Upper Chest", 60, 10, 3, 1800, 1, "First", "Solid set", "Workout 1", 0, 55, "06:30", "07:25", "Morning lift"),
                ("2026-03-16", "Push", "Flat Dumbbell Press", "Chest", 30, 12, 3, 1080, 1, "First", "Controlled reps", "Workout 1", 0, 55, "06:30", "07:25", "Morning lift"),
                ("2026-03-16", "Push", "Shoulder Press", "Front Delts", 25, 10, 3, 750, 0, "First", "", "Workout 1", 0, 55, "06:30", "07:25", "Morning lift"),
                ("2026-03-20", "Pull", "Lat Pulldown", "Lats", 55, 10, 3, 1650, 1, "First", "", "Workout 1", 0, 50, "07:00", "07:50", "Pull day"),
                ("2026-03-24", "Push", "Incline Machine Press", "Upper Chest", 65, 8, 3, 1560, 1, "PR", "Heavier than last week", "Workout 1", 0, 60, "06:20", "07:20", "Push strength"),
                ("2026-03-24", "Push", "Flat Dumbbell Press", "Chest", 32.5, 10, 3, 975, 1, "PR", "Up in load", "Workout 1", 0, 60, "06:20", "07:20", "Push strength"),
            ]
            c.executemany(
                """
                INSERT INTO workout_logs (
                    date, day_type, exercise, muscle_group, weight, reps, sets, volume, near_failure, new_pr, notes,
                    session_type, is_outdoor, duration_min, start_time, end_time, session_notes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                sample_workouts,
            )

        existing_metrics = c.execute("SELECT COUNT(*) AS count FROM body_metrics").fetchone()["count"]
        if existing_metrics == 0:
            sample_metrics = [
                ("2026-03-17", 84.2, 92.0, 104.0, 36.0, 57.0, 22.5, "Baseline", 99.0, 38.0, 57.0, "Starting point"),
                ("2026-03-24", 83.6, 91.2, 103.5, 36.1, 56.8, 22.0, "Good week", 98.5, 37.8, 56.8, "Waist moving down"),
            ]
            c.executemany(
                """
                INSERT INTO body_metrics (
                    date, body_weight, waist, chest, arms, thigh, body_fat_percent, notes, hips, neck, thighs, progress_notes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                sample_metrics,
            )

        existing_cardio = c.execute("SELECT COUNT(*) AS count FROM cardio_logs").fetchone()["count"]
        if existing_cardio == 0:
            sample_cardio = [
                ("2026-03-18", "Incline Walking", 25, 220, "Moderate", "Post workout", 0, 2.2, "11:20 /km"),
                ("2026-03-22", "Outdoor Walk", 45, 260, "Moderate", "Evening walk", 1, 4.8, "09:15 /km"),
                ("2026-03-24", "Stairmaster", 15, 180, "Hard", "Finisher", 0, 0, ""),
            ]
            c.executemany(
                """
                INSERT INTO cardio_logs (
                    date, cardio_type, duration_min, calories, intensity, notes, is_outdoor, distance_km, pace_text
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                sample_cardio,
            )

        existing_profile = c.execute("SELECT COUNT(*) AS count FROM user_profile").fetchone()["count"]
        if existing_profile == 0:
            c.execute(
                """
                INSERT INTO user_profile (age, gender, height_cm, current_weight_kg, activity_level, goal, desired_deficit)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    USER_PROFILE_DEFAULT["age"],
                    USER_PROFILE_DEFAULT["gender"],
                    USER_PROFILE_DEFAULT["height_cm"],
                    USER_PROFILE_DEFAULT["current_weight_kg"],
                    USER_PROFILE_DEFAULT["activity_level"],
                    USER_PROFILE_DEFAULT["goal"],
                    USER_PROFILE_DEFAULT["desired_deficit"],
                ),
            )

        c.execute("DELETE FROM recipe_library WHERE recipe_name IN ('Chicken Rice Bowl', 'Chicken Roti Plate')")
        c.executemany(
            """
            INSERT OR REPLACE INTO recipe_library (
                recipe_name, meal_type, ingredients_json, steps_json, calories, protein, carbs, fats, fiber,
                portion_note, is_spicy, is_vegetarian, is_egg_based, is_soya_based
            )
            VALUES (
                :recipe_name, :meal_type, :ingredients_json, :steps_json, :calories, :protein, :carbs, :fats, :fiber,
                :portion_note, :is_spicy, :is_vegetarian, :is_egg_based, :is_soya_based
            )
            """,
            RECIPE_LIBRARY,
        )

        c.execute("DELETE FROM diet_plan_templates")
        c.executemany(
            """
            INSERT INTO diet_plan_templates (day_name, meal_type, option_1, option_2, option_3, option_4, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            DIET_PLAN_TEMPLATES,
        )

        existing_targets = c.execute("SELECT COUNT(*) AS count FROM daily_targets").fetchone()["count"]
        if existing_targets == 0:
            challenge_start = datetime.fromisoformat(ensure_challenge_start_date()).date()
            for offset in range(-1, 2):
                target_date = (challenge_start + timedelta(days=offset)).isoformat()
                c.execute(
                    """
                    INSERT INTO daily_targets (
                        date, calorie_target, protein_target, carbs_target, fats_target, fiber_target, water_target_liters
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        target_date,
                        2450,
                        185,
                        DEFAULT_TARGETS["carbs_target"],
                        DEFAULT_TARGETS["fats_target"],
                        DEFAULT_TARGETS["fiber_target"],
                        DEFAULT_TARGETS["water_target_liters"],
                    ),
                )

        existing_challenge = c.execute("SELECT COUNT(*) AS count FROM challenge_days").fetchone()["count"]
        if existing_challenge == 0:
            challenge_start = datetime.fromisoformat(ensure_challenge_start_date()).date()
            demo_days = [
                {
                    "date": (challenge_start - timedelta(days=2)).isoformat(),
                    "challenge_day_number": 1,
                    "workout_1_completed": 1,
                    "workout_2_completed": 1,
                    "one_workout_outdoors": 1,
                    "followed_diet": 1,
                    "diet_followed": 1,
                    "no_cheat_meals": 1,
                    "no_alcohol": 1,
                    "water_goal_completed": 1,
                    "progress_picture_taken": 1,
                    "body_weight": 84.0,
                    "steps": 11250,
                    "sleep_hours": 7.4,
                    "mood": "Focused",
                    "energy_level": 8,
                    "selected_diet_plan": "High protein calorie deficit",
                    "day_status": "perfect",
                    "compliance_score": 100,
                },
                {
                    "date": (challenge_start - timedelta(days=1)).isoformat(),
                    "challenge_day_number": 2,
                    "workout_1_completed": 1,
                    "workout_2_completed": 0,
                    "one_workout_outdoors": 1,
                    "followed_diet": 1,
                    "diet_followed": 1,
                    "no_cheat_meals": 1,
                    "no_alcohol": 1,
                    "water_goal_completed": 0,
                    "progress_picture_taken": 0,
                    "body_weight": 83.8,
                    "steps": 9050,
                    "sleep_hours": 6.8,
                    "mood": "Tired",
                    "energy_level": 6,
                    "selected_diet_plan": "High protein calorie deficit",
                    "day_status": "failed",
                    "compliance_score": 58,
                },
                {
                    "date": challenge_start.isoformat(),
                    "challenge_day_number": 3,
                    "workout_1_completed": 1,
                    "workout_2_completed": 0,
                    "one_workout_outdoors": 0,
                    "followed_diet": 1,
                    "diet_followed": 1,
                    "no_cheat_meals": 1,
                    "no_alcohol": 1,
                    "water_goal_completed": 0,
                    "progress_picture_taken": 0,
                    "body_weight": 83.6,
                    "steps": 6500,
                    "sleep_hours": 7.0,
                    "mood": "Locked in",
                    "energy_level": 7,
                    "selected_diet_plan": "High protein calorie deficit",
                    "day_status": "incomplete",
                    "compliance_score": 62,
                },
            ]
            for item in demo_days:
                c.execute(
                    """
                    INSERT INTO challenge_days (
                        date, challenge_day_number, workout_1_completed, workout_2_completed, one_workout_outdoors,
                        followed_diet, no_cheat_meals, no_alcohol, water_goal_completed, progress_picture_taken,
                        body_weight, steps, sleep_hours, mood, energy_level, selected_diet_plan, diet_followed,
                        day_status, compliance_score
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        item["date"],
                        item["challenge_day_number"],
                        item["workout_1_completed"],
                        item["workout_2_completed"],
                        item["one_workout_outdoors"],
                        item["followed_diet"],
                        item["no_cheat_meals"],
                        item["no_alcohol"],
                        item["water_goal_completed"],
                        item["progress_picture_taken"],
                        item["body_weight"],
                        item["steps"],
                        item["sleep_hours"],
                        item["mood"],
                        item["energy_level"],
                        item["selected_diet_plan"],
                        item["diet_followed"],
                        item["day_status"],
                        item["compliance_score"],
                    ),
                )

        existing_nutrition = c.execute("SELECT COUNT(*) AS count FROM nutrition_logs").fetchone()["count"]
        if existing_nutrition == 0:
            sample_nutrition = [
                ((date.today() - timedelta(days=1)).isoformat(), "Breakfast", "Overnight Oats Protein Bowl", "1 bowl", 430, 27, 58, 10, 9, "High protein", 1, "recipe", "Overnight Oats Protein Bowl"),
                ((date.today() - timedelta(days=1)).isoformat(), "Lunch", "Chicken Rice Bowl", "1 plate", 610, 48, 62, 15, 6, "Meal prep", 1, "recipe", "Chicken Rice Bowl"),
                (date.today().isoformat(), "Breakfast", "Egg Bhurji Toast Combo", "1 serving", 390, 26, 24, 20, 4, "Quick breakfast", 1, "recipe", "Egg Bhurji Toast Combo"),
                (date.today().isoformat(), "Post-workout", "Beast Life Whey Protein", "1 scoop", 120, 24, 3, 2, 0, "", 1, "quick_add", "Beast Life Whey Protein"),
            ]
            c.executemany(
                """
                INSERT INTO nutrition_logs (
                    date, meal_type, food_name, quantity, calories, protein, carbs, fats, fiber, notes, serving_count, source_type, recipe_name
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                sample_nutrition,
            )

        existing_hydration = c.execute("SELECT COUNT(*) AS count FROM hydration_logs").fetchone()["count"]
        if existing_hydration == 0:
            sample_hydration = [
                ((date.today() - timedelta(days=1)).isoformat(), 500),
                ((date.today() - timedelta(days=1)).isoformat(), 1000),
                (date.today().isoformat(), 500),
                (date.today().isoformat(), 250),
            ]
            c.executemany("INSERT INTO hydration_logs (date, amount_ml) VALUES (?, ?)", sample_hydration)

        existing_favorites = c.execute("SELECT COUNT(*) AS count FROM favorite_meals").fetchone()["count"]
        if existing_favorites == 0:
            sample_favorites = [
                ("Chicken Rice Bowl", "Lunch", "Chicken rice bowl", "1 plate", 610, 48, 62, 15, 6, "Reliable cut meal"),
                ("Whey + Banana", "Post-workout", "Whey + banana", "1 shake", 230, 26, 27, 2, 3, ""),
            ]
            c.executemany(
                """
                INSERT INTO favorite_meals (
                    name, meal_type, food_name, quantity, calories, protein, carbs, fats, fiber, notes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                sample_favorites,
            )

        existing_exercise_burn = c.execute("SELECT COUNT(*) AS count FROM exercise_calorie_logs").fetchone()["count"]
        if existing_exercise_burn == 0:
            c.executemany(
                """
                INSERT INTO exercise_calorie_logs (date, activity_type, duration_min, calories_burned, source, notes)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                [
                    (date.today().isoformat(), "Push", 55, 310, "workout", "Strength training estimate"),
                    (date.today().isoformat(), "Incline Walking", 25, 220, "cardio", "Post workout cardio"),
                ],
            )

        existing_photos = c.execute("SELECT COUNT(*) AS count FROM progress_photos").fetchone()["count"]
        if existing_photos == 0:
            challenge_start = datetime.fromisoformat(ensure_challenge_start_date()).date()
            c.executemany(
                """
                INSERT INTO progress_photos (date, photo_type, file_path, notes)
                VALUES (?, ?, ?, ?)
                """,
                [
                    ((challenge_start - timedelta(days=2)).isoformat(), "front", "uploads/progress_photos/sample/day1_front.jpg", "Sample metadata"),
                    (challenge_start.isoformat(), "side", "uploads/progress_photos/sample/day3_side.jpg", "Sample metadata"),
                ],
            )

        c.execute("INSERT OR IGNORE INTO app_settings (key, value) VALUES ('target_weight', '78')")
        c.execute("INSERT OR IGNORE INTO app_settings (key, value) VALUES ('diet_plan_name', 'High protein calorie deficit')")
        conn.commit()
