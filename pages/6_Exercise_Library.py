from __future__ import annotations

import streamlit as st

from components.exercise_preview import render_exercise_preview
from exercise_data import load_exercise_data, search_exercises

st.title("🏋️ Exercise Library")
st.caption("Search your custom exercise list with direct YouTube demos + smart fallback links.")

records = load_exercise_data()
if not records:
    st.warning("Exercise library is empty. Run: python scripts/enrich_exercises_with_youtube.py")
    st.stop()

all_day_types = sorted({item["day_type"] for item in records})
all_muscles = sorted({item["muscle_group"] for item in records})

c1, c2 = st.columns(2)
with c1:
    day_filter = st.multiselect("Filter by Day Type", all_day_types, default=[])
with c2:
    muscle_filter = st.multiselect("Filter by Muscle Group", all_muscles, default=[])

search = st.text_input("Search exercise")
filtered = search_exercises(records, query=search, day_types=day_filter, muscle_groups=muscle_filter)

st.caption(f"Showing {len(filtered)} exercises")

for idx, item in enumerate(filtered):
    with st.container(border=True):
        render_exercise_preview(item)
        if idx < len(filtered) - 1:
            st.divider()
