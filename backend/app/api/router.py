from fastapi import APIRouter

from app.api.routes import (
    body_metrics,
    cardio,
    dashboard,
    exercises,
    health,
    hydration,
    meal_plans,
    nutrition,
    profile,
    progress_photos,
    recipes,
    today,
    weekly_review,
    workout_timetable,
    workouts,
)


api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(profile.router)
api_router.include_router(today.router)
api_router.include_router(dashboard.router)
api_router.include_router(workout_timetable.router)
api_router.include_router(workouts.router)
api_router.include_router(cardio.router)
api_router.include_router(body_metrics.router)
api_router.include_router(nutrition.router)
api_router.include_router(hydration.router)
api_router.include_router(recipes.router)
api_router.include_router(meal_plans.router)
api_router.include_router(progress_photos.router)
api_router.include_router(exercises.router)
api_router.include_router(weekly_review.router)
