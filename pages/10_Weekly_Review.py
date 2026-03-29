from __future__ import annotations

from datetime import date, timedelta

import pandas as pd
import streamlit as st

from db import get_weekly_review, save_weekly_review
from utils import bar_chart, metric_card, status_banner
from utils.weekly_review import get_week_start, get_weekly_summary

st.title("Weekly Review")
default_week_start = get_week_start()
selected_week = st.date_input("Select week", value=default_week_start)
week_start = selected_week - timedelta(days=selected_week.weekday())
summary = get_weekly_summary(week_start)
review = get_weekly_review(week_start.isoformat())

c1, c2, c3, c4 = st.columns(4)
with c1:
    metric_card("Avg calories", f"{summary['avg_calories']:.0f}", "Daily average")
with c2:
    metric_card("Avg protein", f"{summary['avg_protein']:.0f} g", "Daily average")
with c3:
    metric_card("Water adherence", f"{summary['water_adherence_pct']:.0f}%", "Average target hit")
with c4:
    metric_card("Workout consistency", str(summary["workout_consistency"]), "Days trained this week")

c5, c6, c7, c8 = st.columns(4)
with c5:
    metric_card("Perfect days", str(summary["perfect_days"]), "Challenge wins")
with c6:
    metric_card("Incomplete days", str(summary["incomplete_days"]), "Still open or partial")
with c7:
    metric_card("Failed days", str(summary["failed_days"]), "Past misses")
with c8:
    metric_card("PRs", str(summary["prs"]), "New performance markers")

st.markdown("### Weekly Outcomes")
status_banner(
    f"Weight change: {summary['weight_change']:+.2f} • Waist change: {summary['waist_change']:+.2f} • Cardio minutes: {summary['cardio_minutes']}",
    "success" if summary["perfect_days"] >= 4 else "warning",
)

charts_col1, charts_col2 = st.columns(2)
with charts_col1:
    if not summary["nutrition_df"].empty:
        st.plotly_chart(bar_chart(summary["nutrition_df"], "date", "calories", "Calories by day", "#2563eb"), use_container_width=True)
    else:
        st.info("No nutrition logs this week.")
with charts_col2:
    if not summary["hydration_df"].empty:
        st.plotly_chart(bar_chart(summary["hydration_df"], "date", "total_ml", "Water intake by day", "#0ea5e9"), use_container_width=True)
    else:
        st.info("No hydration logs this week.")

if not summary["challenge_df"].empty:
    challenge_counts = (
        summary["challenge_df"]["day_status"]
        .value_counts()
        .rename_axis("day_status")
        .reset_index(name="count")
    )
    st.plotly_chart(bar_chart(challenge_counts, "day_status", "count", "Perfect vs incomplete vs failed", "#f97316"), use_container_width=True)

st.markdown("### Reflection")
with st.form("weekly_review_form"):
    what_went_well = st.text_area("What went well", value=review.get("what_went_well", ""))
    what_was_difficult = st.text_area("What was difficult", value=review.get("what_was_difficult", ""))
    focus_for_next_week = st.text_area("Focus for next week", value=review.get("focus_for_next_week", ""))
    notes = st.text_area("Weekly notes", value=review.get("notes", ""))
    submitted = st.form_submit_button("Save Weekly Review")
if submitted:
    save_weekly_review(
        {
            "week_start": week_start.isoformat(),
            "what_went_well": what_went_well,
            "what_was_difficult": what_was_difficult,
            "focus_for_next_week": focus_for_next_week,
            "notes": notes,
        }
    )
    st.success("Weekly review saved.")
