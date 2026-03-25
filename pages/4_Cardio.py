from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from db import delete_latest_log, fetch_df, insert_cardio
from utils import bar_chart, trend_chart

st.title("🚴 Cardio Tracker")
st.caption("Track fat-loss supportive cardio, adherence, and calories burned.")

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
    c1, c2 = st.columns(2)
    with c1:
        log_date = st.date_input("Date", value=date.today())
        cardio_type = st.selectbox("Cardio Type", cardio_types)
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with c2:
        calories = st.number_input("Calories (optional)", min_value=0, max_value=3000, value=180)
        intensity = st.select_slider("Intensity", options=["Easy", "Moderate", "Hard"], value="Moderate")
        notes = st.text_input("Notes")

    submit = st.form_submit_button("Save Cardio")

if submit:
    insert_cardio(
        {
            "date": log_date.strftime("%Y-%m-%d"),
            "cardio_type": cardio_type,
            "duration_min": int(duration),
            "calories": int(calories),
            "intensity": intensity,
            "notes": notes,
        }
    )
    st.success("Cardio saved.")

cardio = fetch_df("SELECT * FROM cardio_logs ORDER BY date")
if cardio.empty:
    st.info("No cardio entries yet.")
else:
    cardio["date"] = pd.to_datetime(cardio["date"])
    weekly = cardio[cardio["date"] >= (pd.Timestamp.today() - pd.Timedelta(days=6))]
    total_week = int(weekly["duration_min"].sum())
    total_cal = int(weekly["calories"].fillna(0).sum())
    st.metric("This week cardio minutes", total_week)
    st.metric("This week cardio calories", total_cal)

    by_day = cardio.groupby("date", as_index=False).agg(duration_min=("duration_min", "sum"), calories=("calories", "sum"))
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(bar_chart(by_day, "date", "duration_min", "Cardio Minutes by Day", "#06b6d4"), use_container_width=True)
    with c2:
        st.plotly_chart(trend_chart(by_day, "date", "calories", "Cardio Calories Trend", "#ef4444"), use_container_width=True)

    st.dataframe(cardio.sort_values("date", ascending=False), use_container_width=True, hide_index=True)

if st.button("Delete latest cardio log", type="secondary"):
    delete_latest_log("cardio_logs")
    st.warning("Latest cardio entry deleted.")
