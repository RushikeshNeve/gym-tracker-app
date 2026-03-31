from __future__ import annotations

from datetime import date

import streamlit as st

from components.exercise_preview import render_exercise_preview
from db import DAY_TYPES, WORKOUT_SESSION_TYPES, delete_latest_log, fetch_df, get_user_profile, insert_workout
from utils import metric_card, section_card
from utils.calorie_logic import estimate_calories_burned
from utils.challenge_logic import get_split_plan
from utils.exercise_data import get_exercise_by_name, load_exercise_data

st.title("Log Workout")
st.caption("Keep the existing lift logger, now upgraded for 75 Hard workout sessions.")

exercise_library = load_exercise_data()
exercises = fetch_df("SELECT exercise, day_type, muscle_group FROM exercises ORDER BY exercise")
exercise_names = exercises["exercise"].tolist()
selected_exercise = st.selectbox("Pick Exercise", exercise_names, index=0)
selected_meta = get_exercise_by_name(exercise_library, selected_exercise)
if selected_meta:
    render_exercise_preview(selected_meta)

row = exercises[exercises["exercise"] == selected_exercise].iloc[0]
previous = fetch_df(
    "SELECT date, weight, reps, sets, new_pr FROM workout_logs WHERE exercise = ? ORDER BY date DESC, id DESC LIMIT 3",
    (selected_exercise,),
)
plan = get_split_plan()
profile = get_user_profile()

top_left, top_right = st.columns(2)
with top_left:
    section_card("Suggested split", f"Today: {plan['today_plan']} • Tomorrow: {plan['tomorrow_plan']}")
with top_right:
    if previous.empty:
        section_card("Previous performance", "No history yet for this exercise.")
    else:
        last = previous.iloc[0]
        section_card("Previous performance", f"{last['date']} • {last['weight']} x {last['reps']} for {last['sets']} sets")

with st.form("workout_form", clear_on_submit=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        log_date = st.date_input("Date", value=date.today())
        day_type = st.selectbox("Day Type", DAY_TYPES, index=0)
    with c2:
        session_type = st.selectbox("Workout session type", WORKOUT_SESSION_TYPES, index=0)
        is_outdoor = st.toggle("Outdoor workout")
    with c3:
        duration_min = st.number_input("Session duration (min)", min_value=0, max_value=240, value=45, step=5)
        near_failure = st.toggle("Near failure?")

    c4, c5, c6 = st.columns(3)
    with c4:
        exercise = st.text_input("Exercise", value=selected_exercise, disabled=True)
        muscle_group = st.text_input("Muscle Group", value=row["muscle_group"], disabled=True)
    with c5:
        weight = st.number_input("Weight", min_value=0.0, step=0.5, value=20.0)
        reps = st.number_input("Reps", min_value=1, step=1, value=10)
    with c6:
        sets = st.number_input("Sets", min_value=1, step=1, value=3)
        start_time = st.time_input("Start time")
        end_time = st.time_input("End time")

    notes = st.text_area("Notes", placeholder="How did the workout feel?")
    session_notes = st.text_area("Session notes", placeholder="Context, gym flow, weather, anything worth remembering")
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
        "session_type": session_type,
        "is_outdoor": is_outdoor,
        "duration_min": int(duration_min),
        "start_time": start_time.strftime("%H:%M"),
        "end_time": end_time.strftime("%H:%M"),
        "session_notes": session_notes,
        "estimated_calories_burned": estimate_calories_burned(day_type, int(duration_min), float(profile.get("current_weight_kg", 0) or 0)),
    }
    pr = insert_workout(payload)
    volume = weight * reps * sets
    st.success(f"Saved. Volume: {volume:.0f} • Estimated burn: {payload['estimated_calories_burned']:.0f} kcal")
    if pr:
        st.balloons()
        st.markdown(f"### {pr} achieved on **{selected_exercise}**")

with st.expander("Rest Timer"):
    seconds = st.slider("Seconds", 30, 240, 90, 15)
    st.code(f"Rest target: {seconds} sec")

st.markdown("### Recent comparison")
if previous.empty:
    st.info("No previous performance yet.")
else:
    st.dataframe(previous, use_container_width=True, hide_index=True)

st.markdown("### Quick Delete")
recent = fetch_df("SELECT * FROM workout_logs ORDER BY id DESC LIMIT 1")
if recent.empty:
    st.info("No workout logs yet.")
else:
    latest = recent.iloc[0]
    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Latest session", str(latest["session_type"]), latest["date"])
    with c2:
        metric_card("Outdoor", "Yes" if latest["is_outdoor"] else "No", latest["exercise"])
    with c3:
        metric_card("Duration", f"{latest['duration_min']} min", f"{latest.get('estimated_calories_burned', 0):.0f} kcal")
    st.dataframe(recent, use_container_width=True, hide_index=True)

if st.button("Delete latest workout log", type="secondary"):
    delete_latest_log("workout_logs")
    st.warning("Latest workout log deleted.")
