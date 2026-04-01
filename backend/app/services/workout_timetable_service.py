from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.exercise_library import ExerciseLibrary


WEEKLY_SPLIT = [
    {"day": "Day 1", "workout": "Push"},
    {"day": "Day 2", "workout": "Pull"},
    {"day": "Day 3", "workout": "Legs"},
    {"day": "Day 4", "workout": "Push"},
    {"day": "Day 5", "workout": "Pull"},
    {"day": "Day 6", "workout": "Cardio + Core"},
    {"day": "Day 7", "workout": "Rest"},
]


TIMETABLE_CONFIG = [
    {
        "id": "push",
        "day_label": "Day 1 & 4",
        "title": "Push",
        "subtitle": "Chest + Shoulders + Triceps",
        "accent": "primary",
        "notes": ["Finish the session with 10-15 minutes of incline treadmill, elliptical, or cycling."],
        "images": [
            "https://www.puregym.com/media/h3gjo30x/dumbbell-bench-press.jpg?quality=80",
            "https://blog.myarsenalstrength.com/hubfs/chest%20press.webp",
            "https://cdn.muscleandstrength.com/sites/default/files/standing-high-to-low-cable-fly-1.jpg",
            "https://www.chrisadamspersonaltraining.com/uploads/1/3/2/1/132150751/published/screenshot-20210803-132234-gallery.jpg?1628000356=",
            "https://cdn.shopify.com/s/files/1/0618/9462/3460/files/stock-photo-beautiful-young-caucasian-female-athlete-exercising-with-cable-crossover-machine-in-fitness-gym-1846648126-800x571.jpg",
        ],
        "blocks": [
            {"category": "Chest Press", "sets_reps": "3 x 8-12", "options": ["Flat Dumbbell Press", "Smith Machine Press", "Flat Barbell Bench Press"]},
            {"category": "Incline Chest", "sets_reps": "3 x 8-12", "options": ["Incline Machine Press", "Incline Dumbbell Press", "Incline Barbell Bench Press"]},
            {"category": "Chest Isolation", "sets_reps": "3 x 10-12", "options": ["High to Low Cable Crossover", "Pec Deck Fly", "Cable Fly"]},
            {"category": "Shoulders", "sets_reps": "3 x 12-15", "options": ["Cable Lateral Raise", "Dumbbell Lateral Raise", "Machine Shoulder Press"]},
            {"category": "Triceps 1", "sets_reps": "3 x 10-12", "options": ["Rope Pushdown", "Skull Crushers", "Dips"]},
            {"category": "Triceps 2", "sets_reps": "3 x 10-12", "options": ["Overhead Rope Extension", "Cable Tricep Skull Crusher", "Close Grip Bench Press"]},
            {"category": "Workout Finisher Cardio", "sets_reps": "10-15 min", "options": ["Incline Walking", "Elliptical", "Cycling"]},
        ],
    },
    {
        "id": "pull",
        "day_label": "Day 2 & 5",
        "title": "Pull",
        "subtitle": "Back + Biceps",
        "accent": "secondary",
        "notes": ["Finish the session with 10-15 minutes of incline treadmill, elliptical, or cycling."],
        "images": [
            "https://www.puregym.com/media/mmijlfwq/wide-grip-lat-pulldown.jpg?quality=80",
            "https://www.puregym.com/media/0epkvais/seated-row.jpg?quality=80",
            "https://www.soletreadmills.com/cdn/shop/articles/A_man_doing_a_barbell_bent_over_row..png?v=1751312161&width=2048",
            "https://blog.myarsenalstrength.com/hs-fs/hubfs/Bent%20over%20row%20exercise.png",
            "https://hips.hearstapps.com/menshealth-uk/main/assets/row-under.gif",
        ],
        "blocks": [
            {"category": "Vertical Pull", "sets_reps": "3 x 8-12", "options": ["Lat Pulldown", "Assisted Pull-ups", "Pull-ups"]},
            {"category": "Row (Wide)", "sets_reps": "3 x 8-12", "options": ["Seated Machine Row Wide Grip", "Cable Row", "Barbell Row"]},
            {"category": "Row (Close)", "sets_reps": "3 x 8-12", "options": ["Seated Machine Row Close Grip", "Seated Cable Row", "T-Bar Row"]},
            {"category": "Traps", "sets_reps": "3 x 10-12", "options": ["Shrugs", "Upright Row", "Face Pull"]},
            {"category": "Biceps 1", "sets_reps": "3 x 10-12", "options": ["Machine Curl", "EZ Bar Curl", "Cable Curl"]},
            {"category": "Biceps 2", "sets_reps": "3 x 10-12", "options": ["Hammer Curl", "Bayesian Curl", "Dumbbell Curl"]},
            {"category": "Workout Finisher Cardio", "sets_reps": "10-15 min", "options": ["Incline Walking", "Elliptical", "Cycling"]},
        ],
    },
    {
        "id": "legs",
        "day_label": "Day 3",
        "title": "Legs",
        "subtitle": "Strength Focus",
        "accent": "warning",
        "notes": [
            "Keep same structure on repeat days.",
            "Rotate exercise options after 2-3 weeks or when equipment availability changes.",
            "Finish the session with 10-15 minutes of incline treadmill, elliptical, or cycling.",
        ],
        "images": [
            "https://bellsofsteel.com/cdn/shop/articles/How-To-Use-Hack-Squat-Machine.webp?v=1708539914&width=1024",
            "https://hips.hearstapps.com/hmg-prod/images/woman-lifting-weight-on-legs-royalty-free-image-1704915259.jpg?crop=0.670xw%3A1.00xh%3B0.0801xw%2C0&resize=1200%3A%2A",
            "https://www.puregym.com/media/5gwmhhys/romanian-deadlift.jpg?quality=80",
            "https://cdn.muscleandstrength.com/sites/default/files/romanian-deadlift.jpg",
            "https://content.artofmanliness.com/uploads/2024/11/Romanian-Deadlift-1.jpg",
        ],
        "blocks": [
            {"category": "Squat", "sets_reps": "3 x 8-12", "options": ["Squat", "Smith Machine Squat", "Back Squat"]},
            {"category": "Quad Focus", "sets_reps": "3 x 10", "options": ["Leg Press", "Bulgarian Split Squat", "Walking Lunges"]},
            {"category": "Hamstrings", "sets_reps": "3 x 8-12", "options": ["Romanian Deadlift", "Barbell RDL", "Dumbbell RDL"]},
            {"category": "Isolation", "sets_reps": "3 x 10-12", "options": ["Leg Extension", "Glute Bridge", "Hip Thrust"]},
            {"category": "Curl", "sets_reps": "3 x 10-12", "options": ["Leg Curl", "Seated Leg Curl", "Lying Leg Curl"]},
            {"category": "Calves", "sets_reps": "4 x 12-15", "options": ["Standing Calf Raise", "Seated Calf Raise", "Calf Raises"]},
            {"category": "Workout Finisher Cardio", "sets_reps": "10-15 min", "options": ["Incline Walking", "Elliptical", "Cycling"]},
        ],
    },
    {
        "id": "cardio-core",
        "day_label": "Day 6",
        "title": "Cardio + Core",
        "subtitle": "Conditioning + trunk work",
        "accent": "secondary",
        "notes": ["Pick one option per block.", "Repeat the structure and gradually add time, reps, or intensity."],
        "images": [
            "https://static.nike.com/a/images/f_auto%2Ccs_srgb/w_1536%2Cc_limit/6a2dbeb8-e877-42c1-ae92-52e1ae29799f/3-treadmill-workouts-that-can-boost-your-fitness.jpg",
            "https://jsbhealthcare.co.in/cdn/shop/files/exercise-cycle-air-bike-for-home-jsb-hf175_16ab4842-55bf-484d-8bc9-8397ab1e116e.webp?v=1759901440",
            "https://www.realsimple.com/thmb/LAvXbxPdTZGe9chMDEbUmWV19ZQ%3D/1500x0/filters%3Ano_upscale%28%29%3Amax_bytes%28150000%29%3Astrip_icc%28%29/JumpRope_Infographic-100-7cbf0af757f04e108a0756f93c7d1fad.jpg",
            "https://hips.hearstapps.com/hmg-prod/images/skip-those-worries-away-royalty-free-image-1678894439.jpg?crop=0.669xw%3A1.00xh%3B0.0226xw%2C0&resize=640%3A%2A",
            "https://cdn.shopify.com/s/files/1/0316/7810/3691/files/jump_rope_routine_HIIT_exercise_f25afb37-ff2d-4512-82fb-e47935f7ac29.jpg?v=1611754826",
        ],
        "blocks": [
            {"category": "Cardio", "sets_reps": "Pick 1", "options": ["Treadmill Running", "Cycling", "Incline Walking"]},
            {"category": "HIIT", "sets_reps": "Pick 1", "options": ["Outdoor Run", "Jump Rope", "Stairmaster"]},
            {"category": "Core", "sets_reps": "3 rounds", "options": ["Plank", "Hanging Leg Raise", "Russian Twists"]},
        ],
    },
]


def get_workout_timetable(db: Session) -> dict:
    exercise_rows = list(db.scalars(select(ExerciseLibrary).order_by(ExerciseLibrary.name.asc())).all())
    exercise_by_name = {exercise.name: exercise for exercise in exercise_rows}

    timetable_days = []
    for day in TIMETABLE_CONFIG:
        blocks = []
        for block in day["blocks"]:
            options = []
            for option_name in block["options"]:
                exercise = exercise_by_name.get(option_name)
                if exercise is None:
                    continue
                options.append({"id": exercise.id, "name": exercise.name})
            blocks.append(
                {
                    "category": block["category"],
                    "sets_reps": block["sets_reps"],
                    "options": options,
                }
            )
        timetable_days.append(
            {
                "id": day["id"],
                "day_label": day["day_label"],
                "title": day["title"],
                "subtitle": day["subtitle"],
                "accent": day["accent"],
                "notes": day["notes"],
                "images": day["images"],
                "blocks": blocks,
            }
        )

    return {
        "weekly_split": WEEKLY_SPLIT,
        "timetable_days": timetable_days,
    }
