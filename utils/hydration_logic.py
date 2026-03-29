"""Hydration calculations for daily and weekly progress."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

import pandas as pd

from db import fetch_df, get_daily_targets


def get_daily_hydration(log_date: str) -> dict[str, Any]:
    logs = fetch_df("SELECT * FROM hydration_logs WHERE date = ? ORDER BY id DESC", (log_date,))
    targets = get_daily_targets(log_date)
    total_ml = int(logs["amount_ml"].sum()) if not logs.empty else 0
    target_ml = int(float(targets["water_target_liters"] or 0) * 1000)
    return {
        "logs": logs,
        "target_liters": float(targets["water_target_liters"] or 0),
        "target_ml": target_ml,
        "total_ml": total_ml,
        "remaining_ml": max(0, target_ml - total_ml),
        "bottle_count": round(total_ml / 500, 1) if total_ml else 0,
        "progress_pct": min(100, round((total_ml / target_ml) * 100, 1)) if target_ml else 0,
    }


def get_weekly_hydration(end_date: date | None = None) -> pd.DataFrame:
    end = end_date or date.today()
    start = end - timedelta(days=6)
    logs = fetch_df(
        "SELECT date, SUM(amount_ml) AS total_ml FROM hydration_logs WHERE date BETWEEN ? AND ? GROUP BY date ORDER BY date",
        (start.isoformat(), end.isoformat()),
    )
    if logs.empty:
        return logs
    logs["date"] = pd.to_datetime(logs["date"])
    targets = []
    for day_value in logs["date"].dt.date:
        targets.append(int(float(get_daily_targets(day_value.isoformat())["water_target_liters"]) * 1000))
    logs["target_ml"] = targets
    logs["adherence_pct"] = (logs["total_ml"] / logs["target_ml"]).clip(upper=1).fillna(0) * 100
    return logs
