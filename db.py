"""Database layer for gym tracker app."""

from __future__ import annotations

import sqlite3
from contextlib import closing
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import pandas as pd

from seed_exercises import EXERCISE_TUPLES

DB_PATH = Path("gym_tracker.db")


DAY_TYPES = ["Push", "Pull", "Legs", "Upper", "Lower", "Cardio", "Full Body"]


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


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
        conn.commit()


def seed_exercises() -> None:
    with closing(get_conn()) as conn:
        conn.executemany(
            "INSERT OR IGNORE INTO exercises (exercise, day_type, muscle_group) VALUES (?, ?, ?)",
            EXERCISE_TUPLES,
        )
        conn.commit()


def seed_sample_data() -> None:
    with closing(get_conn()) as conn:
        c = conn.cursor()
        existing = c.execute("SELECT COUNT(*) AS count FROM workout_logs").fetchone()["count"]
        if existing > 0:
            return

        sample_workouts = [
            ("2026-03-16", "Push", "Incline Machine Press", "Upper Chest", 60, 10, 3, 1800, 1, "First", "Solid set"),
            ("2026-03-16", "Push", "Flat Dumbbell Press", "Chest", 30, 12, 3, 1080, 1, "First", "Controlled reps"),
            ("2026-03-16", "Push", "Shoulder Press", "Front Delts", 25, 10, 3, 750, 0, "First", ""),
            ("2026-03-16", "Push", "Cable Lateral Raise", "Side Delts", 10, 15, 3, 450, 1, "First", "Burn set"),
            ("2026-03-20", "Pull", "Lat Pulldown", "Lats", 55, 10, 3, 1650, 1, "First", ""),
            ("2026-03-24", "Push", "Incline Machine Press", "Upper Chest", 65, 8, 3, 1560, 1, "PR", "Heavier than last week"),
            ("2026-03-24", "Push", "Flat Dumbbell Press", "Chest", 32.5, 10, 3, 975, 1, "PR", "Up in load"),
        ]
        c.executemany(
            """
            INSERT INTO workout_logs (date, day_type, exercise, muscle_group, weight, reps, sets, volume, near_failure, new_pr, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            sample_workouts,
        )

        sample_metrics = [
            ("2026-03-17", 84.2, 92.0, 104.0, 36.0, 57.0, 22.5, "Baseline"),
            ("2026-03-24", 83.6, 91.2, 103.5, 36.1, 56.8, 22.0, "Good week"),
        ]
        c.executemany(
            """
            INSERT INTO body_metrics (date, body_weight, waist, chest, arms, thigh, body_fat_percent, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            sample_metrics,
        )

        sample_cardio = [
            ("2026-03-18", "Incline Walking", 25, 220, "Moderate", "Post workout"),
            ("2026-03-22", "Cycling", 30, 260, "Moderate", "Recovery"),
            ("2026-03-24", "Stairmaster", 15, 180, "Hard", "Finisher"),
        ]
        c.executemany(
            """
            INSERT INTO cardio_logs (date, cardio_type, duration_min, calories, intensity, notes)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            sample_cardio,
        )

        c.execute("INSERT OR IGNORE INTO app_settings (key, value) VALUES ('target_weight', '78')")
        conn.commit()


def fetch_df(query: str, params: tuple[Any, ...] = ()) -> pd.DataFrame:
    with closing(get_conn()) as conn:
        return pd.read_sql_query(query, conn, params=params)


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
    pr_status = calculate_pr_status(payload["exercise"], payload["weight"], payload["reps"])
    volume = payload["weight"] * payload["reps"] * payload["sets"]

    with closing(get_conn()) as conn:
        conn.execute(
            """
            INSERT INTO workout_logs (date, day_type, exercise, muscle_group, weight, reps, sets, volume, near_failure, new_pr, notes)
            VALUES (:date, :day_type, :exercise, :muscle_group, :weight, :reps, :sets, :volume, :near_failure, :new_pr, :notes)
            """,
            {
                **payload,
                "volume": volume,
                "near_failure": int(bool(payload.get("near_failure", False))),
                "new_pr": pr_status,
            },
        )
        conn.commit()
    return pr_status


def insert_body_metric(payload: dict[str, Any]) -> None:
    with closing(get_conn()) as conn:
        conn.execute(
            """
            INSERT INTO body_metrics (date, body_weight, waist, chest, arms, thigh, body_fat_percent, notes)
            VALUES (:date, :body_weight, :waist, :chest, :arms, :thigh, :body_fat_percent, :notes)
            """,
            payload,
        )
        conn.commit()


def insert_cardio(payload: dict[str, Any]) -> None:
    with closing(get_conn()) as conn:
        conn.execute(
            """
            INSERT INTO cardio_logs (date, cardio_type, duration_min, calories, intensity, notes)
            VALUES (:date, :cardio_type, :duration_min, :calories, :intensity, :notes)
            """,
            payload,
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


def delete_latest_log(table_name: str) -> None:
    with closing(get_conn()) as conn:
        conn.execute(f"DELETE FROM {table_name} WHERE id = (SELECT MAX(id) FROM {table_name})")
        conn.commit()


def get_dashboard_metrics() -> dict[str, Any]:
    today = date.today()
    week_start = today - timedelta(days=6)

    workouts = fetch_df("SELECT * FROM workout_logs")
    cardio = fetch_df("SELECT * FROM cardio_logs")
    body = fetch_df("SELECT * FROM body_metrics ORDER BY date")

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
    }
