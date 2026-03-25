from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from db import delete_latest_log, fetch_df, insert_body_metric
from utils import trend_chart

st.title("📏 Body Metrics")
st.caption("Track body transformation and fat-loss check-ins.")

with st.form("body_form", clear_on_submit=True):
    log_date = st.date_input("Date", value=date.today())
    c1, c2, c3 = st.columns(3)
    with c1:
        body_weight = st.number_input("Body Weight", min_value=30.0, max_value=250.0, value=80.0, step=0.1)
        waist = st.number_input("Waist", min_value=40.0, max_value=180.0, value=90.0, step=0.1)
    with c2:
        chest = st.number_input("Chest", min_value=50.0, max_value=180.0, value=100.0, step=0.1)
        arms = st.number_input("Arms", min_value=15.0, max_value=70.0, value=35.0, step=0.1)
    with c3:
        thigh = st.number_input("Thigh", min_value=20.0, max_value=100.0, value=55.0, step=0.1)
        body_fat = st.number_input("Body Fat %", min_value=3.0, max_value=60.0, value=20.0, step=0.1)

    notes = st.text_area("Notes")
    submitted = st.form_submit_button("Save Body Check-in")

if submitted:
    insert_body_metric(
        {
            "date": log_date.strftime("%Y-%m-%d"),
            "body_weight": body_weight,
            "waist": waist,
            "chest": chest,
            "arms": arms,
            "thigh": thigh,
            "body_fat_percent": body_fat,
            "notes": notes,
        }
    )
    st.success("Body metrics saved.")

body = fetch_df("SELECT * FROM body_metrics ORDER BY date")
if body.empty:
    st.info("No body metrics yet.")
else:
    body["date"] = pd.to_datetime(body["date"])
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(trend_chart(body, "date", "body_weight", "Body Weight Trend", "#f97316"), use_container_width=True)
        st.plotly_chart(trend_chart(body, "date", "waist", "Waist Trend", "#14b8a6"), use_container_width=True)
    with c2:
        st.plotly_chart(trend_chart(body, "date", "body_fat_percent", "Body Fat % Trend", "#eab308"), use_container_width=True)
        st.dataframe(body.sort_values("date", ascending=False), use_container_width=True, hide_index=True)

if st.button("Delete latest body metric", type="secondary"):
    delete_latest_log("body_metrics")
    st.warning("Latest body metric deleted.")
