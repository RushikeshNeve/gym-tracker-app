DAY_TYPES = ["Push", "Pull", "Legs", "Upper", "Lower", "Cardio", "Full Body", "Active Recovery"]
WORKOUT_SESSION_TYPES = ["Workout 1", "Workout 2"]
MEAL_TYPES = ["Breakfast", "Lunch", "Dinner", "Snack", "Pre-workout", "Post-workout"]
PHOTO_TYPES = ["front", "side", "back"]
WEEKDAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
ACTIVITY_LEVELS = ["sedentary", "lightly_active", "moderately_active", "very_active"]
GOAL_TYPES = ["fat_loss", "maintenance", "recomp"]

DEFAULT_TARGETS = {
    "calorie_target": 2200.0,
    "protein_target": 180.0,
    "carbs_target": 200.0,
    "fats_target": 70.0,
    "fiber_target": 30.0,
    "water_target_liters": 4.0,
}

REQUIRED_TASK_LABELS = {
    "workout_1_completed": "Workout 1",
    "one_workout_outdoors": "Outdoor workout",
    "followed_diet": "Followed diet",
    "no_cheat_meals": "No cheat meals",
    "water_goal_completed": "Water goal",
    "progress_picture_taken": "Progress photo",
}

REQUIRED_TASK_KEYS = list(REQUIRED_TASK_LABELS.keys())
