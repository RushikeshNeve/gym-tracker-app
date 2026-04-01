from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field

from app.schemas.common import ChartPoint, TimestampFields
from app.schemas.targets import DailyTargetRead


class NutritionLogBase(BaseModel):
    date: date
    meal_type: str
    food_name: str
    quantity: str = ""
    serving_count: float = Field(default=1.0, ge=0.1)
    calories: float = Field(default=0, ge=0)
    protein: float = Field(default=0, ge=0)
    carbs: float = Field(default=0, ge=0)
    fats: float = Field(default=0, ge=0)
    fiber: float = Field(default=0, ge=0)
    notes: str = ""
    source_type: str = "manual"
    recipe_name: str = ""


class NutritionLogCreate(NutritionLogBase):
    pass


class NutritionLogUpdate(BaseModel):
    meal_type: str | None = None
    food_name: str | None = None
    quantity: str | None = None
    serving_count: float | None = Field(default=None, ge=0.1)
    calories: float | None = Field(default=None, ge=0)
    protein: float | None = Field(default=None, ge=0)
    carbs: float | None = Field(default=None, ge=0)
    fats: float | None = Field(default=None, ge=0)
    fiber: float | None = Field(default=None, ge=0)
    notes: str | None = None
    source_type: str | None = None
    recipe_name: str | None = None


class NutritionLogRead(NutritionLogBase, TimestampFields):
    id: int
    profile_id: int


class NutritionMealAnalysisRequest(BaseModel):
    meal_type: str
    meal_description: str = Field(min_length=3)


class NutritionMealAnalysisResult(BaseModel):
    meal_type: str
    food_name: str
    quantity: str
    calories: float = Field(ge=0)
    protein: float = Field(ge=0)
    carbs: float = Field(ge=0)
    fats: float = Field(ge=0)
    fiber: float = Field(ge=0)
    notes: str = ""
    assumptions: list[str] = Field(default_factory=list)
    source_type: str = "ai_estimated"


class NutritionTotals(BaseModel):
    calories: float
    protein: float
    carbs: float
    fats: float
    fiber: float


class NutritionDailySummary(BaseModel):
    date: date
    totals: NutritionTotals
    remaining: NutritionTotals
    targets: DailyTargetRead
    meals: list[NutritionLogRead]
    compliance_inputs: dict[str, bool]


class WeeklyNutritionSummary(BaseModel):
    avg_calories: float
    avg_protein: float
    chart: list[ChartPoint]
