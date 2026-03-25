"""Exercise seed data for the fitness tracker app."""

from __future__ import annotations

from typing import TypedDict


class SeedExercise(TypedDict):
    name: str
    day_type: str
    muscle_group: str


CUSTOM_EXERCISES: list[SeedExercise] = [
    # Chest / Push
    {"name": "Flat Dumbbell Press", "day_type": "Push", "muscle_group": "Chest"},
    {"name": "Flat Barbell Bench Press", "day_type": "Push", "muscle_group": "Chest"},
    {"name": "Incline Dumbbell Press", "day_type": "Push", "muscle_group": "Upper Chest"},
    {"name": "Incline Barbell Bench Press", "day_type": "Push", "muscle_group": "Upper Chest"},
    {"name": "Incline Machine Press", "day_type": "Push", "muscle_group": "Upper Chest"},
    {"name": "Chest Press Machine", "day_type": "Push", "muscle_group": "Chest"},
    {"name": "Smith Machine Press", "day_type": "Push", "muscle_group": "Chest"},
    {"name": "Pec Deck Fly", "day_type": "Push", "muscle_group": "Chest"},
    {"name": "Cable Fly", "day_type": "Push", "muscle_group": "Chest"},
    {"name": "High to Low Cable Crossover", "day_type": "Push", "muscle_group": "Lower Chest"},
    {"name": "Low to High Cable Fly", "day_type": "Push", "muscle_group": "Upper Chest"},
    {"name": "Push-ups", "day_type": "Push", "muscle_group": "Chest"},
    {"name": "Weighted Push-ups", "day_type": "Push", "muscle_group": "Chest"},
    {"name": "Dips", "day_type": "Push", "muscle_group": "Lower Chest"},
    # Shoulders
    {"name": "Shoulder Press", "day_type": "Push", "muscle_group": "Front Delts"},
    {"name": "Dumbbell Shoulder Press", "day_type": "Push", "muscle_group": "Front Delts"},
    {"name": "Machine Shoulder Press", "day_type": "Push", "muscle_group": "Front Delts"},
    {"name": "Arnold Press", "day_type": "Push", "muscle_group": "Front Delts"},
    {"name": "Cable Lateral Raise", "day_type": "Push", "muscle_group": "Side Delts"},
    {"name": "Dumbbell Lateral Raise", "day_type": "Push", "muscle_group": "Side Delts"},
    {"name": "Front Raise", "day_type": "Push", "muscle_group": "Front Delts"},
    {"name": "Reverse Pec Deck", "day_type": "Pull", "muscle_group": "Rear Delts"},
    {"name": "Face Pull", "day_type": "Pull", "muscle_group": "Rear Delts"},
    {"name": "Rear Delt Fly", "day_type": "Pull", "muscle_group": "Rear Delts"},
    {"name": "Upright Row", "day_type": "Pull", "muscle_group": "Traps"},
    # Triceps
    {"name": "Rope Pushdown", "day_type": "Push", "muscle_group": "Triceps"},
    {"name": "Straight Bar Pushdown", "day_type": "Push", "muscle_group": "Triceps"},
    {"name": "Overhead Rope Extension", "day_type": "Push", "muscle_group": "Triceps"},
    {"name": "Skull Crushers", "day_type": "Push", "muscle_group": "Triceps"},
    {"name": "Cable Tricep Skull Crusher", "day_type": "Push", "muscle_group": "Triceps"},
    {"name": "Close Grip Bench Press", "day_type": "Push", "muscle_group": "Triceps"},
    {"name": "Bench Dips", "day_type": "Push", "muscle_group": "Triceps"},
    # Back / Lats
    {"name": "Lat Pulldown", "day_type": "Pull", "muscle_group": "Lats"},
    {"name": "Wide Grip Lat Pulldown", "day_type": "Pull", "muscle_group": "Lats"},
    {"name": "Close Grip Lat Pulldown", "day_type": "Pull", "muscle_group": "Lats"},
    {"name": "Pull-ups", "day_type": "Pull", "muscle_group": "Lats"},
    {"name": "Assisted Pull-ups", "day_type": "Pull", "muscle_group": "Lats"},
    {"name": "Seated Cable Row", "day_type": "Pull", "muscle_group": "Back"},
    {"name": "Seated Machine Row Wide Grip", "day_type": "Pull", "muscle_group": "Upper Back"},
    {"name": "Seated Machine Row Close Grip", "day_type": "Pull", "muscle_group": "Back"},
    {"name": "Barbell Row", "day_type": "Pull", "muscle_group": "Back"},
    {"name": "T-Bar Row", "day_type": "Pull", "muscle_group": "Upper Back"},
    {"name": "Dumbbell Row", "day_type": "Pull", "muscle_group": "Back"},
    {"name": "Chest Supported Row", "day_type": "Pull", "muscle_group": "Upper Back"},
    {"name": "Straight Arm Pulldown", "day_type": "Pull", "muscle_group": "Lats"},
    {"name": "Shrugs", "day_type": "Pull", "muscle_group": "Traps"},
    # Biceps / forearms
    {"name": "Dumbbell Curl", "day_type": "Pull", "muscle_group": "Biceps"},
    {"name": "Alternating Dumbbell Curl", "day_type": "Pull", "muscle_group": "Biceps"},
    {"name": "Machine Curl", "day_type": "Pull", "muscle_group": "Biceps"},
    {"name": "Hammer Curl", "day_type": "Pull", "muscle_group": "Biceps"},
    {"name": "Preacher Curl", "day_type": "Pull", "muscle_group": "Biceps"},
    {"name": "Cable Curl", "day_type": "Pull", "muscle_group": "Biceps"},
    {"name": "Bayesian Curl", "day_type": "Pull", "muscle_group": "Biceps"},
    {"name": "Concentration Curl", "day_type": "Pull", "muscle_group": "Biceps"},
    {"name": "EZ Bar Curl", "day_type": "Pull", "muscle_group": "Biceps"},
    {"name": "Wrist Curl", "day_type": "Pull", "muscle_group": "Forearms"},
    {"name": "Reverse Wrist Curl", "day_type": "Pull", "muscle_group": "Forearms"},
    # Legs
    {"name": "Squat", "day_type": "Legs", "muscle_group": "Quads"},
    {"name": "Back Squat", "day_type": "Legs", "muscle_group": "Quads"},
    {"name": "Front Squat", "day_type": "Legs", "muscle_group": "Quads"},
    {"name": "Smith Machine Squat", "day_type": "Legs", "muscle_group": "Quads"},
    {"name": "Squat Machine", "day_type": "Legs", "muscle_group": "Quads"},
    {"name": "Leg Press", "day_type": "Legs", "muscle_group": "Quads"},
    {"name": "Leg Extension", "day_type": "Legs", "muscle_group": "Quads"},
    {"name": "Romanian Deadlift", "day_type": "Legs", "muscle_group": "Hamstrings"},
    {"name": "Barbell RDL", "day_type": "Legs", "muscle_group": "Hamstrings"},
    {"name": "Dumbbell RDL", "day_type": "Legs", "muscle_group": "Hamstrings"},
    {"name": "Leg Curl", "day_type": "Legs", "muscle_group": "Hamstrings"},
    {"name": "Seated Leg Curl", "day_type": "Legs", "muscle_group": "Hamstrings"},
    {"name": "Lying Leg Curl", "day_type": "Legs", "muscle_group": "Hamstrings"},
    {"name": "Bulgarian Split Squat", "day_type": "Legs", "muscle_group": "Glutes"},
    {"name": "Walking Lunges", "day_type": "Legs", "muscle_group": "Glutes"},
    {"name": "Hip Thrust", "day_type": "Legs", "muscle_group": "Glutes"},
    {"name": "Glute Bridge", "day_type": "Legs", "muscle_group": "Glutes"},
    {"name": "Calf Raises", "day_type": "Legs", "muscle_group": "Calves"},
    {"name": "Seated Calf Raise", "day_type": "Legs", "muscle_group": "Calves"},
    {"name": "Standing Calf Raise", "day_type": "Legs", "muscle_group": "Calves"},
    # Core
    {"name": "Crunches", "day_type": "Full Body", "muscle_group": "Abs"},
    {"name": "Cable Crunch", "day_type": "Full Body", "muscle_group": "Abs"},
    {"name": "Hanging Leg Raise", "day_type": "Full Body", "muscle_group": "Abs"},
    {"name": "Plank", "day_type": "Full Body", "muscle_group": "Abs"},
    {"name": "Russian Twists", "day_type": "Full Body", "muscle_group": "Obliques"},
    {"name": "Ab Wheel", "day_type": "Full Body", "muscle_group": "Abs"},
    {"name": "Mountain Climbers", "day_type": "Full Body", "muscle_group": "Full Body"},
    {"name": "Dead Bug", "day_type": "Full Body", "muscle_group": "Abs"},
    {"name": "Pallof Press", "day_type": "Full Body", "muscle_group": "Obliques"},
    # Cardio
    {"name": "Treadmill Running", "day_type": "Cardio", "muscle_group": "Cardio"},
    {"name": "Incline Walking", "day_type": "Cardio", "muscle_group": "Cardio"},
    {"name": "Cycling", "day_type": "Cardio", "muscle_group": "Cardio"},
    {"name": "Stairmaster", "day_type": "Cardio", "muscle_group": "Cardio"},
    {"name": "Rowing Machine", "day_type": "Cardio", "muscle_group": "Cardio"},
    {"name": "Elliptical", "day_type": "Cardio", "muscle_group": "Cardio"},
    {"name": "Jump Rope", "day_type": "Cardio", "muscle_group": "Cardio"},
    {"name": "Outdoor Walk", "day_type": "Cardio", "muscle_group": "Cardio"},
    {"name": "Outdoor Run", "day_type": "Cardio", "muscle_group": "Cardio"},
    {"name": "Sled Push", "day_type": "Full Body", "muscle_group": "Full Body"},
    # Upper / Lower variants
    {"name": "Cable Row", "day_type": "Upper", "muscle_group": "Back"},
    {"name": "Bench Press", "day_type": "Upper", "muscle_group": "Chest"},
    {"name": "Pull Down", "day_type": "Upper", "muscle_group": "Lats"},
    {"name": "Leg Press Heavy", "day_type": "Lower", "muscle_group": "Quads"},
    {"name": "RDL Heavy", "day_type": "Lower", "muscle_group": "Hamstrings"},
]


EXERCISES = [(e["name"], e["day_type"], e["muscle_group"]) for e in CUSTOM_EXERCISES]


def get_custom_exercises() -> list[SeedExercise]:
    return CUSTOM_EXERCISES.copy()
