"""Utility helpers for analytics, charts, styling, and CSV mapping."""

from __future__ import annotations

from datetime import date
from io import StringIO
from typing import Any

import pandas as pd
import plotly.express as px
import streamlit as st

from db import fetch_df, insert_body_metric, insert_cardio, insert_workout


def inject_css() -> None:
    st.markdown(
        """
        <style>
            .main {padding-top: 0.6rem;}
            .block-container {padding-top: 1rem; padding-bottom: 2rem; max-width: 1180px;}
            .metric-card, .section-card, .summary-card {
                background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
                border-radius: 18px;
                padding: 16px;
                color: #0f172a;
                box-shadow: 0 12px 32px rgba(15, 23, 42, 0.08);
                border: 1px solid rgba(148, 163, 184, 0.18);
                min-height: 100px;
                margin-bottom: 0.75rem;
            }
            .metric-title {font-size: 0.8rem; color: #475569; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.04em;}
            .metric-value {font-size: 1.55rem; font-weight: 700; color: #0f172a;}
            .metric-subtitle {font-size: 0.85rem; color: #64748b;}
            .chip {
                display: inline-block;
                padding: 4px 10px;
                border-radius: 999px;
                font-size: 0.75rem;
                font-weight: 600;
                margin-right: 0.35rem;
                margin-bottom: 0.35rem;
            }
            .chip-success {background: #dcfce7; color: #166534;}
            .chip-warn {background: #fef3c7; color: #92400e;}
            .chip-danger {background: #fee2e2; color: #991b1b;}
            .chip-neutral {background: #e2e8f0; color: #334155;}
            .banner {
                border-radius: 16px;
                padding: 14px 16px;
                margin-bottom: 0.85rem;
                font-weight: 600;
            }
            .banner-success {background: #dcfce7; color: #166534; border: 1px solid #86efac;}
            .banner-warning {background: #fef3c7; color: #92400e; border: 1px solid #fcd34d;}
            .banner-danger {background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5;}
            .today-hero {
                background: radial-gradient(circle at top left, #e0f2fe, #ffffff 50%, #fef3c7 100%);
                border-radius: 24px;
                padding: 20px;
                border: 1px solid rgba(148, 163, 184, 0.2);
                box-shadow: 0 16px 40px rgba(15, 23, 42, 0.08);
                margin-bottom: 1rem;
            }
            .hero-day {font-size: 2rem; font-weight: 800; color: #0f172a;}
            .hero-subtitle {font-size: 0.95rem; color: #475569; margin-top: 0.25rem;}
            @media (max-width: 768px) {
                .block-container {padding-left: 0.8rem; padding-right: 0.8rem;}
                .hero-day {font-size: 1.6rem;}
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
          <div class='metric-subtitle'>{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_card(title: str, content: str) -> None:
    st.markdown(
        f"""
        <div class='section-card'>
          <div class='metric-title'>{title}</div>
          <div style='font-size:0.95rem;color:#1e293b;'>{content}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_banner(message: str, tone: str = "warning") -> None:
    tone_class = {
        "success": "banner-success",
        "warning": "banner-warning",
        "danger": "banner-danger",
    }.get(tone, "banner-warning")
    st.markdown(f"<div class='banner {tone_class}'>{message}</div>", unsafe_allow_html=True)


def chip(label: str, tone: str = "neutral") -> str:
    tone_class = {
        "success": "chip-success",
        "warn": "chip-warn",
        "danger": "chip-danger",
        "neutral": "chip-neutral",
    }.get(tone, "chip-neutral")
    return f"<span class='chip {tone_class}'>{label}</span>"


def render_chip_row(labels: list[tuple[str, str]]) -> None:
    html = "".join(chip(label, tone) for label, tone in labels)
    st.markdown(html, unsafe_allow_html=True)


def progress_block(label: str, value: float, target: float, color: str = "#2563eb") -> None:
    ratio = 0 if target <= 0 else min(1.0, value / target)
    st.markdown(f"**{label}** {value:.0f} / {target:.0f}")
    st.progress(ratio, text=f"{ratio * 100:.0f}%")


def render_today_hero(day_label: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class='today-hero'>
          <div class='hero-day'>{day_label}</div>
          <div class='hero-subtitle'>{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def trend_chart(df: pd.DataFrame, x: str, y: str, title: str, color: str = "#22c55e"):
    if df.empty:
        return None
    fig = px.line(df.sort_values(x), x=x, y=y, markers=True, title=title)
    fig.update_traces(line=dict(color=color, width=3))
    fig.update_layout(height=300, margin=dict(l=10, r=10, t=40, b=10), template="plotly_white")
    return fig


def bar_chart(df: pd.DataFrame, x: str, y: str, title: str, color: str = "#3b82f6"):
    if df.empty:
        return None
    fig = px.bar(df, x=x, y=y, title=title, color_discrete_sequence=[color])
    fig.update_layout(height=320, margin=dict(l=10, r=10, t=40, b=10), template="plotly_white")
    return fig


def donut_chart(df: pd.DataFrame, names: str, values: str, title: str, color_sequence: list[str] | None = None):
    if df.empty:
        return None
    fig = px.pie(df, names=names, values=values, hole=0.6, title=title, color_discrete_sequence=color_sequence)
    fig.update_layout(height=320, margin=dict(l=10, r=10, t=40, b=10), template="plotly_white")
    return fig


def get_today_plan() -> str:
    order = ["Push", "Pull", "Legs", "Cardio / Outdoor", "Active Recovery"]
    idx = date.today().weekday() % len(order)
    return order[idx]


def get_recent_activity(limit: int = 10) -> pd.DataFrame:
    q = """
    SELECT date, day_type, exercise, weight, reps, sets, new_pr, session_type, is_outdoor
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
            insert_workout(
                {
                    "date": row.get("date"),
                    "day_type": row.get("day_type", "Full Body") or "Full Body",
                    "exercise": row.get("exercise", "Unknown"),
                    "muscle_group": row.get("muscle_group", "Full Body") or "Full Body",
                    "weight": float(row.get("weight", 0) or 0),
                    "reps": int(row.get("reps", 0) or 0),
                    "sets": int(row.get("sets", 1) or 1),
                    "near_failure": bool(row.get("near_failure", False)),
                    "notes": str(row.get("notes", "") or ""),
                    "session_type": str(row.get("session_type", "Workout 1") or "Workout 1"),
                    "is_outdoor": bool(row.get("is_outdoor", False)),
                    "duration_min": int(row.get("duration_min", 0) or 0),
                    "start_time": str(row.get("start_time", "") or ""),
                    "end_time": str(row.get("end_time", "") or ""),
                    "session_notes": str(row.get("session_notes", row.get("notes", "")) or ""),
                }
            )
            imported["workouts"] += 1

    if body_columns.issubset(df.columns):
        b = df.copy()
        b["date"] = pd.to_datetime(b["date"], errors="coerce").dt.strftime("%Y-%m-%d")
        for _, row in b.dropna(subset=["date", "body_weight"]).iterrows():
            insert_body_metric(
                {
                    "date": row.get("date"),
                    "body_weight": float(row.get("body_weight", 0) or 0),
                    "waist": float(row.get("waist", 0) or 0) if "waist" in b.columns else None,
                    "chest": float(row.get("chest", 0) or 0) if "chest" in b.columns else None,
                    "arms": float(row.get("arms", 0) or 0) if "arms" in b.columns else None,
                    "thigh": float(row.get("thigh", 0) or 0) if "thigh" in b.columns else None,
                    "body_fat_percent": float(row.get("body_fat_percent", 0) or 0) if "body_fat_percent" in b.columns else None,
                    "hips": float(row.get("hips", 0) or 0) if "hips" in b.columns else None,
                    "neck": float(row.get("neck", 0) or 0) if "neck" in b.columns else None,
                    "thighs": float(row.get("thighs", row.get("thigh", 0)) or 0) if "thighs" in b.columns or "thigh" in b.columns else None,
                    "notes": str(row.get("notes", "") or ""),
                    "progress_notes": str(row.get("progress_notes", row.get("notes", "")) or ""),
                }
            )
            imported["body_metrics"] += 1

    if cardio_columns.issubset(df.columns):
        c = df.copy()
        c["date"] = pd.to_datetime(c["date"], errors="coerce").dt.strftime("%Y-%m-%d")
        for _, row in c.dropna(subset=["date", "cardio_type"]).iterrows():
            insert_cardio(
                {
                    "date": row.get("date"),
                    "cardio_type": row.get("cardio_type", "Cardio"),
                    "duration_min": int(row.get("duration_min", 0) or 0),
                    "calories": int(row.get("calories", 0) or 0),
                    "intensity": str(row.get("intensity", "Moderate") or "Moderate"),
                    "notes": str(row.get("notes", "") or ""),
                    "is_outdoor": bool(row.get("is_outdoor", False)),
                    "distance_km": float(row.get("distance_km", 0) or 0),
                    "pace_text": str(row.get("pace_text", "") or ""),
                }
            )
            imported["cardio"] += 1

    return imported
