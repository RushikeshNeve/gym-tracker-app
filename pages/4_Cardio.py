from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from db import delete_latest_log, fetch_df, get_user_profile, insert_cardio
from utils import bar_chart, metric_card, status_banner, trend_chart
from utils.calorie_logic import estimate_calories_burned

st.title("Cardio")
st.caption("Track cardio sessions that support fat loss and the outdoor-workout rule.")

cardio_types = [
    "Treadmill Running",
    "Incline Walking",
    "Cycling",
    "Stairmaster",
    "Rowing Machine",
    "Elliptical",
    "Jump Rope",
    "Outdoor Walk",
    "Outdoor Run",
]

with st.form("cardio_form", clear_on_submit=True):
    profile = get_user_profile()
    c1, c2 = st.columns(2)
    with c1:
        log_date = st.date_input("Date", value=date.today())
        cardio_type = st.selectbox("Cardio Type", cardio_types)
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
        distance = st.number_input("Distance (km)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    with c2:
        calories = st.number_input("Calories", min_value=0, max_value=3000, value=180)
        intensity = st.select_slider("Intensity", options=["Easy", "Moderate", "Hard"], value="Moderate")
        is_outdoor = st.toggle("Outdoor session", value="Outdoor" in cardio_type)
        pace = st.text_input("Pace", value="")
        notes = st.text_input("Notes")

    submit = st.form_submit_button("Save Cardio")

if submit:
    estimated_burn = estimate_calories_burned(cardio_type, int(duration), float(profile.get("current_weight_kg", 0) or 0))
    insert_cardio(
        {
            "date": log_date.strftime("%Y-%m-%d"),
            "cardio_type": cardio_type,
            "duration_min": int(duration),
            "calories": int(calories),
            "intensity": intensity,
            "notes": notes,
            "is_outdoor": is_outdoor,
            "distance_km": distance,
            "pace_text": pace,
            "estimated_calories_burned": estimated_burn,
        }
    )
    st.success(f"Cardio saved. Estimated burn: {estimated_burn:.0f} kcal.")

cardio = fetch_df("SELECT * FROM cardio_logs ORDER BY date")
if cardio.empty:
    st.info("No cardio entries yet.")
else:
    cardio["date"] = pd.to_datetime(cardio["date"])
    weekly = cardio[cardio["date"] >= (pd.Timestamp.today() - pd.Timedelta(days=6))]
    total_week = int(weekly["duration_min"].sum())
    total_cal = int(weekly["calories"].fillna(0).sum())
    outdoor_count = int(weekly["is_outdoor"].fillna(0).sum())
    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Weekly cardio", str(total_week), "Minutes in last 7 days")
    with c2:
        metric_card("Weekly calories", str(total_cal), "Estimated burn")
    with c3:
        metric_card("Outdoor sessions", str(outdoor_count), "Rule-supporting sessions")

    by_day = cardio.groupby("date", as_index=False).agg(duration_min=("duration_min", "sum"), calories=("calories", "sum"))
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(bar_chart(by_day, "date", "duration_min", "Cardio minutes by day", "#06b6d4"), use_container_width=True)
    with c2:
        st.plotly_chart(trend_chart(by_day, "date", "calories", "Cardio calories trend", "#ef4444"), use_container_width=True)

    if outdoor_count > 0:
        status_banner("You have outdoor cardio entries that can help satisfy the outdoor workout requirement.", "success")
    else:
        status_banner("No outdoor cardio logged this week yet.", "warning")

    st.dataframe(cardio.sort_values("date", ascending=False), use_container_width=True, hide_index=True)

if st.button("Delete latest cardio log", type="secondary"):
    delete_latest_log("cardio_logs")
    st.warning("Latest cardio entry deleted.")
