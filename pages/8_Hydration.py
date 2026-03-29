from __future__ import annotations

from datetime import date

import streamlit as st

from db import delete_hydration_log, get_hydration_export_df, insert_hydration_log, save_daily_targets
from utils import bar_chart, metric_card, progress_block, status_banner
from utils.hydration_logic import get_daily_hydration, get_weekly_hydration

st.title("Hydration")
selected_date = st.date_input("Hydration date", value=date.today())
log_date = selected_date.isoformat()
hydration = get_daily_hydration(log_date)

c1, c2, c3 = st.columns(3)
with c1:
    metric_card("Water today", f"{hydration['total_ml'] / 1000:.2f} L", f"Target {hydration['target_liters']:.2f} L")
with c2:
    metric_card("Remaining", f"{hydration['remaining_ml'] / 1000:.2f} L", "Still to drink")
with c3:
    metric_card("Bottle count", str(hydration["bottle_count"]), "Based on 500 ml bottles")

progress_block("Water progress", hydration["total_ml"], hydration["target_ml"])

with st.form("water_target_form"):
    water_target = st.number_input("Daily water target (L)", min_value=1.0, max_value=10.0, value=float(hydration["target_liters"]), step=0.25)
    if st.form_submit_button("Save Water Target"):
        save_daily_targets({"date": log_date, "water_target_liters": water_target})
        st.success("Water target saved.")
        st.rerun()

st.markdown("### Quick Add")
q1, q2, q3 = st.columns(3)
with q1:
    if st.button("Add 250 ml", use_container_width=True):
        insert_hydration_log({"date": log_date, "amount_ml": 250})
        st.rerun()
with q2:
    if st.button("Add 500 ml", use_container_width=True):
        insert_hydration_log({"date": log_date, "amount_ml": 500})
        st.rerun()
with q3:
    if st.button("Add 1 L", use_container_width=True):
        insert_hydration_log({"date": log_date, "amount_ml": 1000})
        st.rerun()

if hydration["progress_pct"] >= 100:
    status_banner("Water goal complete for the day.", "success")
else:
    status_banner(f"{hydration['remaining_ml'] / 1000:.2f} L remaining to hit target.", "warning")

st.markdown("### Intake History")
if hydration["logs"].empty:
    st.info("No hydration entries yet.")
else:
    selected_log = st.selectbox("Select hydration log to delete", hydration["logs"]["id"].tolist(), format_func=lambda x: f"Entry #{x}")
    if st.button("Delete Selected Entry", type="secondary"):
        delete_hydration_log(int(selected_log))
        st.warning("Hydration entry deleted.")
        st.rerun()
    st.dataframe(hydration["logs"], use_container_width=True, hide_index=True)

st.markdown("### Weekly Hydration Adherence")
weekly = get_weekly_hydration()
if weekly.empty:
    st.info("Weekly hydration trend will show up after a few entries.")
else:
    st.plotly_chart(bar_chart(weekly, "date", "total_ml", "Weekly hydration intake", "#0ea5e9"), use_container_width=True)
    st.dataframe(weekly[["date", "total_ml", "target_ml", "adherence_pct"]], use_container_width=True, hide_index=True)

export_df = get_hydration_export_df()
st.download_button("Export hydration CSV", export_df.to_csv(index=False).encode("utf-8"), "hydration_logs.csv")
