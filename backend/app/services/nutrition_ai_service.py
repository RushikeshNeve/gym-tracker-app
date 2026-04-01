from __future__ import annotations

import json

from openai import OpenAI

from app.core.config import settings
from app.schemas.nutrition import NutritionMealAnalysisRequest, NutritionMealAnalysisResult


class NutritionAnalysisError(RuntimeError):
    pass


def analyze_meal_with_openai(payload: NutritionMealAnalysisRequest) -> NutritionMealAnalysisResult:
    if not settings.openai_api_key:
        raise NutritionAnalysisError("OpenAI API key is not configured on the backend.")

    client = OpenAI(api_key=settings.openai_api_key)
    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "meal_type": {"type": "string"},
            "food_name": {"type": "string"},
            "quantity": {"type": "string"},
            "calories": {"type": "number"},
            "protein": {"type": "number"},
            "carbs": {"type": "number"},
            "fats": {"type": "number"},
            "fiber": {"type": "number"},
            "notes": {"type": "string"},
            "assumptions": {
                "type": "array",
                "items": {"type": "string"},
            },
            "source_type": {"type": "string"},
        },
        "required": [
            "meal_type",
            "food_name",
            "quantity",
            "calories",
            "protein",
            "carbs",
            "fats",
            "fiber",
            "notes",
            "assumptions",
            "source_type",
        ],
    }
    prompt = (
        "Estimate calories and macros for the user's meal as accurately as possible. "
        "Use common Indian household portions when the user is vague. "
        "Return realistic calories, protein, carbs, fats, and fiber. "
        "Keep food_name short and human-readable. "
        "Put the important estimation assumptions in the assumptions array."
    )

    response = client.responses.create(
        model=settings.openai_nutrition_model,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": prompt,
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Meal type: {payload.meal_type}\nMeal description: {payload.meal_description}",
                    }
                ],
            },
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "nutrition_meal_analysis",
                "schema": schema,
                "strict": True,
            }
        },
    )

    output_text = getattr(response, "output_text", "")
    if not output_text:
        raise NutritionAnalysisError("OpenAI did not return nutrition analysis output.")

    try:
        parsed = json.loads(output_text)
    except json.JSONDecodeError as exc:
        raise NutritionAnalysisError("OpenAI returned invalid nutrition analysis JSON.") from exc

    parsed["meal_type"] = payload.meal_type
    return NutritionMealAnalysisResult.model_validate(parsed)
