from __future__ import annotations

import streamlit as st

from components.exercise_preview import render_exercise_preview
from utils.exercise_data import filter_values, load_enriched_exercises, search_and_filter_exercises

st.title("🏋️ Exercise Library")
st.caption("Search and filter your custom exercise list enriched by free-exercise-db.")

exercises = load_enriched_exercises()

if not exercises:
    st.warning("No enriched exercise data found. Run: python scripts/enrich_exercises.py")
    st.stop()

query = st.text_input("Search by custom or source name")

c1, c2 = st.columns(2)
with c1:
    day_type_filter = st.multiselect("Day type", filter_values(exercises, "day_type"))
    equipment_filter = st.multiselect("Equipment", filter_values(exercises, "equipment"))
    category_filter = st.multiselect("Category", filter_values(exercises, "category"))
with c2:
    muscle_filter = st.multiselect("Muscle group", filter_values(exercises, "muscle_group"))
    level_filter = st.multiselect("Level", filter_values(exercises, "level"))
    matched_only = st.toggle("Matched only", value=False)

filtered = search_and_filter_exercises(
    exercises,
    query=query,
    day_types=day_type_filter,
    muscle_groups=muscle_filter,
    equipment=equipment_filter,
    levels=level_filter,
    categories=category_filter,
    matched_only=matched_only,
)

st.caption(f"Showing {len(filtered)} exercises")

for idx, exercise in enumerate(filtered):
    render_exercise_preview(exercise, key_prefix=f"library_{idx}")
