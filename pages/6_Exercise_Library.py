from __future__ import annotations

import streamlit as st

from db import fetch_df

st.title("🏋️ Exercise Library")
st.caption("Large built-in exercise database grouped by training day and muscle group.")

ex = fetch_df("SELECT exercise, day_type, muscle_group FROM exercises ORDER BY muscle_group, exercise")

if ex.empty:
    st.warning("Exercise library is empty.")
    st.stop()

c1, c2 = st.columns(2)
with c1:
    day_filter = st.multiselect("Filter by Day Type", sorted(ex["day_type"].unique()), default=[])
with c2:
    muscle_filter = st.multiselect("Filter by Muscle Group", sorted(ex["muscle_group"].unique()), default=[])

if day_filter:
    ex = ex[ex["day_type"].isin(day_filter)]
if muscle_filter:
    ex = ex[ex["muscle_group"].isin(muscle_filter)]

search = st.text_input("Search exercise")
if search:
    ex = ex[ex["exercise"].str.contains(search, case=False, na=False)]

st.dataframe(ex, use_container_width=True, hide_index=True)

st.markdown("### Grouped View")
for muscle, group in ex.groupby("muscle_group"):
    with st.expander(f"{muscle} ({len(group)})"):
        st.write(", ".join(group["exercise"].tolist()))
