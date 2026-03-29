from __future__ import annotations

from datetime import date, timedelta

import pandas as pd
import streamlit as st

from db import (
    ACTIVITY_LEVELS,
    GOAL_TYPES,
    copy_nutrition_logs,
    delete_nutrition_log,
    get_nutrition_export_df,
    get_user_profile,
    insert_nutrition_log,
    save_daily_targets,
    save_user_profile,
    update_nutrition_log,
)
from utils import bar_chart, metric_card, progress_block, status_banner
from utils.calorie_logic import calculate_daily_energy_balance, get_weekly_energy_balance
from utils.nutrition_logic import (
    calculate_diet_compliance_score,
    get_daily_nutrition,
    get_meal_breakdown,
    get_recipe_by_name,
    get_recipe_library_df,
    get_spicy_snacks_df,
    get_today_meal_plan,
    get_weekly_nutrition,
)
from utils.profile_logic import calculate_bmr, calculate_protein_target, calculate_target_calories, calculate_tdee

st.title("Nutrition")
selected_date = st.date_input("Nutrition date", value=date.today())
log_date = selected_date.isoformat()
profile = get_user_profile()
daily = get_daily_nutrition(log_date)
energy = calculate_daily_energy_balance(log_date)
meal_plan = get_today_meal_plan(selected_date)
spicy_snacks = get_spicy_snacks_df()

with st.expander("Profile & Maintenance Calories", expanded=True):
    with st.form("profile_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            age = st.number_input("Age", min_value=15, max_value=80, value=int(profile.get("age", 27)))
            gender = st.selectbox("Gender", ["male", "female"], index=0 if str(profile.get("gender", "male")).lower() == "male" else 1)
            height_cm = st.number_input("Height (cm)", min_value=120.0, max_value=230.0, value=float(profile.get("height_cm", 175.0)), step=0.5)
        with c2:
            current_weight_kg = st.number_input("Current weight (kg)", min_value=35.0, max_value=250.0, value=float(profile.get("current_weight_kg", 83.5)), step=0.1)
            activity_level = st.selectbox("Activity level", ACTIVITY_LEVELS, index=ACTIVITY_LEVELS.index(str(profile.get("activity_level", "moderately_active"))))
            goal = st.selectbox("Goal", GOAL_TYPES, index=GOAL_TYPES.index(str(profile.get("goal", "fat_loss"))))
        with c3:
            desired_deficit = st.number_input("Desired deficit", min_value=0, max_value=1200, value=int(float(profile.get("desired_deficit", 450))), step=50)
            preview_profile = {
                "age": age,
                "gender": gender,
                "height_cm": height_cm,
                "current_weight_kg": current_weight_kg,
                "activity_level": activity_level,
                "goal": goal,
                "desired_deficit": desired_deficit,
            }
            st.metric("BMR", f"{calculate_bmr(preview_profile):.0f}")
            st.metric("TDEE", f"{calculate_tdee(preview_profile):.0f}")
            st.metric("Target calories", f"{calculate_target_calories(preview_profile):.0f}")
        save_profile_btn = st.form_submit_button("Save Profile", use_container_width=True)
    if save_profile_btn:
        save_user_profile(preview_profile)
        save_daily_targets(
            {
                "date": log_date,
                "calorie_target": round(calculate_target_calories(preview_profile)),
                "protein_target": round(calculate_protein_target(preview_profile)),
                "carbs_target": float(daily["targets"]["carbs_target"]),
                "fats_target": float(daily["targets"]["fats_target"]),
                "fiber_target": float(daily["targets"]["fiber_target"]),
                "water_target_liters": float(daily["targets"]["water_target_liters"]),
            }
        )
        st.success("Profile saved and today's calorie/protein targets updated.")
        st.rerun()

st.markdown("### Energy Balance")
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    metric_card("Maintenance", f"{energy['maintenance_calories']:.0f}", "TDEE")
with c2:
    metric_card("Target", f"{energy['target_calories']:.0f}", "Goal calories")
with c3:
    metric_card("Food", f"{energy['food_calories']:.0f}", "Consumed today")
with c4:
    metric_card("Burned", f"{energy['exercise_calories']:.0f}", "Exercise calories")
with c5:
    metric_card("Net", f"{energy['net_calories']:.0f}", "Food minus burn")
with c6:
    metric_card("Balance", f"{energy['deficit_or_surplus']:.0f}", energy["status"].replace("_", " ").title())

status_banner(
    f"Daily status: {energy['status'].replace('_', ' ').title()} • Protein today {daily['totals']['protein']:.0f} g • Diet score {calculate_diet_compliance_score(log_date, True, True)}",
    "success" if energy["status"] == "in_deficit" else "warning",
)

st.markdown("### Daily Targets")
with st.form("target_form"):
    c1, c2, c3 = st.columns(3)
    with c1:
        calorie_target = st.number_input("Calories", min_value=1000, max_value=6000, value=int(float(daily["targets"]["calorie_target"])), step=50)
        protein_target = st.number_input("Protein", min_value=50, max_value=400, value=int(float(daily["targets"]["protein_target"])), step=5)
    with c2:
        carbs_target = st.number_input("Carbs", min_value=0, max_value=600, value=int(float(daily["targets"]["carbs_target"])), step=5)
        fats_target = st.number_input("Fats", min_value=0, max_value=250, value=int(float(daily["targets"]["fats_target"])), step=5)
    with c3:
        fiber_target = st.number_input("Fiber", min_value=0, max_value=120, value=int(float(daily["targets"]["fiber_target"])), step=1)
        water_target = st.number_input("Water target (L)", min_value=1.0, max_value=10.0, value=float(daily["targets"]["water_target_liters"]), step=0.25)
    if st.form_submit_button("Save Daily Targets"):
        save_daily_targets(
            {
                "date": log_date,
                "calorie_target": calorie_target,
                "protein_target": protein_target,
                "carbs_target": carbs_target,
                "fats_target": fats_target,
                "fiber_target": fiber_target,
                "water_target_liters": water_target,
            }
        )
        st.success("Targets saved.")
        st.rerun()

c1, c2, c3, c4 = st.columns(4)
with c1:
    metric_card("Calories consumed", f"{daily['totals']['calories']:.0f}", f"{daily['remaining']['calories']:.0f} remaining")
with c2:
    metric_card("Protein", f"{daily['totals']['protein']:.0f} g", f"{daily['remaining']['protein']:.0f} remaining")
with c3:
    metric_card("Carbs", f"{daily['totals']['carbs']:.0f} g", f"{daily['remaining']['carbs']:.0f} remaining")
with c4:
    metric_card("Fats", f"{daily['totals']['fats']:.0f} g", f"{daily['remaining']['fats']:.0f} remaining")

progress_block("Calorie target", daily["totals"]["calories"], float(daily["targets"]["calorie_target"]))
progress_block("Protein target", daily["totals"]["protein"], float(daily["targets"]["protein_target"]))
progress_block("Carbs target", daily["totals"]["carbs"], float(daily["targets"]["carbs_target"]))
progress_block("Fats target", daily["totals"]["fats"], float(daily["targets"]["fats_target"]))

st.markdown("### Today's Planned Meals")
if meal_plan.empty:
    st.info("No meal template for this weekday yet.")
else:
    selected_options: dict[str, str] = {}
    for _, row in meal_plan.iterrows():
        options = [opt for opt in [row["option_1"], row["option_2"], row["option_3"], row["option_4"]] if isinstance(opt, str) and opt.strip()]
        if not options:
            continue
        meal_type = str(row["meal_type"]).replace("_", " ").title()
        st.markdown(f"#### {meal_type}")
        picked = st.radio(
            f"Choose {meal_type}",
            options,
            horizontal=True,
            key=f"plan_{row['meal_type']}",
            label_visibility="collapsed",
        )
        selected_options[row["meal_type"]] = picked
        recipe = get_recipe_by_name(picked)
        if recipe:
            with st.container(border=True):
                col_a, col_b = st.columns([1.2, 0.8])
                with col_a:
                    st.subheader(recipe["recipe_name"])
                    st.caption(recipe["portion_note"])
                    st.write("Ingredients")
                    for item in recipe["ingredients"]:
                        st.write(f"- {item['item']}: {item['quantity']}")
                    st.write("Steps")
                    for idx, step in enumerate(recipe["steps"], start=1):
                        st.write(f"{idx}. {step}")
                with col_b:
                    metric_card("Calories", f"{recipe['calories']:.0f}", "Per serving")
                    metric_card("Protein", f"{recipe['protein']:.0f} g", "High-protein focus")
                    metric_card("Carbs", f"{recipe['carbs']:.0f} g", "Per serving")
                    metric_card("Fats", f"{recipe['fats']:.0f} g", "Per serving")
                    st.caption("Tags")
                    tags = []
                    if recipe["is_spicy"]:
                        tags.append("Spicy")
                    if recipe["is_vegetarian"]:
                        tags.append("Vegetarian")
                    if recipe["is_egg_based"]:
                        tags.append("Egg based")
                    if recipe["is_soya_based"]:
                        tags.append("Soya based")
                    st.write(", ".join(tags) if tags else "None")
            serving_count = st.number_input(f"Serving count for {picked}", min_value=0.5, max_value=5.0, value=1.0, step=0.5, key=f"serving_{row['meal_type']}")
            if st.button(f"Add {picked}", key=f"add_{row['meal_type']}", use_container_width=True):
                insert_nutrition_log(
                    {
                        "date": log_date,
                        "meal_type": row["meal_type"].replace("_", " ").title(),
                        "food_name": recipe["recipe_name"],
                        "quantity": recipe["portion_note"],
                        "serving_count": serving_count,
                        "calories": recipe["calories"] * serving_count,
                        "protein": recipe["protein"] * serving_count,
                        "carbs": recipe["carbs"] * serving_count,
                        "fats": recipe["fats"] * serving_count,
                        "fiber": recipe["fiber"] * serving_count,
                        "source_type": "recipe",
                        "recipe_name": recipe["recipe_name"],
                        "notes": row.get("notes", "") or "",
                    }
                )
                st.success(f"Added {picked}.")
                st.rerun()

st.markdown("### Quick Add")
qa1, qa2 = st.columns(2)
with qa1:
    if st.button("Add Beast Life Whey Protein", use_container_width=True):
        whey = get_recipe_by_name("Beast Life Whey Protein")
        if whey:
            insert_nutrition_log(
                {
                    "date": log_date,
                    "meal_type": "Post-workout",
                    "food_name": whey["recipe_name"],
                    "quantity": whey["portion_note"],
                    "serving_count": 1,
                    "calories": whey["calories"],
                    "protein": whey["protein"],
                    "carbs": whey["carbs"],
                    "fats": whey["fats"],
                    "fiber": whey["fiber"],
                    "source_type": "quick_add",
                    "recipe_name": whey["recipe_name"],
                    "notes": "Quick-add whey",
                }
            )
            st.success("Whey added.")
            st.rerun()
with qa2:
    if st.button("Duplicate Yesterday's Meals", use_container_width=True):
        copied = copy_nutrition_logs((selected_date - timedelta(days=1)).isoformat(), log_date)
        if copied:
            st.success(f"Copied {copied} meals from yesterday.")
            st.rerun()
        status_banner("No meals found yesterday to duplicate.", "warning")

st.markdown("### Spicy Evening Snacks")
if spicy_snacks.empty:
    st.info("No spicy snack presets available.")
else:
    snack_cols = st.columns(2)
    for idx, (_, row) in enumerate(spicy_snacks.iterrows()):
        with snack_cols[idx % 2]:
            with st.container(border=True):
                st.subheader(row["recipe_name"])
                st.caption(row["portion_note"])
                st.write(f"{row['calories']:.0f} kcal • {row['protein']:.0f} g protein • {row['carbs']:.0f} g carbs • {row['fats']:.0f} g fats")
                if st.button(f"Add {row['recipe_name']}", key=f"snack_{row['id']}", use_container_width=True):
                    insert_nutrition_log(
                        {
                            "date": log_date,
                            "meal_type": "Snack",
                            "food_name": row["recipe_name"],
                            "quantity": row["portion_note"],
                            "serving_count": 1,
                            "calories": row["calories"],
                            "protein": row["protein"],
                            "carbs": row["carbs"],
                            "fats": row["fats"],
                            "fiber": row["fiber"],
                            "source_type": "snack_preset",
                            "recipe_name": row["recipe_name"],
                            "notes": "Spicy evening snack quick add",
                        }
                    )
                    st.success("Snack added.")
                    st.rerun()

st.markdown("### Recipe Library")
recipes_df = get_recipe_library_df()
if not recipes_df.empty:
    recipe_name = st.selectbox("Browse recipe details", recipes_df["recipe_name"].tolist())
    recipe = get_recipe_by_name(recipe_name)
    if recipe:
        with st.container(border=True):
            st.subheader(recipe["recipe_name"])
            st.caption(f"{recipe['meal_type'].replace('_', ' ').title()} • {recipe['portion_note']}")
            rc1, rc2 = st.columns(2)
            with rc1:
                st.write("Ingredients")
                for item in recipe["ingredients"]:
                    st.write(f"- {item['item']}: {item['quantity']}")
            with rc2:
                st.write("Steps")
                for idx, step in enumerate(recipe["steps"], start=1):
                    st.write(f"{idx}. {step}")

st.markdown("### Meal Log For Today")
meals = daily["meals"]
if meals.empty:
    st.info("No meals logged yet.")
else:
    editable_id = st.selectbox("Select meal entry", meals["id"].tolist(), format_func=lambda x: f"Entry #{x}")
    selected_row = meals[meals["id"] == editable_id].iloc[0]
    with st.expander("Edit meal entry"):
        with st.form("edit_meal_form"):
            c1, c2 = st.columns(2)
            with c1:
                edit_meal_type = st.text_input("Meal type", value=selected_row["meal_type"])
                edit_food_name = st.text_input("Food name", value=selected_row["food_name"])
                edit_quantity = st.text_input("Quantity", value=selected_row["quantity"])
                edit_notes = st.text_area("Notes", value=selected_row["notes"])
            with c2:
                edit_calories = st.number_input("Calories", min_value=0.0, value=float(selected_row["calories"]), step=10.0)
                edit_protein = st.number_input("Protein", min_value=0.0, value=float(selected_row["protein"]), step=1.0)
                edit_carbs = st.number_input("Carbs", min_value=0.0, value=float(selected_row["carbs"]), step=1.0)
                edit_fats = st.number_input("Fats", min_value=0.0, value=float(selected_row["fats"]), step=1.0)
                edit_fiber = st.number_input("Fiber", min_value=0.0, value=float(selected_row["fiber"]), step=1.0)
            if st.form_submit_button("Save Changes"):
                update_nutrition_log(
                    int(editable_id),
                    {
                        "meal_type": edit_meal_type,
                        "food_name": edit_food_name,
                        "quantity": edit_quantity,
                        "calories": edit_calories,
                        "protein": edit_protein,
                        "carbs": edit_carbs,
                        "fats": edit_fats,
                        "fiber": edit_fiber,
                        "notes": edit_notes,
                        "serving_count": float(selected_row.get("serving_count", 1) or 1),
                        "source_type": selected_row.get("source_type", "manual"),
                        "recipe_name": selected_row.get("recipe_name", edit_food_name),
                    },
                )
                st.success("Meal updated.")
                st.rerun()
        if st.button("Delete Meal Entry", type="secondary", use_container_width=True):
            delete_nutrition_log(int(editable_id))
            st.warning("Meal entry deleted.")
            st.rerun()
    st.dataframe(meals, use_container_width=True, hide_index=True)

breakdown = get_meal_breakdown(log_date)
if not breakdown.empty:
    st.plotly_chart(bar_chart(breakdown, "meal_type", "calories", "Meal-wise calorie breakdown", "#f97316"), use_container_width=True)

st.markdown("### Weekly Trends")
weekly_nutrition, weekly_summary = get_weekly_nutrition()
weekly_energy, weekly_energy_summary = get_weekly_energy_balance()
wc1, wc2 = st.columns(2)
with wc1:
    if not weekly_nutrition.empty:
        st.plotly_chart(bar_chart(weekly_nutrition, "date", "calories", "Daily calories consumed", "#2563eb"), use_container_width=True)
        st.plotly_chart(bar_chart(weekly_nutrition, "date", "protein", "Protein trend", "#16a34a"), use_container_width=True)
    else:
        st.info("Not enough nutrition data for weekly trends yet.")
with wc2:
    if not weekly_energy.empty:
        st.plotly_chart(bar_chart(weekly_energy, "date", "exercise_calories", "Daily calories burned", "#ef4444"), use_container_width=True)
        st.plotly_chart(bar_chart(weekly_energy, "date", "deficit_or_surplus", "Deficit trend", "#8b5cf6"), use_container_width=True)
    else:
        st.info("Not enough energy balance data yet.")

status_banner(
    f"Average daily calories: {weekly_summary['avg_calories']:.0f} • Average daily protein: {weekly_summary['avg_protein']:.0f} g • Weekly avg deficit: {weekly_energy_summary['weekly_average_deficit']:.0f} • Estimated fat loss pace: {weekly_energy_summary['estimated_fat_loss_kg_per_week']:.2f} kg/week",
    "success" if weekly_energy_summary["weekly_average_deficit"] > 0 else "warning",
)

st.download_button("Export nutrition CSV", get_nutrition_export_df().to_csv(index=False).encode("utf-8"), "nutrition_logs.csv")
