from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.body_metrics import BodyMetric
from app.models.cardio_logs import CardioLog
from app.models.challenge_days import ChallengeDay
from app.models.hydration_logs import HydrationLog
from app.models.nutrition_logs import NutritionLog
from app.models.progress_photos import ProgressPhoto
from app.models.user_profile import UserProfile
from app.models.workouts import Workout, WorkoutExercise
from app.seeds.seed_reference_data import main as seed_reference_data
from app.services.profile_service import ensure_profile, get_or_create_daily_target


def main() -> None:
    seed_reference_data()
    with SessionLocal() as db:
        profile = ensure_profile(db)
        challenge_start = profile.challenge_start_date or (date.today() + timedelta(days=1))

        if not db.scalar(select(Workout).limit(1)):
            workout = Workout(
                profile_id=profile.id,
                date=challenge_start - timedelta(days=2),
                day_type="Push",
                session_type="Workout 1",
                is_outdoor=False,
                duration_min=55,
                session_notes="Morning lift",
                estimated_calories_burned=310,
            )
            db.add(workout)
            db.flush()
            db.add(
                WorkoutExercise(
                    workout_id=workout.id,
                    exercise_name="Incline Machine Press",
                    muscle_group="Upper Chest",
                    weight=60,
                    reps=10,
                    sets=3,
                    volume=1800,
                    near_failure=True,
                    new_pr="First",
                    notes="Solid set",
                )
            )

        if not db.scalar(select(BodyMetric).limit(1)):
            db.add_all(
                [
                    BodyMetric(profile_id=profile.id, date=challenge_start - timedelta(days=2), body_weight=84.2, waist=92.0, chest=104.0, arms=36.0, thighs=57.0, body_fat_percent=22.5, progress_notes="Baseline"),
                    BodyMetric(profile_id=profile.id, date=challenge_start, body_weight=83.6, waist=91.2, chest=103.5, arms=36.1, thighs=56.8, body_fat_percent=22.0, progress_notes="Waist moving down"),
                ]
            )

        if not db.scalar(select(CardioLog).limit(1)):
            db.add_all(
                [
                    CardioLog(profile_id=profile.id, date=challenge_start - timedelta(days=1), cardio_type="Outdoor Walk", duration_min=45, calories=260, intensity="Moderate", notes="Evening walk", is_outdoor=True, distance_km=4.8, pace_text="09:15 /km", estimated_calories_burned=260),
                    CardioLog(profile_id=profile.id, date=challenge_start, cardio_type="Stairmaster", duration_min=15, calories=180, intensity="Hard", notes="Finisher", is_outdoor=False, distance_km=0, pace_text="", estimated_calories_burned=180),
                ]
            )

        if not db.scalar(select(NutritionLog).limit(1)):
            today = date.today()
            db.add_all(
                [
                    NutritionLog(profile_id=profile.id, date=today, meal_type="Breakfast", food_name="Egg Bhurji Toast Combo", quantity="1 serving", calories=390, protein=26, carbs=24, fats=20, fiber=4, notes="Quick breakfast", serving_count=1, source_type="recipe", recipe_name="Egg Bhurji Toast Combo"),
                    NutritionLog(profile_id=profile.id, date=today, meal_type="Post-workout", food_name="Beast Life Whey Protein", quantity="1 scoop", calories=120, protein=24, carbs=3, fats=2, fiber=0, notes="", serving_count=1, source_type="quick_add", recipe_name="Beast Life Whey Protein"),
                ]
            )

        if not db.scalar(select(HydrationLog).limit(1)):
            today = date.today()
            db.add_all(
                [
                    HydrationLog(profile_id=profile.id, date=today, amount_ml=500),
                    HydrationLog(profile_id=profile.id, date=today, amount_ml=250),
                ]
            )

        if not db.scalar(select(ChallengeDay).limit(1)):
            db.add_all(
                [
                    ChallengeDay(profile_id=profile.id, date=challenge_start - timedelta(days=2), challenge_day_number=1, workout_1_completed=True, workout_2_completed=True, one_workout_outdoors=True, followed_diet=True, no_cheat_meals=True, no_alcohol=True, water_goal_completed=True, progress_picture_taken=True, body_weight=84.0, steps=11250, sleep_hours=7.4, mood="Focused", energy_level=8, selected_diet_plan="High protein calorie deficit", diet_followed=True, day_status="perfect", compliance_score=100),
                    ChallengeDay(profile_id=profile.id, date=challenge_start - timedelta(days=1), challenge_day_number=2, workout_1_completed=True, workout_2_completed=False, one_workout_outdoors=True, followed_diet=True, no_cheat_meals=True, no_alcohol=True, water_goal_completed=False, progress_picture_taken=False, body_weight=83.8, steps=9050, sleep_hours=6.8, mood="Tired", energy_level=6, selected_diet_plan="High protein calorie deficit", diet_followed=True, day_status="failed", compliance_score=58),
                ]
            )

        if not db.scalar(select(ProgressPhoto).limit(1)):
            db.add_all(
                [
                    ProgressPhoto(profile_id=profile.id, date=challenge_start - timedelta(days=2), photo_type="front", file_url="https://example.com/progress/day1_front.jpg", blob_key="progress/day1_front.jpg", notes="Sample metadata"),
                    ProgressPhoto(profile_id=profile.id, date=challenge_start, photo_type="side", file_url="https://example.com/progress/day3_side.jpg", blob_key="progress/day3_side.jpg", notes="Sample metadata"),
                ]
            )

        for offset in range(-1, 2):
            get_or_create_daily_target(db, profile, challenge_start + timedelta(days=offset))

        db.commit()
        print("Demo data seeded.")


if __name__ == "__main__":
    main()
