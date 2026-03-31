from __future__ import annotations

import streamlit as st

from db import ensure_challenge_start_date, init_db, seed_exercises, seed_sample_data
from utils import inject_css, render_chip_row, render_today_hero
from utils.challenge_logic import get_challenge_progress

st.set_page_config(page_title="75 Hard Tracker", page_icon="💪", layout="wide")

init_db()
seed_exercises()
seed_sample_data()
inject_css()

challenge_start = ensure_challenge_start_date()
progress = get_challenge_progress()

render_today_hero(
    f"75 Hard Accountability Hub",
    f"Challenge start date: {challenge_start} • Day {progress['day_number']} / 75",
)
render_chip_row(
    [
        ("Today first", "success"),
        ("Fat-loss focused", "warn"),
        ("Workout + nutrition + water + photos", "neutral"),
    ]
)

st.markdown(
    """
### Quick Start
Use the sidebar in this order:
- **Today** for your daily 75 Hard checklist and accountability
- **Dashboard** for KPIs, challenge trends, and this-week summary
- **Log Workout**, **Nutrition**, and **Hydration** for daily execution
- **Body Metrics**, **Cardio**, **Progress**, and **Progress Photos** for transformation tracking
- **Exercise Library** and **Weekly Review** for planning and reflection
"""
)
