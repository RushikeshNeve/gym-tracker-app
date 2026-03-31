from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from db import fetch_df, get_challenge_export_df, get_dashboard_metrics, get_hydration_export_df, get_nutrition_export_df, get_setting
from utils import bar_chart, donut_chart, get_recent_activity, import_google_sheet_csv, metric_card, status_banner, trend_chart
from utils.calorie_logic import calculate_daily_energy_balance, get_weekly_energy_balance
from utils.challenge_logic import get_split_plan, get_today_snapshot
from utils.hydration_logic import get_daily_hydration, get_weekly_hydration
from utils.nutrition_logic import get_daily_nutrition, get_weekly_nutrition
from utils.profile_logic import calculate_target_calories, calculate_tdee
from utils.weekly_review import get_weekly_summary
from db import get_user_profile

st.title("Dashboard")

profile = get_user_profile()
snapshot = get_today_snapshot()
metrics = get_dashboard_metrics()
today_nutrition = get_daily_nutrition(date.today().isoformat())
today_hydration = get_daily_hydration(date.today().isoformat())
energy = calculate_daily_energy_balance(date.today().isoformat())
split_plan = get_split_plan()
total_completed = int(snapshot.get("total_completed", 0))
required_total = int(snapshot.get("required_total", 8))

weight_df = fetch_df("SELECT date, body_weight, waist FROM body_metrics ORDER BY date")
workouts = fetch_df("SELECT * FROM workout_logs ORDER BY date")
cardio = fetch_df("SELECT * FROM cardio_logs ORDER BY date")
challenge = get_challenge_export_df()
weekly_energy, weekly_energy_summary = get_weekly_energy_balance()

start_weight = None
latest_weight = metrics["latest_weight"]
if not weight_df.empty:
    start_weight = float(weight_df.iloc[0]["body_weight"]) if pd.notna(weight_df.iloc[0]["body_weight"]) else None
weight_change = (latest_weight - start_weight) if latest_weight is not None and start_weight is not None else None

row1 = st.columns(5)
cards1 = [
    ("Day", f"{snapshot['day_number']} / 75", snapshot["day_status"].title()),
    ("Maintenance", f"{energy['maintenance_calories']:.0f}", "TDEE"),
    ("Target", f"{energy['target_calories']:.0f}", "Goal calories"),
    ("Food today", f"{energy['food_calories']:.0f}", "Consumed"),
    ("Burned today", f"{energy['exercise_calories']:.0f}", "Exercise calories"),
]
for col, card in zip(row1, cards1):
    with col:
        metric_card(*card)

row2 = st.columns(5)
cards2 = [
    ("Net calories", f"{energy['net_calories']:.0f}", "Food minus burn"),
    ("Deficit/Surplus", f"{energy['deficit_or_surplus']:.0f}", energy["status"].replace("_", " ").title()),
    ("Protein", f"{today_nutrition['totals']['protein']:.0f} g", f"{today_nutrition['remaining']['protein']:.0f} g remaining"),
    ("Water", f"{today_hydration['total_ml'] / 1000:.2f} L", f"Target {today_hydration['target_liters']:.2f} L"),
    ("75 Hard", f"{snapshot['compliance_score']:.0f}%", f"{total_completed} of {required_total} tasks"),
]
for col, card in zip(row2, cards2):
    with col:
        metric_card(*card)

if snapshot["pending_tasks"]:
    status_banner("Pending tasks: " + ", ".join(snapshot["pending_tasks"]), "warning")
else:
    status_banner("Today is fully compliant and nutrition is logged cleanly.", "success")

st.markdown("### Energy Trends")
chart1, chart2 = st.columns(2)
with chart1:
    if not weekly_energy.empty:
        st.plotly_chart(bar_chart(weekly_energy, "date", "food_calories", "Daily calories consumed", "#2563eb"), use_container_width=True)
        st.plotly_chart(bar_chart(weekly_energy, "date", "exercise_calories", "Daily calories burned", "#ef4444"), use_container_width=True)
    else:
        st.info("No energy data yet.")
with chart2:
    if not weekly_energy.empty:
        st.plotly_chart(bar_chart(weekly_energy, "date", "net_calories", "Daily net calories", "#0f766e"), use_container_width=True)
        st.plotly_chart(bar_chart(weekly_energy, "date", "deficit_or_surplus", "Deficit trend", "#8b5cf6"), use_container_width=True)
    else:
        st.info("No energy data yet.")

st.markdown("### Progress Trends")
charts_left, charts_right = st.columns(2)
if not weight_df.empty:
    weight_df["date"] = pd.to_datetime(weight_df["date"])
with charts_left:
    if not weight_df.empty:
        st.plotly_chart(trend_chart(weight_df, "date", "body_weight", "Weight trend", "#f97316"), use_container_width=True)
        st.plotly_chart(trend_chart(weight_df, "date", "waist", "Waist trend", "#14b8a6"), use_container_width=True)
    else:
        st.info("No body metrics yet.")
with charts_right:
    weekly_nutrition, _ = get_weekly_nutrition()
    if not weekly_nutrition.empty:
        st.plotly_chart(bar_chart(weekly_nutrition, "date", "protein", "Protein trend", "#16a34a"), use_container_width=True)
        st.plotly_chart(bar_chart(weekly_nutrition, "date", "calories", "Weekly macro adherence", "#f97316"), use_container_width=True)
    else:
        st.info("No nutrition data yet.")

chart3, chart4 = st.columns(2)
with chart3:
    weekly_hydration = get_weekly_hydration()
    if not weekly_hydration.empty:
        st.plotly_chart(bar_chart(weekly_hydration, "date", "total_ml", "Water consumed", "#0ea5e9"), use_container_width=True)
    else:
        st.info("No hydration data yet.")
with chart4:
    if not challenge.empty:
        challenge["date"] = pd.to_datetime(challenge["date"])
        st.plotly_chart(trend_chart(challenge[["date", "compliance_score"]], "date", "compliance_score", "75 Hard compliance", "#f59e0b"), use_container_width=True)
        day_status_mix = challenge["day_status"].value_counts().rename_axis("day_status").reset_index(name="count")
        st.plotly_chart(donut_chart(day_status_mix, "day_status", "count", "Perfect vs incomplete days", ["#16a34a", "#f59e0b", "#dc2626"]), use_container_width=True)
    else:
        st.info("No challenge data yet.")

left, right = st.columns([1.1, 1])
week_summary = get_weekly_summary()
with left:
    st.markdown("### This Week Summary")
    summary_df = pd.DataFrame(
        [
            ["Weekly average deficit", round(weekly_energy_summary["weekly_average_deficit"], 1)],
            ["Estimated fat loss pace (kg/week)", round(weekly_energy_summary["estimated_fat_loss_kg_per_week"], 2)],
            ["Workout consistency", week_summary["workout_consistency"]],
            ["Outdoor consistency", week_summary["outdoor_workout_consistency"]],
            ["Perfect days", week_summary["perfect_days"]],
            ["Protein average", round(get_weekly_nutrition()[1]["avg_protein"], 1)],
            ["Planned workout", split_plan["today_plan"]],
        ],
        columns=["Metric", "Value"],
    )
    summary_df["Value"] = summary_df["Value"].astype(str)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
with right:
    st.markdown("### Profile Snapshot")
    profile_df = pd.DataFrame(
        [
            ["Weight", profile.get("current_weight_kg")],
            ["Height", profile.get("height_cm")],
            ["Activity", profile.get("activity_level")],
            ["Goal", profile.get("goal")],
            ["Desired deficit", profile.get("desired_deficit")],
            ["Calculated TDEE", round(calculate_tdee(profile), 1)],
            ["Calculated target", round(calculate_target_calories(profile), 1)],
        ],
        columns=["Field", "Value"],
    )
    profile_df["Value"] = profile_df["Value"].astype(str)
    st.dataframe(
        profile_df,
        use_container_width=True,
        hide_index=True,
    )

st.markdown("### Recent PRs")
recent_prs = fetch_df("SELECT date, exercise, weight, reps, new_pr FROM workout_logs WHERE new_pr IN ('PR','First') ORDER BY date DESC, id DESC LIMIT 10")
if recent_prs.empty:
    st.info("No PRs yet.")
else:
    st.dataframe(recent_prs, use_container_width=True, hide_index=True)

st.markdown("### Recent Activity")
st.dataframe(get_recent_activity(), use_container_width=True, hide_index=True)

with st.expander("Goal & Data Tools"):
    c1, c2 = st.columns(2)
    with c1:
        target_weight = st.number_input("Target body weight", min_value=30.0, max_value=250.0, value=float(get_setting("target_weight", 78)), step=0.5)
        if st.button("Save Target"):
            from db import set_setting

            set_setting("target_weight", target_weight)
            st.success("Target updated")
    with c2:
        up = st.file_uploader("Import Google Sheet CSV", type=["csv"])
        if up is not None and st.button("Import CSV"):
            imported = import_google_sheet_csv(up.read())
            st.success(f"Imported: {imported}")

    st.download_button("Export workouts CSV", fetch_df("SELECT * FROM workout_logs ORDER BY date DESC").to_csv(index=False).encode("utf-8"), file_name="workouts.csv")
    st.download_button("Export nutrition CSV", get_nutrition_export_df().to_csv(index=False).encode("utf-8"), file_name="nutrition_logs.csv")
    st.download_button("Export hydration CSV", get_hydration_export_df().to_csv(index=False).encode("utf-8"), file_name="hydration_logs.csv")
