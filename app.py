from __future__ import annotations

import streamlit as st

from db import init_db, seed_exercises, seed_sample_data
from utils import inject_css

st.set_page_config(page_title="Gym Tracker Pro", page_icon="🏋️", layout="wide")

init_db()
seed_exercises()
seed_sample_data()
inject_css()

st.title("🏋️ Gym Tracker Pro")
st.caption("Mobile-first fitness tracking for strength, fat-loss, and consistency.")

st.markdown(
    """
### Quick Start
Use the sidebar to navigate pages:
- **Dashboard** for KPIs, trends, score, and recommendations
- **Log Workout** for fast lifting entries and PR auto-detection
- **Body Metrics** for transformation tracking
- **Cardio** for adherence and calories burned
- **Progress** for deeper analytics and filters
- **Exercise Library** for searchable movement catalog

This app is seeded with demo entries based on your spreadsheet logic.
"""
)
