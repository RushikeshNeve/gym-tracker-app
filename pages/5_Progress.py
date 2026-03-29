from __future__ import annotations

import pandas as pd
import streamlit as st

from db import fetch_df
from utils import bar_chart, metric_card, trend_chart

st.title("Progress")
st.caption("Use this page for deeper analytics across training, body metrics, cardio, and challenge adherence.")

workouts = fetch_df("SELECT * FROM workout_logs ORDER BY date")
body = fetch_df("SELECT * FROM body_metrics ORDER BY date")
cardio = fetch_df("SELECT * FROM cardio_logs ORDER BY date")
challenge = fetch_df("SELECT date, day_status, compliance_score FROM challenge_days ORDER BY date")
nutrition = fetch_df("SELECT date, calories, protein FROM nutrition_logs ORDER BY date")

if workouts.empty and body.empty and cardio.empty and challenge.empty:
    st.info("Start logging activity to unlock analytics.")
    st.stop()

if not workouts.empty:
    workouts["date"] = pd.to_datetime(workouts["date"])
if not body.empty:
    body["date"] = pd.to_datetime(body["date"])
if not cardio.empty:
    cardio["date"] = pd.to_datetime(cardio["date"])
if not challenge.empty:
    challenge["date"] = pd.to_datetime(challenge["date"])
if not nutrition.empty:
    nutrition["date"] = pd.to_datetime(nutrition["date"])

available_dates = []
for df in [workouts, body, cardio, challenge, nutrition]:
    if not df.empty:
        available_dates.extend(df["date"].dt.date.tolist())
min_d, max_d = min(available_dates), max(available_dates)

colf1, colf2 = st.columns(2)
with colf1:
    date_range = st.date_input("Date range", value=(min_d, max_d), min_value=min_d, max_value=max_d)
with colf2:
    selected_day_types = []
    if not workouts.empty:
        selected_day_types = st.multiselect("Day Type", sorted(workouts["day_type"].dropna().unique()), default=list(sorted(workouts["day_type"].dropna().unique())))

filtered_workouts = workouts.copy()
if isinstance(date_range, tuple) and len(date_range) == 2:
    if not workouts.empty:
        filtered_workouts = filtered_workouts[(filtered_workouts["date"].dt.date >= date_range[0]) & (filtered_workouts["date"].dt.date <= date_range[1])]
    if not body.empty:
        body = body[(body["date"].dt.date >= date_range[0]) & (body["date"].dt.date <= date_range[1])]
    if not cardio.empty:
        cardio = cardio[(cardio["date"].dt.date >= date_range[0]) & (cardio["date"].dt.date <= date_range[1])]
    if not challenge.empty:
        challenge = challenge[(challenge["date"].dt.date >= date_range[0]) & (challenge["date"].dt.date <= date_range[1])]
    if not nutrition.empty:
        nutrition = nutrition[(nutrition["date"].dt.date >= date_range[0]) & (nutrition["date"].dt.date <= date_range[1])]
if selected_day_types and not filtered_workouts.empty:
    filtered_workouts = filtered_workouts[filtered_workouts["day_type"].isin(selected_day_types)]

c1, c2, c3, c4 = st.columns(4)
with c1:
    total_sessions = int(filtered_workouts["date"].dt.date.nunique()) if not filtered_workouts.empty else 0
    metric_card("Workout days", str(total_sessions), "Distinct training days")
with c2:
    total_volume = filtered_workouts["volume"].sum() if not filtered_workouts.empty else 0
    metric_card("Total volume", f"{total_volume:.0f}", "Selected range")
with c3:
    cardio_minutes = cardio["duration_min"].sum() if not cardio.empty else 0
    metric_card("Cardio minutes", f"{cardio_minutes:.0f}", "Selected range")
with c4:
    avg_compliance = challenge["compliance_score"].mean() if not challenge.empty else 0
    metric_card("Avg compliance", f"{avg_compliance:.0f}%", "Challenge score")

row1, row2 = st.columns(2)
with row1:
    if not filtered_workouts.empty:
        by_week = filtered_workouts.groupby(pd.Grouper(key="date", freq="W")).agg(volume=("volume", "sum"), entries=("id", "count")).reset_index()
        st.plotly_chart(bar_chart(by_week, "date", "entries", "Workout frequency by week", "#3b82f6"), use_container_width=True)
        st.plotly_chart(bar_chart(by_week, "date", "volume", "Volume by week", "#22c55e"), use_container_width=True)
    else:
        st.info("No workout data in current filter.")
with row2:
    if not nutrition.empty:
        nutrition_day = nutrition.groupby("date", as_index=False).sum(numeric_only=True)
        st.plotly_chart(trend_chart(nutrition_day, "date", "calories", "Calories over time", "#f97316"), use_container_width=True)
        st.plotly_chart(trend_chart(nutrition_day, "date", "protein", "Protein over time", "#16a34a"), use_container_width=True)
    else:
        st.info("No nutrition data in current filter.")

row3, row4 = st.columns(2)
with row3:
    if not body.empty:
        st.plotly_chart(trend_chart(body, "date", "body_weight", "Body weight changes", "#f97316"), use_container_width=True)
        if "waist" in body.columns:
            st.plotly_chart(trend_chart(body, "date", "waist", "Waist changes", "#14b8a6"), use_container_width=True)
    else:
        st.info("No body metrics in current filter.")
with row4:
    if not cardio.empty:
        cardio_week = cardio.groupby(pd.Grouper(key="date", freq="W")).agg(cardio_min=("duration_min", "sum")).reset_index()
        st.plotly_chart(bar_chart(cardio_week, "date", "cardio_min", "Cardio consistency", "#06b6d4"), use_container_width=True)
    else:
        st.info("No cardio data in current filter.")

if not challenge.empty:
    st.plotly_chart(trend_chart(challenge, "date", "compliance_score", "Compliance timeline", "#f59e0b"), use_container_width=True)
    st.dataframe(challenge.sort_values("date", ascending=False), use_container_width=True, hide_index=True)

st.markdown("### PR History")
if filtered_workouts.empty:
    st.info("No workout logs in current filter.")
else:
    pr_hist = filtered_workouts[filtered_workouts["new_pr"].isin(["PR", "First"])][["date", "exercise", "weight", "reps", "new_pr"]].sort_values("date", ascending=False)
    if pr_hist.empty:
        st.info("No PRs in current filters.")
    else:
        st.dataframe(pr_hist, use_container_width=True, hide_index=True)
