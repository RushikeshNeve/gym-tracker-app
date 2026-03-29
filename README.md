# 75 Hard Gym Tracker Pro

An upgraded Streamlit app that extends the original gym tracker into a full 75 Hard accountability and fat-loss system for workout consistency, hydration, diet adherence, recipes, calorie deficit tracking, progress photos, and weekly review.

## Features
- Today-first 75 Hard dashboard with required daily checklist
- Two-workout + outdoor workout rule tracking
- Profile-based BMR, TDEE, maintenance calorie, and target calorie calculation
- Weekly meal-plan templates with multiple daily meal options
- Recipe library with ingredients, steps, portions, and macro breakdown
- Calorie, protein, carbs, fats, and fiber tracking
- Energy balance tracking: food calories, exercise calories, net calories, deficit/surplus
- Diet compliance logging, whey quick-add, and spicy evening snack quick-adds
- Hydration tracker with quick-add buttons and weekly adherence
- Progress-photo metadata plus local file storage
- Upgraded body metrics with fat-loss focused measurements
- Weekly review summaries with reflections
- Preserved workout logger, PR logic, cardio tracker, progress analytics, and exercise library
- CSV import for legacy workout/body/cardio data plus CSV export for workouts, challenge days, nutrition, and hydration

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Project Structure
- `app.py`
- `db.py`
- `utils/__init__.py`
- `utils/challenge_logic.py`
- `utils/nutrition_logic.py`
- `utils/hydration_logic.py`
- `utils/weekly_review.py`
- `pages/0_Today.py`
- `pages/1_Dashboard.py`
- `pages/2_Log_Workout.py`
- `pages/3_Body_Metrics.py`
- `pages/4_Cardio.py`
- `pages/5_Progress.py`
- `pages/6_Exercise_Library.py`
- `pages/7_Nutrition.py`
- `pages/8_Hydration.py`
- `pages/9_Progress_Photos.py`
- `pages/10_Weekly_Review.py`

## Challenge Logic
- `challenge_start_date` is stored in `app_settings`
- On first run it defaults to tomorrow relative to the local machine date
- `challenge_day_number` is derived from that start date
- A day is `perfect` when all required 75 Hard tasks are complete:
  - workout 1
  - workout 2
  - one workout outdoors
  - followed diet
  - no cheat meals
  - no alcohol
  - water goal completed
  - progress picture taken
- A day is `incomplete` when it is today or in the future and still has missing required tasks
- A day is `failed` when it is in the past and still has missing required tasks
- The app does not hard reset the challenge; it marks status clearly and keeps the history

## Progress Photos
- Uploaded images are stored locally under `uploads/progress_photos/YYYY-MM-DD/`
- The database stores photo metadata and file paths in `progress_photos`
- If an image file is later missing, the app still keeps the metadata and warns gracefully

## Demo Data
The app seeds:
- existing workout, body metric, and cardio demo data
- a default challenge start date set to tomorrow
- sample challenge-day entries
- sample nutrition, hydration, profile, recipe, and exercise-burn logs
- sample progress-photo metadata

Seeding only happens when the relevant tables are empty.

## Notes
- Database file: `gym_tracker.db`
- Storage is local SQLite only
- Charts use Plotly
- Exercise library and YouTube demo enrichment remain available

## YouTube Exercise Demo Data
The app uses `seed_exercises.py` as the exercise source of truth and enriches exercises with:
- `youtube_url`
- `youtube_search_url`
- execution instructions
- common mistakes
- coaching tips

### Regenerate exercise video data
```bash
python scripts/enrich_exercises_with_youtube.py
```
