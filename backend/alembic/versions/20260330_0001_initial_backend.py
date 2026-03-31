"""initial backend schema

Revision ID: 20260330_0001
Revises:
Create Date: 2026-03-30 23:55:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260330_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "exercise_library",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("day_type", sa.String(length=64), nullable=False),
        sa.Column("muscle_group", sa.String(length=128), nullable=False),
        sa.Column("youtube_url", sa.String(length=1024), nullable=False, server_default=""),
        sa.Column("youtube_search_url", sa.String(length=1024), nullable=False, server_default=""),
        sa.Column("instructions_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("common_mistakes_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("tips", sa.Text(), nullable=False, server_default=""),
        sa.Column("matched", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("name", name="uq_exercise_library_name"),
    )
    op.create_index("ix_exercise_library_name", "exercise_library", ["name"])
    op.create_index("ix_exercise_library_day_type", "exercise_library", ["day_type"])
    op.create_index("ix_exercise_library_muscle_group", "exercise_library", ["muscle_group"])

    op.create_table(
        "recipe_library",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("recipe_name", sa.String(length=255), nullable=False),
        sa.Column("meal_type", sa.String(length=64), nullable=False),
        sa.Column("ingredients_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("steps_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("calories", sa.Float(), nullable=False, server_default="0"),
        sa.Column("protein", sa.Float(), nullable=False, server_default="0"),
        sa.Column("carbs", sa.Float(), nullable=False, server_default="0"),
        sa.Column("fats", sa.Float(), nullable=False, server_default="0"),
        sa.Column("fiber", sa.Float(), nullable=False, server_default="0"),
        sa.Column("portion_note", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("is_spicy", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("is_vegetarian", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("is_egg_based", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("is_soya_based", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("recipe_name", name="uq_recipe_library_recipe_name"),
    )
    op.create_index("ix_recipe_library_recipe_name", "recipe_library", ["recipe_name"])
    op.create_index("ix_recipe_library_meal_type", "recipe_library", ["meal_type"])

    op.create_table(
        "diet_plan_templates",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("day_name", sa.String(length=16), nullable=False),
        sa.Column("meal_type", sa.String(length=64), nullable=False),
        sa.Column("option_1", sa.String(length=255)),
        sa.Column("option_2", sa.String(length=255)),
        sa.Column("option_3", sa.String(length=255)),
        sa.Column("option_4", sa.String(length=255)),
        sa.Column("notes", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_diet_plan_templates_day_name", "diet_plan_templates", ["day_name"])
    op.create_index("ix_diet_plan_templates_meal_type", "diet_plan_templates", ["meal_type"])

    op.create_table(
        "user_profile",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("age", sa.Integer()),
        sa.Column("gender", sa.String(length=20)),
        sa.Column("height_cm", sa.Float()),
        sa.Column("current_weight_kg", sa.Float()),
        sa.Column("activity_level", sa.String(length=32)),
        sa.Column("goal", sa.String(length=32)),
        sa.Column("desired_deficit", sa.Float()),
        sa.Column("challenge_start_date", sa.Date()),
        sa.Column("target_weight_kg", sa.Float()),
        sa.Column("preferred_diet_plan_name", sa.String(length=255)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_user_profile_id", "user_profile", ["id"])

    op.create_table(
        "body_metrics",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("profile_id", sa.Integer(), sa.ForeignKey("user_profile.id", ondelete="CASCADE"), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("body_weight", sa.Float()),
        sa.Column("waist", sa.Float()),
        sa.Column("chest", sa.Float()),
        sa.Column("arms", sa.Float()),
        sa.Column("thigh", sa.Float()),
        sa.Column("body_fat_percent", sa.Float()),
        sa.Column("notes", sa.Text(), nullable=False, server_default=""),
        sa.Column("hips", sa.Float()),
        sa.Column("neck", sa.Float()),
        sa.Column("thighs", sa.Float()),
        sa.Column("progress_notes", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_body_metrics_profile_id", "body_metrics", ["profile_id"])
    op.create_index("ix_body_metrics_date", "body_metrics", ["date"])

    op.create_table(
        "cardio_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("profile_id", sa.Integer(), sa.ForeignKey("user_profile.id", ondelete="CASCADE"), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("cardio_type", sa.String(length=128), nullable=False),
        sa.Column("duration_min", sa.Integer(), nullable=False),
        sa.Column("calories", sa.Integer()),
        sa.Column("intensity", sa.String(length=32)),
        sa.Column("notes", sa.Text(), nullable=False, server_default=""),
        sa.Column("is_outdoor", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("distance_km", sa.Float(), nullable=False, server_default="0"),
        sa.Column("pace_text", sa.String(length=64), nullable=False, server_default=""),
        sa.Column("estimated_calories_burned", sa.Float(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_cardio_logs_profile_id", "cardio_logs", ["profile_id"])
    op.create_index("ix_cardio_logs_date", "cardio_logs", ["date"])

    op.create_table(
        "challenge_days",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("profile_id", sa.Integer(), sa.ForeignKey("user_profile.id", ondelete="CASCADE"), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("challenge_day_number", sa.Integer()),
        sa.Column("workout_1_completed", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("workout_2_completed", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("one_workout_outdoors", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("followed_diet", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("no_cheat_meals", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("no_alcohol", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("water_goal_completed", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("progress_picture_taken", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("body_weight", sa.Float()),
        sa.Column("steps", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("sleep_hours", sa.Float(), nullable=False, server_default="0"),
        sa.Column("mood", sa.String(length=120), nullable=False, server_default=""),
        sa.Column("energy_level", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("notes", sa.Text(), nullable=False, server_default=""),
        sa.Column("selected_diet_plan", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("diet_followed", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("cheat_meal", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("junk_food", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("sugary_drinks", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("hunger_level", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("cravings_level", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("binge_urge", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("diet_notes", sa.Text(), nullable=False, server_default=""),
        sa.Column("day_status", sa.String(length=32), nullable=False, server_default="incomplete"),
        sa.Column("compliance_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("profile_id", "date", name="uq_challenge_days_profile_date"),
    )
    op.create_index("ix_challenge_days_profile_id", "challenge_days", ["profile_id"])
    op.create_index("ix_challenge_days_date", "challenge_days", ["date"])

    op.create_table(
        "daily_targets",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("profile_id", sa.Integer(), sa.ForeignKey("user_profile.id", ondelete="CASCADE"), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("calorie_target", sa.Float(), nullable=False, server_default="2200"),
        sa.Column("protein_target", sa.Float(), nullable=False, server_default="180"),
        sa.Column("carbs_target", sa.Float(), nullable=False, server_default="200"),
        sa.Column("fats_target", sa.Float(), nullable=False, server_default="70"),
        sa.Column("fiber_target", sa.Float(), nullable=False, server_default="30"),
        sa.Column("water_target_liters", sa.Float(), nullable=False, server_default="4"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("profile_id", "date", name="uq_daily_targets_profile_date"),
    )
    op.create_index("ix_daily_targets_profile_id", "daily_targets", ["profile_id"])
    op.create_index("ix_daily_targets_date", "daily_targets", ["date"])

    op.create_table(
        "hydration_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("profile_id", sa.Integer(), sa.ForeignKey("user_profile.id", ondelete="CASCADE"), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("amount_ml", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_hydration_logs_profile_id", "hydration_logs", ["profile_id"])
    op.create_index("ix_hydration_logs_date", "hydration_logs", ["date"])

    op.create_table(
        "nutrition_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("profile_id", sa.Integer(), sa.ForeignKey("user_profile.id", ondelete="CASCADE"), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("meal_type", sa.String(length=64), nullable=False),
        sa.Column("food_name", sa.String(length=255), nullable=False),
        sa.Column("quantity", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("serving_count", sa.Float(), nullable=False, server_default="1"),
        sa.Column("calories", sa.Float(), nullable=False, server_default="0"),
        sa.Column("protein", sa.Float(), nullable=False, server_default="0"),
        sa.Column("carbs", sa.Float(), nullable=False, server_default="0"),
        sa.Column("fats", sa.Float(), nullable=False, server_default="0"),
        sa.Column("fiber", sa.Float(), nullable=False, server_default="0"),
        sa.Column("notes", sa.Text(), nullable=False, server_default=""),
        sa.Column("source_type", sa.String(length=64), nullable=False, server_default="manual"),
        sa.Column("recipe_name", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_nutrition_logs_profile_id", "nutrition_logs", ["profile_id"])
    op.create_index("ix_nutrition_logs_date", "nutrition_logs", ["date"])

    op.create_table(
        "progress_photos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("profile_id", sa.Integer(), sa.ForeignKey("user_profile.id", ondelete="CASCADE"), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("photo_type", sa.String(length=32), nullable=False, server_default="front"),
        sa.Column("file_url", sa.String(length=1024), nullable=False),
        sa.Column("blob_key", sa.String(length=512)),
        sa.Column("notes", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_progress_photos_profile_id", "progress_photos", ["profile_id"])
    op.create_index("ix_progress_photos_date", "progress_photos", ["date"])

    op.create_table(
        "weekly_reviews",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("profile_id", sa.Integer(), sa.ForeignKey("user_profile.id", ondelete="CASCADE"), nullable=False),
        sa.Column("week_start", sa.Date(), nullable=False),
        sa.Column("what_went_well", sa.Text(), nullable=False, server_default=""),
        sa.Column("what_was_difficult", sa.Text(), nullable=False, server_default=""),
        sa.Column("focus_for_next_week", sa.Text(), nullable=False, server_default=""),
        sa.Column("notes", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("profile_id", "week_start", name="uq_weekly_reviews_profile_week"),
    )
    op.create_index("ix_weekly_reviews_profile_id", "weekly_reviews", ["profile_id"])
    op.create_index("ix_weekly_reviews_week_start", "weekly_reviews", ["week_start"])

    op.create_table(
        "workouts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("profile_id", sa.Integer(), sa.ForeignKey("user_profile.id", ondelete="CASCADE"), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("day_type", sa.String(length=64), nullable=False),
        sa.Column("session_type", sa.String(length=32), nullable=False, server_default="Workout 1"),
        sa.Column("is_outdoor", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("duration_min", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("start_time", sa.Time()),
        sa.Column("end_time", sa.Time()),
        sa.Column("session_notes", sa.Text(), nullable=False, server_default=""),
        sa.Column("estimated_calories_burned", sa.Float(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_workouts_profile_id", "workouts", ["profile_id"])
    op.create_index("ix_workouts_date", "workouts", ["date"])

    op.create_table(
        "workout_exercises",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("workout_id", sa.Integer(), sa.ForeignKey("workouts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("exercise_name", sa.String(length=255), nullable=False),
        sa.Column("muscle_group", sa.String(length=128), nullable=False, server_default=""),
        sa.Column("weight", sa.Float(), nullable=False, server_default="0"),
        sa.Column("reps", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("sets", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("volume", sa.Float(), nullable=False, server_default="0"),
        sa.Column("near_failure", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("new_pr", sa.String(length=32), nullable=False, server_default=""),
        sa.Column("notes", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_workout_exercises_workout_id", "workout_exercises", ["workout_id"])
    op.create_index("ix_workout_exercises_exercise_name", "workout_exercises", ["exercise_name"])


def downgrade() -> None:
    op.drop_index("ix_workout_exercises_exercise_name", table_name="workout_exercises")
    op.drop_index("ix_workout_exercises_workout_id", table_name="workout_exercises")
    op.drop_table("workout_exercises")
    op.drop_index("ix_workouts_date", table_name="workouts")
    op.drop_index("ix_workouts_profile_id", table_name="workouts")
    op.drop_table("workouts")
    op.drop_index("ix_weekly_reviews_week_start", table_name="weekly_reviews")
    op.drop_index("ix_weekly_reviews_profile_id", table_name="weekly_reviews")
    op.drop_table("weekly_reviews")
    op.drop_index("ix_progress_photos_date", table_name="progress_photos")
    op.drop_index("ix_progress_photos_profile_id", table_name="progress_photos")
    op.drop_table("progress_photos")
    op.drop_index("ix_nutrition_logs_date", table_name="nutrition_logs")
    op.drop_index("ix_nutrition_logs_profile_id", table_name="nutrition_logs")
    op.drop_table("nutrition_logs")
    op.drop_index("ix_hydration_logs_date", table_name="hydration_logs")
    op.drop_index("ix_hydration_logs_profile_id", table_name="hydration_logs")
    op.drop_table("hydration_logs")
    op.drop_index("ix_daily_targets_date", table_name="daily_targets")
    op.drop_index("ix_daily_targets_profile_id", table_name="daily_targets")
    op.drop_table("daily_targets")
    op.drop_index("ix_challenge_days_date", table_name="challenge_days")
    op.drop_index("ix_challenge_days_profile_id", table_name="challenge_days")
    op.drop_table("challenge_days")
    op.drop_index("ix_cardio_logs_date", table_name="cardio_logs")
    op.drop_index("ix_cardio_logs_profile_id", table_name="cardio_logs")
    op.drop_table("cardio_logs")
    op.drop_index("ix_body_metrics_date", table_name="body_metrics")
    op.drop_index("ix_body_metrics_profile_id", table_name="body_metrics")
    op.drop_table("body_metrics")
    op.drop_index("ix_user_profile_id", table_name="user_profile")
    op.drop_table("user_profile")
    op.drop_index("ix_diet_plan_templates_meal_type", table_name="diet_plan_templates")
    op.drop_index("ix_diet_plan_templates_day_name", table_name="diet_plan_templates")
    op.drop_table("diet_plan_templates")
    op.drop_index("ix_recipe_library_meal_type", table_name="recipe_library")
    op.drop_index("ix_recipe_library_recipe_name", table_name="recipe_library")
    op.drop_table("recipe_library")
    op.drop_index("ix_exercise_library_muscle_group", table_name="exercise_library")
    op.drop_index("ix_exercise_library_day_type", table_name="exercise_library")
    op.drop_index("ix_exercise_library_name", table_name="exercise_library")
    op.drop_table("exercise_library")
