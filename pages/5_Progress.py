from __future__ import annotations

import pandas as pd
import streamlit as st

from db import fetch_df
from utils import bar_chart, trend_chart

st.title("📈 Progress Analytics")
st.caption("Strength progression, consistency, PR timeline, and body transformation.")

workouts = fetch_df("SELECT * FROM workout_logs ORDER BY date")
body = fetch_df("SELECT * FROM body_metrics ORDER BY date")
cardio = fetch_df("SELECT * FROM cardio_logs ORDER BY date")

if workouts.empty:
    st.info("No workouts logged yet.")
    st.stop()

workouts["date"] = pd.to_datetime(workouts["date"])

min_d, max_d = workouts["date"].min().date(), workouts["date"].max().date()
colf1, colf2, colf3, colf4 = st.columns(4)
with colf1:
    date_range = st.date_input("Date range", value=(min_d, max_d), min_value=min_d, max_value=max_d)
with colf2:
    day_type = st.multiselect("Day Type", sorted(workouts["day_type"].dropna().unique()), default=list(sorted(workouts["day_type"].dropna().unique())))
with colf3:
    muscle = st.multiselect("Muscle Group", sorted(workouts["muscle_group"].dropna().unique()), default=list(sorted(workouts["muscle_group"].dropna().unique())))
with colf4:
    exercise = st.multiselect("Exercise", sorted(workouts["exercise"].dropna().unique()), default=[])

filtered = workouts.copy()
if isinstance(date_range, tuple) and len(date_range) == 2:
    filtered = filtered[(filtered["date"].dt.date >= date_range[0]) & (filtered["date"].dt.date <= date_range[1])]
if day_type:
    filtered = filtered[filtered["day_type"].isin(day_type)]
if muscle:
    filtered = filtered[filtered["muscle_group"].isin(muscle)]
if exercise:
    filtered = filtered[filtered["exercise"].isin(exercise)]

if filtered.empty:
    st.warning("No data for selected filters.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Workouts", int(filtered["date"].dt.date.nunique()))
c2.metric("Total Entries", int(len(filtered)))
c3.metric("Total Volume", f"{filtered['volume'].sum():.0f}")
c4.metric("PR Count", int(filtered["new_pr"].isin(["PR", "First"]).sum()))

week_freq = filtered.groupby(pd.Grouper(key="date", freq="W")).agg(sessions=("id", "count"), volume=("volume", "sum"), prs=("new_pr", lambda x: x.isin(["PR", "First"]).sum())).reset_index()

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(week_freq, "date", "sessions", "Workout Frequency by Week", "#3b82f6"), use_container_width=True)
    st.plotly_chart(bar_chart(week_freq, "date", "volume", "Volume by Week", "#22c55e"), use_container_width=True)
with col2:
    st.plotly_chart(trend_chart(week_freq, "date", "prs", "PR Count Over Time", "#f59e0b"), use_container_width=True)
    strongest = filtered.groupby("exercise", as_index=False).agg(best_weight=("weight", "max"), best_reps=("reps", "max"), sessions=("id", "count"))
    st.dataframe(strongest.sort_values(["best_weight", "best_reps"], ascending=False).head(12), use_container_width=True, hide_index=True)

muscle_dist = filtered.groupby("muscle_group", as_index=False)["volume"].sum().sort_values("volume", ascending=False)
st.plotly_chart(bar_chart(muscle_dist, "muscle_group", "volume", "Muscle Group Distribution", "#a855f7"), use_container_width=True)

if not body.empty:
    body["date"] = pd.to_datetime(body["date"])
    b1, b2 = st.columns(2)
    with b1:
        st.plotly_chart(trend_chart(body, "date", "body_weight", "Body Weight Changes", "#f97316"), use_container_width=True)
    with b2:
        if "waist" in body.columns:
            st.plotly_chart(trend_chart(body, "date", "waist", "Waist Trend", "#14b8a6"), use_container_width=True)

if not cardio.empty:
    cardio["date"] = pd.to_datetime(cardio["date"])
    cweek = cardio.groupby(pd.Grouper(key="date", freq="W")).agg(cardio_min=("duration_min", "sum")).reset_index()
    st.plotly_chart(bar_chart(cweek, "date", "cardio_min", "Cardio Consistency (Weekly Minutes)", "#06b6d4"), use_container_width=True)

st.markdown("### PR History by Exercise")
pr_hist = filtered[filtered["new_pr"].isin(["PR", "First"])][["date", "exercise", "weight", "reps", "new_pr"]].sort_values("date", ascending=False)
if pr_hist.empty:
    st.info("No PR history in current filters.")
else:
    st.dataframe(pr_hist, use_container_width=True, hide_index=True)
