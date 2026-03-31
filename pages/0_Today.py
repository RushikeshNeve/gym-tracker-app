from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from db import get_or_create_challenge_day, get_setting, save_challenge_day
from utils import metric_card, progress_block, render_chip_row, status_banner
from utils.challenge_logic import REQUIRED_TASK_KEYS, get_split_plan, get_today_snapshot, sync_challenge_day
from utils.nutrition_logic import calculate_diet_compliance_score

st.title("Today")

st.markdown(
    """
    <style>
        .today-shell {
            display: grid;
            grid-template-columns: 1.4fr 0.9fr;
            gap: 1rem;
            margin-bottom: 1rem;
        }
        .today-hero-card {
            background:
                radial-gradient(circle at top left, rgba(14, 165, 233, 0.18), transparent 32%),
                radial-gradient(circle at bottom right, rgba(249, 115, 22, 0.18), transparent 28%),
                linear-gradient(135deg, #0f172a 0%, #111827 48%, #1e293b 100%);
            color: #f8fafc;
            border-radius: 26px;
            padding: 24px;
            box-shadow: 0 20px 50px rgba(15, 23, 42, 0.24);
            border: 1px solid rgba(255,255,255,0.08);
        }
        .today-kicker {
            text-transform: uppercase;
            letter-spacing: 0.14em;
            font-size: 0.74rem;
            opacity: 0.78;
            margin-bottom: 0.65rem;
        }
        .today-day {
            font-size: 2.25rem;
            font-weight: 800;
            line-height: 1.05;
            margin-bottom: 0.4rem;
        }
        .today-copy {
            color: rgba(248, 250, 252, 0.82);
            font-size: 0.98rem;
            margin-bottom: 1rem;
        }
        .today-hero-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.7rem;
        }
        .today-hero-stat {
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 14px;
        }
        .today-hero-label {
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            opacity: 0.74;
            margin-bottom: 0.35rem;
        }
        .today-hero-value {
            font-size: 1.15rem;
            font-weight: 700;
        }
        .today-side-card {
            background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
            border-radius: 24px;
            padding: 18px;
            border: 1px solid rgba(148, 163, 184, 0.18);
            box-shadow: 0 14px 36px rgba(15, 23, 42, 0.08);
        }
        .today-side-title {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #64748b;
            margin-bottom: 0.4rem;
        }
        .today-side-value {
            font-size: 1.55rem;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 0.25rem;
        }
        .today-side-copy {
            color: #475569;
            font-size: 0.92rem;
        }
        .today-section-title {
            font-size: 1.02rem;
            font-weight: 700;
            color: #f8fafc;
            margin: 0.9rem 0 0.7rem;
        }
        .checklist-status {
            display: inline-block;
            margin-top: 0.45rem;
            margin-bottom: 0.35rem;
            padding: 4px 10px;
            border-radius: 999px;
            font-size: 0.74rem;
            font-weight: 700;
        }
        .checklist-status.done {
            background: rgba(34, 197, 94, 0.16);
            color: #86efac;
            border: 1px solid rgba(34, 197, 94, 0.28);
        }
        .checklist-status.pending {
            background: rgba(245, 158, 11, 0.14);
            color: #fcd34d;
            border: 1px solid rgba(245, 158, 11, 0.24);
        }
        .checklist-copy {
            color: #cbd5e1;
            font-size: 0.92rem;
            line-height: 1.5;
            margin-top: 0.2rem;
        }
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.85rem;
            margin-bottom: 0.9rem;
        }
        .summary-box {
            background: linear-gradient(180deg, #fff7ed 0%, #ffffff 100%);
            border-radius: 18px;
            padding: 14px 15px;
            border: 1px solid rgba(251, 146, 60, 0.18);
        }
        .summary-box:nth-child(2) {
            background: linear-gradient(180deg, #ecfeff 0%, #ffffff 100%);
            border-color: rgba(6, 182, 212, 0.18);
        }
        .summary-box:nth-child(3) {
            background: linear-gradient(180deg, #f0fdf4 0%, #ffffff 100%);
            border-color: rgba(34, 197, 94, 0.18);
        }
        .summary-label {
            font-size: 0.76rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #64748b;
            margin-bottom: 0.35rem;
        }
        .summary-value {
            font-size: 1.15rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 0.25rem;
        }
        .summary-copy {
            color: #475569;
            font-size: 0.88rem;
        }
        .sticky-status {
            position: sticky;
            top: 1rem;
        }
        @media (max-width: 900px) {
            .today-shell {
                grid-template-columns: 1fr;
            }
            .today-hero-grid, .summary-grid, .checklist-grid {
                grid-template-columns: 1fr;
            }
            .sticky-status {
                position: static;
            }
            .today-day {
                font-size: 1.8rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

today_str = date.today().isoformat()
snapshot = get_today_snapshot()
existing_day = get_or_create_challenge_day(today_str)
plan = get_split_plan()
total_completed = int(snapshot.get("total_completed", 0))
required_total = int(snapshot.get("required_total", 8))
progress_pct = round((total_completed / required_total) * 100) if required_total else 0
activity = snapshot["activity"]
energy = snapshot.get("energy_balance", {})
top_status_df = pd.DataFrame(
    [
        {"Metric": "Challenge Day", "Value": f"Day {snapshot['day_number']} / 75", "Details": f"{progress_pct}% complete today"},
        {"Metric": "Current Streak", "Value": str(snapshot["current_streak"]), "Details": "Consecutive perfect days"},
        {"Metric": "Perfect Days", "Value": str(snapshot["perfect_days"]), "Details": "Full-compliance days logged"},
        {"Metric": "Failed Days", "Value": str(snapshot["failed_days"]), "Details": "Past days with missing tasks"},
        {"Metric": "Remaining Days", "Value": str(snapshot["remaining_days"]), "Details": "Days left in the challenge"},
        {"Metric": "Status", "Value": snapshot["day_status"].title(), "Details": f"Compliance score {snapshot['compliance_score']:.0f}%"},
    ]
)
bottom_status_df = pd.DataFrame(
    [
        {"Item": "Today", "Status": snapshot["day_status"].title(), "Notes": f"{total_completed}/{required_total} required tasks complete"},
        {"Item": "Tomorrow Plan", "Status": plan["tomorrow_plan"], "Notes": "Next planned training focus"},
        {"Item": "Recovery Suggestion", "Status": "Action", "Notes": plan["missed_recovery"]},
    ]
)
pending_tasks_df = pd.DataFrame(
    [{"Pending Task": item, "Priority": "Required today"} for item in snapshot["pending_tasks"]]
) if snapshot["pending_tasks"] else pd.DataFrame([{"Pending Task": "No pending tasks", "Priority": "Fully on track"}])
nutrition_status_df = pd.DataFrame(
    [
        {"Nutrition Check": "Calories target", "Status": "Hit" if snapshot["nutrition_bonus_flags"]["calorie_target_hit"] else "Missed"},
        {"Nutrition Check": "Protein target", "Status": "Hit" if snapshot["nutrition_bonus_flags"]["protein_target_hit"] else "Missed"},
        {"Nutrition Check": "Whey taken", "Status": "Yes" if snapshot["nutrition_bonus_flags"]["whey_taken"] else "No"},
        {"Nutrition Check": "Energy status", "Status": energy.get("status", "unknown").replace("_", " ").title()},
    ]
)

task_labels = {
    "workout_1_completed": "Workout 1 completed",
    "workout_2_completed": "Workout 2 completed",
    "one_workout_outdoors": "One workout outdoors",
    "followed_diet": "Followed diet",
    "no_cheat_meals": "No cheat meals",
    "no_alcohol": "No alcohol",
    "water_goal_completed": "Water goal completed",
    "progress_picture_taken": "Progress photo taken",
}
task_help = {
    "workout_1_completed": "Your first intentional session for the day.",
    "workout_2_completed": "Second session needed to stay compliant.",
    "one_workout_outdoors": "At least one of the two sessions must happen outside.",
    "followed_diet": "Stayed aligned with the plan you chose.",
    "no_cheat_meals": "No meals outside the rules today.",
    "no_alcohol": "Zero alcohol for the day.",
    "water_goal_completed": "Hit the full hydration target.",
    "progress_picture_taken": "Logged a progress photo for accountability.",
}
task_tones = {
    "workout_1_completed": "warn",
    "workout_2_completed": "warn",
    "one_workout_outdoors": "neutral",
    "followed_diet": "success",
    "no_cheat_meals": "success",
    "no_alcohol": "success",
    "water_goal_completed": "neutral",
    "progress_picture_taken": "warn",
}

hero_html = f"""
<div class="today-shell">
  <div class="today-hero-card">
    <div class="today-kicker">75 Hard Daily Accountability</div>
    <div class="today-day">Day {snapshot['day_number']} / 75</div>
    <div class="today-copy">
      Starting tomorrow doesn’t need hype, it needs structure. This screen is your one-place check for training,
      diet, water, photos, and daily discipline.
    </div>
    <div class="today-hero-grid">
      <div class="today-hero-stat">
        <div class="today-hero-label">Today score</div>
        <div class="today-hero-value">{snapshot['compliance_score']:.0f}%</div>
      </div>
      <div class="today-hero-stat">
        <div class="today-hero-label">Completed</div>
        <div class="today-hero-value">{total_completed} / {required_total}</div>
      </div>
      <div class="today-hero-stat">
        <div class="today-hero-label">Planned split</div>
        <div class="today-hero-value">{plan['today_plan']}</div>
      </div>
    </div>
  </div>
  <div class="today-side-card sticky-status">
    <div class="today-side-title">Challenge status</div>
    <div class="today-side-value">{snapshot['day_status'].title()}</div>
    <div class="today-side-copy">Current streak {snapshot['current_streak']} • perfect days {snapshot['perfect_days']} • failed days {snapshot['failed_days']}</div>
    <div style="height:0.8rem"></div>
    <div class="today-side-title">Tomorrow</div>
    <div class="today-side-copy">{plan['tomorrow_plan']}</div>
    <div style="height:0.8rem"></div>
    <div class="today-side-title">Recovery suggestion</div>
    <div class="today-side-copy">{plan['missed_recovery']}</div>
  </div>
</div>
"""
st.markdown(hero_html, unsafe_allow_html=True)

if snapshot["day_status"] == "perfect":
    status_banner("Today is fully compliant. Protect the streak and close the day strong.", "success")
else:
    pending_text = ", ".join(snapshot["pending_tasks"]) if snapshot["pending_tasks"] else "No pending tasks"
    status_banner(f"Still open today: {pending_text}", "warning")

st.markdown("<div class='today-section-title'>Status Table</div>", unsafe_allow_html=True)
st.dataframe(top_status_df, use_container_width=True, hide_index=True)

st.markdown("<div class='today-section-title'>Daily Progress</div>", unsafe_allow_html=True)
progress_block("Required tasks complete", total_completed, required_total)

st.markdown("<div class='today-section-title'>Today Summary</div>", unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="summary-grid">
      <div class="summary-box">
        <div class="summary-label">Training</div>
        <div class="summary-value">{activity['total_sessions']} sessions</div>
        <div class="summary-copy">{activity['outdoor_sessions']} outdoor • {activity['workout_sessions']} workout slots logged</div>
      </div>
      <div class="summary-box">
        <div class="summary-label">Hydration</div>
        <div class="summary-value">{activity['water_total_ml'] / 1000:.2f} L</div>
        <div class="summary-copy">Target {activity['water_target_ml'] / 1000:.2f} L for the day</div>
      </div>
      <div class="summary-box">
        <div class="summary-label">Nutrition</div>
        <div class="summary-value">{activity['nutrition_totals']['calories']:.0f} kcal</div>
        <div class="summary-copy">{activity['nutrition_totals']['protein']:.0f} g protein tracked</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='today-section-title'>Nutrition & Energy Check</div>", unsafe_allow_html=True)
st.dataframe(nutrition_status_df, use_container_width=True, hide_index=True)

st.markdown("<div class='today-section-title'>Required Checklist</div>", unsafe_allow_html=True)
checklist_values: dict[str, bool] = {}
with st.form("today_form"):
    checklist_cols = st.columns(2)
    for idx, key in enumerate(REQUIRED_TASK_KEYS):
        with checklist_cols[idx % 2]:
            with st.container(border=True):
                checked = bool(snapshot.get(key))
                checklist_values[key] = st.checkbox(task_labels[key], value=checked, help=task_help[key], key=f"today_{key}")
                st.markdown(
                    f"<div class='checklist-status {'done' if checked else 'pending'}'>{'Done' if checked else 'Pending'}</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(f"<div class='checklist-copy'>{task_help[key]}</div>", unsafe_allow_html=True)

    st.markdown("<div class='today-section-title'>Body, Mood, and Recovery</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        body_weight = st.number_input("Body weight", min_value=30.0, max_value=250.0, value=float(existing_day.get("body_weight") or 80.0), step=0.1)
        steps = st.number_input("Steps", min_value=0, max_value=50000, value=int(existing_day.get("steps") or 0), step=500)
    with c2:
        sleep_hours = st.number_input("Sleep hours", min_value=0.0, max_value=14.0, value=float(existing_day.get("sleep_hours") or 0.0), step=0.25)
        energy_level = st.slider("Energy level", 0, 10, int(existing_day.get("energy_level") or 0))
    with c3:
        mood = st.text_input("Mood", value=str(existing_day.get("mood") or ""))
        selected_diet_plan = st.text_input(
            "Diet plan",
            value=str(existing_day.get("selected_diet_plan") or get_setting("diet_plan_name", "High protein calorie deficit")),
        )

    st.markdown("<div class='today-section-title'>Diet Reality Check</div>", unsafe_allow_html=True)
    d1, d2, d3 = st.columns(3)
    with d1:
        cheat_meal = st.toggle("Cheat meal happened", value=bool(existing_day.get("cheat_meal")))
        junk_food = st.toggle("Junk food included", value=bool(existing_day.get("junk_food")))
    with d2:
        sugary_drinks = st.toggle("Sugary drinks included", value=bool(existing_day.get("sugary_drinks")))
        hunger_level = st.slider("Hunger level", 0, 10, int(existing_day.get("hunger_level") or 0))
    with d3:
        cravings_level = st.slider("Cravings level", 0, 10, int(existing_day.get("cravings_level") or 0))
        binge_urge = st.slider("Binge urge", 0, 10, int(existing_day.get("binge_urge") or 0))

    notes = st.text_area(
        "Daily notes",
        value=str(existing_day.get("notes") or ""),
        placeholder="What nearly slipped, what felt strong, what needs attention tonight?",
    )
    diet_notes = st.text_area(
        "Diet notes",
        value=str(existing_day.get("diet_notes") or ""),
        placeholder="Hunger, cravings, meal timing, food quality, and anything you want to review later.",
    )
    submitted = st.form_submit_button("Save Daily Entry", use_container_width=True)

if submitted:
    diet_score = calculate_diet_compliance_score(
        today_str,
        followed_plan=checklist_values["followed_diet"],
        no_cheat_meal=checklist_values["no_cheat_meals"] and not cheat_meal,
    )
    save_challenge_day(
        {
            **existing_day,
            **{key: int(value) for key, value in checklist_values.items()},
            "date": today_str,
            "body_weight": body_weight,
            "steps": steps,
            "sleep_hours": sleep_hours,
            "mood": mood,
            "energy_level": energy_level,
            "notes": notes,
            "selected_diet_plan": selected_diet_plan,
            "diet_followed": int(checklist_values["followed_diet"]),
            "cheat_meal": int(cheat_meal),
            "junk_food": int(junk_food),
            "sugary_drinks": int(sugary_drinks),
            "hunger_level": hunger_level,
            "cravings_level": cravings_level,
            "binge_urge": binge_urge,
            "diet_notes": diet_notes,
            "no_cheat_meals": int(checklist_values["no_cheat_meals"] and not cheat_meal),
            "compliance_score": max(diet_score, snapshot["compliance_score"]),
        }
    )
    snapshot = sync_challenge_day(today_str)
    st.success("Today updated.")
    st.rerun()

st.markdown("<div class='today-section-title'>Pending Tasks</div>", unsafe_allow_html=True)
st.dataframe(pending_tasks_df, use_container_width=True, hide_index=True)

st.markdown("<div class='today-section-title'>Challenge Status</div>", unsafe_allow_html=True)
st.dataframe(bottom_status_df, use_container_width=True, hide_index=True)
