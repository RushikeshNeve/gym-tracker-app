from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from db import delete_latest_log, fetch_df, insert_body_metric
from utils import metric_card, status_banner, trend_chart

st.title("Body Metrics")
st.caption("Track body composition changes that support fat loss and accountability.")

with st.form("body_form", clear_on_submit=True):
    log_date = st.date_input("Date", value=date.today())
    c1, c2, c3 = st.columns(3)
    with c1:
        body_weight = st.number_input("Body Weight", min_value=30.0, max_value=250.0, value=80.0, step=0.1)
        waist = st.number_input("Waist", min_value=40.0, max_value=180.0, value=90.0, step=0.1)
        hips = st.number_input("Hips", min_value=40.0, max_value=180.0, value=98.0, step=0.1)
    with c2:
        chest = st.number_input("Chest", min_value=50.0, max_value=180.0, value=100.0, step=0.1)
        arms = st.number_input("Arms", min_value=15.0, max_value=70.0, value=35.0, step=0.1)
        neck = st.number_input("Neck", min_value=20.0, max_value=70.0, value=38.0, step=0.1)
    with c3:
        thighs = st.number_input("Thighs", min_value=20.0, max_value=100.0, value=55.0, step=0.1)
        body_fat = st.number_input("Body Fat %", min_value=3.0, max_value=60.0, value=20.0, step=0.1)
    notes = st.text_area("Progress notes")
    submitted = st.form_submit_button("Save Body Check-in")

if submitted:
    insert_body_metric(
        {
            "date": log_date.strftime("%Y-%m-%d"),
            "body_weight": body_weight,
            "waist": waist,
            "hips": hips,
            "chest": chest,
            "arms": arms,
            "neck": neck,
            "thigh": thighs,
            "thighs": thighs,
            "body_fat_percent": body_fat,
            "notes": notes,
            "progress_notes": notes,
        }
    )
    st.success("Body metrics saved.")

body = fetch_df("SELECT * FROM body_metrics ORDER BY date")
if body.empty:
    st.info("No body metrics yet.")
else:
    body["date"] = pd.to_datetime(body["date"])
    latest = body.sort_values("date").iloc[-1]
    start = body.sort_values("date").iloc[0]
    weekly = body[body["date"] >= (pd.Timestamp.today() - pd.Timedelta(days=6))]
    moving_avg = body[["date", "body_weight"]].copy()
    moving_avg["moving_avg"] = moving_avg["body_weight"].rolling(3, min_periods=1).mean()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Day 1 vs current", f"{float(latest['body_weight']) - float(start['body_weight']):+.2f}", "Weight delta")
    with c2:
        metric_card("Waist reduction", f"{float(latest['waist']) - float(start['waist']):+.2f}", "Negative is good")
    with c3:
        weekly_change = 0 if len(weekly.index) < 2 else float(weekly.iloc[-1]["body_weight"] - weekly.iloc[0]["body_weight"])
        metric_card("Weekly weight change", f"{weekly_change:+.2f}", "Last 7 days")
    with c4:
        metric_card("Latest body fat", f"{latest['body_fat_percent']:.1f}%", "Most recent entry")

    ch1, ch2 = st.columns(2)
    with ch1:
        st.plotly_chart(trend_chart(body, "date", "body_weight", "Body weight trend", "#f97316"), use_container_width=True)
        st.plotly_chart(trend_chart(moving_avg, "date", "moving_avg", "Moving average body weight", "#7c3aed"), use_container_width=True)
    with ch2:
        st.plotly_chart(trend_chart(body, "date", "waist", "Waist reduction trend", "#14b8a6"), use_container_width=True)
        if "body_fat_percent" in body.columns:
            st.plotly_chart(trend_chart(body, "date", "body_fat_percent", "Body fat trend", "#eab308"), use_container_width=True)

    status_banner(
        f"Milestones: chest {latest['chest']:.1f} • arms {latest['arms']:.1f} • thighs {latest['thighs'] if pd.notna(latest['thighs']) else latest['thigh']:.1f}",
        "success",
    )
    st.dataframe(body.sort_values("date", ascending=False), use_container_width=True, hide_index=True)

if st.button("Delete latest body metric", type="secondary"):
    delete_latest_log("body_metrics")
    st.warning("Latest body metric deleted.")
