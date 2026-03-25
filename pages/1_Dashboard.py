from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from db import fetch_df, get_dashboard_metrics, get_setting, set_setting
from utils import bar_chart, get_recent_activity, get_today_plan, import_google_sheet_csv, metric_card, trend_chart

st.title("🏠 Dashboard")

metrics = get_dashboard_metrics()

c1, c2, c3, c4 = st.columns(4)
with c1:
    metric_card("🔥 Lifting Streak", f"{metrics['streak']} days", "Train today to keep it alive")
with c2:
    metric_card("✅ Weekly Workouts", str(metrics["weekly_workouts"]), "Target: 5 sessions")
with c3:
    metric_card("📦 Weekly Volume", f"{metrics['weekly_volume']:.0f}", "kg/lb total moved")
with c4:
    metric_card("🏆 PRs This Week", str(metrics["weekly_prs"]), "First logs + true PRs")

c5, c6, c7, c8 = st.columns(4)
with c5:
    metric_card("🚴 Cardio Minutes", str(metrics["cardio_mins"]), "Last 7 days")
with c6:
    latest_weight = "-" if metrics["latest_weight"] is None else f"{metrics['latest_weight']:.1f}"
    metric_card("⚖️ Latest Weight", latest_weight, "Most recent check-in")
with c7:
    metric_card("💯 Weekly Score", f"{metrics['weekly_score']}/100", f"Consistency {metrics['consistency_pct']}%")
with c8:
    target = float(get_setting("target_weight", 78))
    if metrics["latest_weight"]:
        diff = metrics["latest_weight"] - target
        progress = "On Track" if diff <= 0 else f"{diff:.1f} above target"
    else:
        progress = "Set first check-in"
    metric_card("🎯 Goal Progress", progress, f"Target {target:.1f}")

st.markdown("### 📊 Trends")

workouts = fetch_df("SELECT date, volume, exercise, new_pr FROM workout_logs ORDER BY date")
if not workouts.empty:
    workouts["date"] = pd.to_datetime(workouts["date"])
    daily_vol = workouts.groupby("date", as_index=False)["volume"].sum()
    st.plotly_chart(trend_chart(daily_vol, "date", "volume", "Daily Volume Trend", "#22c55e"), use_container_width=True)

body = fetch_df("SELECT date, body_weight, waist FROM body_metrics ORDER BY date")
cardio = fetch_df("SELECT date, duration_min FROM cardio_logs ORDER BY date")

col1, col2 = st.columns(2)
with col1:
    if not body.empty:
        body["date"] = pd.to_datetime(body["date"])
        st.plotly_chart(trend_chart(body, "date", "body_weight", "Body Weight Trend", "#f97316"), use_container_width=True)
    else:
        st.info("No body metrics yet.")
with col2:
    if not cardio.empty:
        cardio["date"] = pd.to_datetime(cardio["date"])
        by_day = cardio.groupby("date", as_index=False)["duration_min"].sum()
        st.plotly_chart(bar_chart(by_day, "date", "duration_min", "Cardio Trend (min)", "#06b6d4"), use_container_width=True)
    else:
        st.info("No cardio logs yet.")

left, right = st.columns([1.2, 1])
with left:
    st.markdown("### 🥇 Top Exercises by Volume")
    top = fetch_df("SELECT exercise, SUM(volume) AS total_volume FROM workout_logs GROUP BY exercise ORDER BY total_volume DESC LIMIT 8")
    if top.empty:
        st.info("Log workouts to see leaderboard.")
    else:
        st.plotly_chart(bar_chart(top, "exercise", "total_volume", "Top Exercises", "#a855f7"), use_container_width=True)

with right:
    st.markdown("### 📍 Today's Recommended Workout")
    day_type = get_today_plan()
    today_plan = fetch_df("SELECT exercise, muscle_group FROM exercises WHERE day_type = ? LIMIT 8", (day_type,))
    st.success(f"Today: **{day_type} Day**")
    st.dataframe(today_plan, use_container_width=True, hide_index=True)

st.markdown("### 🏅 Recent PRs")
recent_prs = fetch_df(
    "SELECT date, exercise, weight, reps, new_pr FROM workout_logs WHERE new_pr IN ('PR','First') ORDER BY date DESC, id DESC LIMIT 10"
)
if recent_prs.empty:
    st.info("No PRs yet. Time to push!")
else:
    st.dataframe(recent_prs, use_container_width=True, hide_index=True)

st.markdown("### 📰 Recent Activity")
st.dataframe(get_recent_activity(), use_container_width=True, hide_index=True)

with st.expander("⚙️ Goal & Data Tools"):
    c1, c2 = st.columns(2)
    with c1:
        target_weight = st.number_input("Target body weight", min_value=30.0, max_value=250.0, value=float(get_setting("target_weight", 78)), step=0.5)
        if st.button("Save Target"):
            set_setting("target_weight", target_weight)
            st.success("Target updated")
    with c2:
        up = st.file_uploader("Import Google Sheet CSV", type=["csv"])
        if up is not None and st.button("Import CSV"):
            imported = import_google_sheet_csv(up.read())
            st.success(f"Imported: {imported}")

    if st.button("Export workouts to CSV"):
        exp = fetch_df("SELECT * FROM workout_logs ORDER BY date DESC")
        st.download_button("Download workouts.csv", exp.to_csv(index=False).encode("utf-8"), file_name="workouts.csv")
