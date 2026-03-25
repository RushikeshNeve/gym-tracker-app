# Gym Tracker Pro (Streamlit)

A production-style, mobile-friendly fitness tracking app inspired by a Google Sheet workflow.

## Features
- Dashboard with KPI cards, weekly score, trends, PR feed, and recommended workout
- Fast workout logger (one row per exercise entry) with automatic PR logic
- Enriched exercise library sourced from free-exercise-db while preserving your custom exercise names
- Body metrics logging + transformation trends
- Cardio logging + weekly adherence and calorie summaries
- Progress analytics with filters (date/day/muscle/exercise)
- Fat-loss features: target weight, goal progress, waist/bodyweight trends
- CSV import utility for exported Google Sheet data
- CSV export for workout logs
- SQLite storage with seeded demo data

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Exercise enrichment (free-exercise-db)
Run the enrichment script to map your custom exercise list to free-exercise-db metadata and preview images:

```bash
python scripts/enrich_exercises.py
```

This command generates/updates:
- `data/free_exercise_db.json` (cache)
- `data/enriched_exercises.json`
- `data/unmatched_exercises.json`
- `data/match_report.csv`

To regenerate from scratch, delete the files above and rerun:

```bash
python scripts/enrich_exercises.py
```

Then launch the app:

```bash
streamlit run app.py
```

## Project Structure
- `app.py`
- `db.py`
- `seed_exercises.py`
- `scripts/enrich_exercises.py`
- `components/exercise_preview.py`
- `utils/ui_helpers.py`
- `utils/exercise_data.py`
- `pages/1_Dashboard.py`
- `pages/2_Log_Workout.py`
- `pages/3_Body_Metrics.py`
- `pages/4_Cardio.py`
- `pages/5_Progress.py`
- `pages/6_Exercise_Library.py`

## Notes
- Database file is `gym_tracker.db` (auto-created)
- On first run, exercises and sample data are seeded
- PR logic:
  - first log of an exercise => `First`
  - higher weight than prior best => `PR`
  - same max weight with higher reps => `PR`
