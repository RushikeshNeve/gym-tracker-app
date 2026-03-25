from __future__ import annotations

from datetime import date

import streamlit as st

from components.exercise_preview import render_exercise_preview
from db import DAY_TYPES, delete_latest_log, fetch_df, insert_workout
from utils.exercise_data import get_exercise_by_name, load_exercise_data

st.title("📝 Log Workout")
st.caption("Fast one-row-per-exercise logging with built-in form demo videos.")

exercise_library = load_exercise_data()
exercises = fetch_df("SELECT exercise, day_type, muscle_group FROM exercises ORDER BY exercise")
exercise_names = exercises["exercise"].tolist()

selected_exercise = st.selectbox("Pick Exercise", exercise_names, index=0)
selected_meta = get_exercise_by_name(exercise_library, selected_exercise)
if selected_meta:
    render_exercise_preview(selected_meta)

with st.form("workout_form", clear_on_submit=True):
    c1, c2 = st.columns(2)
    with c1:
        log_date = st.date_input("Date", value=date.today())
        day_type = st.selectbox("Day Type", DAY_TYPES, index=0)
    with c2:
        exercise = st.text_input("Exercise", value=selected_exercise, disabled=True)
        row = exercises[exercises["exercise"] == selected_exercise].iloc[0]
        muscle_group = st.text_input("Muscle Group", value=row["muscle_group"], disabled=True)

    c3, c4, c5 = st.columns(3)
    with c3:
        weight = st.number_input("Weight", min_value=0.0, step=0.5, value=20.0)
    with c4:
        reps = st.number_input("Reps", min_value=1, step=1, value=10)
    with c5:
        sets = st.number_input("Sets", min_value=1, step=1, value=3)

    near_failure = st.toggle("Near failure?")
    notes = st.text_area("Notes", placeholder="How did the set feel?")

    submitted = st.form_submit_button("Save Workout")

if submitted:
    payload = {
        "date": log_date.strftime("%Y-%m-%d"),
        "day_type": day_type,
        "exercise": selected_exercise,
        "muscle_group": row["muscle_group"],
        "weight": weight,
        "reps": int(reps),
        "sets": int(sets),
        "near_failure": near_failure,
        "notes": notes,
    }
    pr = insert_workout(payload)
    volume = weight * reps * sets
    st.success(f"Saved ✅ Volume: {volume:.0f}")
    if pr:
        st.balloons()
        st.markdown(f"### 🏅 {pr} achieved on **{selected_exercise}**")

with st.expander("🧘 Rest Timer"):
    seconds = st.slider("Seconds", 30, 240, 90, 15)
    st.write("Start your timer and return for the next set.")
    st.code(f"Rest target: {seconds} sec")

st.markdown("### ✏️ Quick Edit/Delete latest entry")
recent = fetch_df("SELECT * FROM workout_logs ORDER BY id DESC LIMIT 1")
if recent.empty:
    st.info("No workout logs yet.")
else:
    st.dataframe(recent, use_container_width=True, hide_index=True)

if st.button("Delete latest workout log", type="secondary"):
    delete_latest_log("workout_logs")
    st.warning("Latest workout log deleted.")
