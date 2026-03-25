"""Utility helpers for analytics, charts, styling, and CSV mapping."""

from __future__ import annotations

from datetime import date
from io import StringIO

import pandas as pd
import plotly.express as px
import streamlit as st

from db import fetch_df, insert_body_metric, insert_cardio, insert_workout


def inject_css() -> None:
    st.markdown(
        """
        <style>
            .main {padding-top: 1rem;}
            .block-container {padding-top: 1.2rem; padding-bottom: 2rem;}
            .metric-card {
                background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
                border-radius: 16px;
                padding: 14px;
                color: #f9fafb;
                box-shadow: 0 8px 24px rgba(0,0,0,0.16);
                border: 1px solid rgba(255,255,255,0.06);
                min-height: 100px;
            }
            .metric-title {font-size: 0.85rem; opacity: 0.85; margin-bottom: 4px;}
            .metric-value {font-size: 1.45rem; font-weight: 700;}
            .pill {padding: 4px 10px; border-radius: 999px; background: #d1fae5; color: #065f46; font-size: 0.75rem;}
            .section-title {font-weight: 700; font-size: 1.1rem; margin: 0.6rem 0;}
            @media (max-width: 768px) {
                .block-container {padding-left: 0.8rem; padding-right: 0.8rem;}
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def metric_card(title: str, value: str, subtitle: str = "") -> None:
    st.markdown(
        f"""
        <div class='metric-card'>
          <div class='metric-title'>{title}</div>
          <div class='metric-value'>{value}</div>
          <div style='font-size:0.8rem;opacity:0.8'>{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def trend_chart(df: pd.DataFrame, x: str, y: str, title: str, color: str = "#22c55e"):
    if df.empty:
        return None
    fig = px.line(df.sort_values(x), x=x, y=y, markers=True, title=title)
    fig.update_traces(line=dict(color=color, width=3))
    fig.update_layout(height=300, margin=dict(l=10, r=10, t=40, b=10), template="plotly_dark")
    return fig


def bar_chart(df: pd.DataFrame, x: str, y: str, title: str, color: str = "#3b82f6"):
    if df.empty:
        return None
    fig = px.bar(df, x=x, y=y, title=title, color_discrete_sequence=[color])
    fig.update_layout(height=320, margin=dict(l=10, r=10, t=40, b=10), template="plotly_dark")
    return fig


def get_today_plan() -> str:
    order = ["Push", "Pull", "Legs", "Upper", "Lower"]
    idx = date.today().weekday() % len(order)
    return order[idx]


def get_recent_activity(limit: int = 10) -> pd.DataFrame:
    q = """
    SELECT date, day_type, exercise, weight, reps, sets, new_pr
    FROM workout_logs
    ORDER BY date DESC, id DESC
    LIMIT ?
    """
    return fetch_df(q, (limit,))


def import_google_sheet_csv(csv_bytes: bytes) -> dict[str, int]:
    text = csv_bytes.decode("utf-8", errors="ignore")
    df = pd.read_csv(StringIO(text))
    df.columns = [c.strip().lower() for c in df.columns]

    imported = {"workouts": 0, "body_metrics": 0, "cardio": 0}

    workout_columns = {"date", "day_type", "exercise", "muscle_group", "weight", "reps", "sets"}
    body_columns = {"date", "body_weight"}
    cardio_columns = {"date", "cardio_type", "duration_min"}

    if workout_columns.issubset(df.columns):
        w = df.copy()
        w["date"] = pd.to_datetime(w["date"], errors="coerce").dt.strftime("%Y-%m-%d")
        for _, row in w.dropna(subset=["date", "exercise"]).iterrows():
            payload = {
                "date": row.get("date"),
                "day_type": row.get("day_type", "Full Body") or "Full Body",
                "exercise": row.get("exercise", "Unknown"),
                "muscle_group": row.get("muscle_group", "Full Body") or "Full Body",
                "weight": float(row.get("weight", 0) or 0),
                "reps": int(row.get("reps", 0) or 0),
                "sets": int(row.get("sets", 1) or 1),
                "near_failure": bool(row.get("near_failure", False)),
                "notes": str(row.get("notes", "") or ""),
            }
            insert_workout(payload)
            imported["workouts"] += 1

    if body_columns.issubset(df.columns):
        b = df.copy()
        b["date"] = pd.to_datetime(b["date"], errors="coerce").dt.strftime("%Y-%m-%d")
        optional = ["waist", "chest", "arms", "thigh", "body_fat_percent", "notes"]
        for _, row in b.dropna(subset=["date", "body_weight"]).iterrows():
            payload = {
                "date": row.get("date"),
                "body_weight": float(row.get("body_weight", 0) or 0),
                "waist": float(row.get("waist", 0) or 0) if "waist" in b.columns else None,
                "chest": float(row.get("chest", 0) or 0) if "chest" in b.columns else None,
                "arms": float(row.get("arms", 0) or 0) if "arms" in b.columns else None,
                "thigh": float(row.get("thigh", 0) or 0) if "thigh" in b.columns else None,
                "body_fat_percent": float(row.get("body_fat_percent", 0) or 0)
                if "body_fat_percent" in b.columns
                else None,
                "notes": str(row.get("notes", "") or ""),
            }
            insert_body_metric(payload)
            imported["body_metrics"] += 1

    if cardio_columns.issubset(df.columns):
        c = df.copy()
        c["date"] = pd.to_datetime(c["date"], errors="coerce").dt.strftime("%Y-%m-%d")
        for _, row in c.dropna(subset=["date", "cardio_type"]).iterrows():
            payload = {
                "date": row.get("date"),
                "cardio_type": row.get("cardio_type", "Cardio"),
                "duration_min": int(row.get("duration_min", 0) or 0),
                "calories": int(row.get("calories", 0) or 0),
                "intensity": str(row.get("intensity", "Moderate") or "Moderate"),
                "notes": str(row.get("notes", "") or ""),
            }
            insert_cardio(payload)
            imported["cardio"] += 1

    return imported
