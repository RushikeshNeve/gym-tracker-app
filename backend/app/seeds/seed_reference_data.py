from __future__ import annotations

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.diet_plan_templates import DietPlanTemplate
from app.models.exercise_library import ExerciseLibrary
from app.models.recipe_library import RecipeLibrary
from app.seeds.source_loader import load_seed_sources


def main() -> None:
    seed_exercises, seed_nutrition = load_seed_sources()
    with SessionLocal() as db:
        seen_exercise_names: set[str] = set()
        for item in seed_exercises.EXERCISES:
            name = item["name"]
            if name in seen_exercise_names:
                continue
            seen_exercise_names.add(name)
            exists = db.scalar(select(ExerciseLibrary).where(ExerciseLibrary.name == name))
            if not exists:
                db.add(
                    ExerciseLibrary(
                        name=name,
                        day_type=item["day_type"],
                        muscle_group=item["muscle_group"],
                        youtube_url="",
                        youtube_search_url=f"https://www.youtube.com/results?search_query={name.replace(' ', '+')}+form",
                        instructions_json=[],
                        common_mistakes_json=[],
                        tips="",
                        matched=False,
                    )
                )

        for item in seed_nutrition.RECIPE_LIBRARY:
            exists = db.scalar(select(RecipeLibrary).where(RecipeLibrary.recipe_name == item["recipe_name"]))
            if not exists:
                db.add(
                    RecipeLibrary(
                        recipe_name=item["recipe_name"],
                        meal_type=item["meal_type"],
                        ingredients_json=item["ingredients_json"] if isinstance(item["ingredients_json"], list) else __import__("json").loads(item["ingredients_json"]),
                        steps_json=item["steps_json"] if isinstance(item["steps_json"], list) else __import__("json").loads(item["steps_json"]),
                        calories=item["calories"],
                        protein=item["protein"],
                        carbs=item["carbs"],
                        fats=item["fats"],
                        fiber=item["fiber"],
                        portion_note=item["portion_note"],
                        is_spicy=bool(item["is_spicy"]),
                        is_vegetarian=bool(item["is_vegetarian"]),
                        is_egg_based=bool(item["is_egg_based"]),
                        is_soya_based=bool(item["is_soya_based"]),
                    )
                )

        for row in seed_nutrition.DIET_PLAN_TEMPLATES:
            exists = db.scalar(
                select(DietPlanTemplate).where(
                    DietPlanTemplate.day_name == row[0],
                    DietPlanTemplate.meal_type == row[1],
                )
            )
            if not exists:
                db.add(
                    DietPlanTemplate(
                        day_name=row[0],
                        meal_type=row[1],
                        option_1=row[2],
                        option_2=row[3],
                        option_3=row[4],
                        option_4=row[5],
                        notes=row[6],
                    )
                )

        db.commit()
        print("Reference data seeded.")


if __name__ == "__main__":
    main()
