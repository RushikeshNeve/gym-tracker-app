import { useQuery } from "@tanstack/react-query";

import { api } from "@/lib/api/services";
import { queryKeys } from "@/lib/api/query-keys";
import { formatShortDate, formatWeekday, getTodayDateString } from "@/lib/date";
import type { DashboardSummary } from "@/types/dashboard";

function numberOrZero(value: number | null | undefined) {
  return typeof value === "number" ? value : 0;
}

export function useDashboardData() {
  return useQuery<DashboardSummary>({
    queryKey: queryKeys.dashboard(),
    queryFn: async () => {
      const [dashboard, today, bodyMetrics] = await Promise.all([
        api.dashboard.get(),
        api.today.get(),
        api.bodyMetrics.list(),
      ]);

      const firstMetric = bodyMetrics[bodyMetrics.length - 1];
      const latestMetric = bodyMetrics[0];
      const weightChange = firstMetric?.body_weight != null && latestMetric?.body_weight != null ? latestMetric.body_weight - firstMetric.body_weight : 0;
      const weightPoints = [...bodyMetrics]
        .reverse()
        .slice(-7)
        .map((item) => ({ label: formatWeekday(item.date), value: numberOrZero(item.body_weight) }));
      const waistPoints = [...bodyMetrics]
        .reverse()
        .slice(-7)
        .map((item) => ({ label: formatWeekday(item.date), value: numberOrZero(item.waist) }));

      return {
        heroLabel: "Weekly command center",
        heroTitle: "Dashboard",
        heroDescription: "A premium read on trend direction, compliance pressure, and whether the body is moving the way the plan says it should.",
        kpis: [
          { label: "Day X / 75", value: `${today.day_number} / 75`, detail: `${today.remaining_days} days remain in the challenge.`, tone: "primary" },
          { label: "Today completion", value: `${Math.round((today.total_completed / Math.max(today.required_total, 1)) * 100)}%`, detail: `${today.pending_tasks.length} tasks still open.`, tone: "secondary" },
          { label: "Current streak", value: `${dashboard.metrics.streak} days`, detail: "Perfect-day streak still alive.", tone: "primary" },
          { label: "Perfect days", value: `${dashboard.metrics.perfect_days}`, detail: "Full-compliance days banked so far." },
          { label: "Weight change", value: `${weightChange > 0 ? "+" : ""}${weightChange.toFixed(1)} kg`, detail: "Change since the earliest body entry.", tone: "secondary" },
          { label: "Calories today", value: `${Math.round(dashboard.energy.food_calories)}`, detail: "Food intake logged today." },
          { label: "Protein today", value: `${Math.round(dashboard.energy.protein)} g`, detail: "Protein logged so far.", tone: "primary" },
          { label: "Water today", value: `${(dashboard.hydration.total_ml / 1000).toFixed(1)} L`, detail: `${(dashboard.hydration.remaining_ml / 1000).toFixed(1)}L remaining.` },
          { label: "Workout completion", value: today.activity.workout_sessions >= 1 ? "Done" : "Pending", detail: `${today.activity.workout_sessions} training session${today.activity.workout_sessions === 1 ? "" : "s"} logged today.`, tone: today.activity.workout_sessions >= 1 ? "primary" : "warning" },
          { label: "Outdoor status", value: today.activity.outdoor_sessions >= 1 ? "Done" : "Pending", detail: "Challenge outdoor requirement status.", tone: today.activity.outdoor_sessions >= 1 ? "secondary" : "warning" },
        ],
        trends: {
          weight: {
            title: "Weight trend",
            description: "Seven-day bodyweight movement.",
            unit: "kg",
            accent: "primary",
            points: weightPoints.length ? weightPoints : [{ label: "No data", value: 0 }],
            summary: latestMetric?.body_weight != null ? `Latest bodyweight is ${latestMetric.body_weight.toFixed(1)} kg.` : "Log body metrics to unlock the weight trend.",
          },
          waist: {
            title: "Waist trend",
            description: "Waistline change across recent measurements.",
            unit: "cm",
            accent: "secondary",
            points: waistPoints.length ? waistPoints : [{ label: "No data", value: 0 }],
            summary: latestMetric?.waist != null ? `Latest waist measurement is ${latestMetric.waist.toFixed(1)} cm.` : "Log waist measurements to unlock this trend.",
          },
          calories: {
            title: "Calories trend",
            description: "Recent calorie intake against the target.",
            unit: "kcal",
            accent: "warning",
            points: dashboard.weekly_nutrition_chart.map((item) => ({ label: formatWeekday(item.date), value: item.calories })),
            summary: `Average intake is centered around ${Math.round(dashboard.challenge.weekly_summary.avg_calories)} kcal.`,
          },
          protein: {
            title: "Protein trend",
            description: "Recent protein intake consistency.",
            unit: "g",
            accent: "primary",
            points: dashboard.weekly_nutrition_chart.map((item) => ({ label: formatWeekday(item.date), value: item.protein })),
            summary: `Average protein is ${Math.round(dashboard.challenge.weekly_summary.avg_protein)} g.`,
          },
          hydration: {
            title: "Hydration trend",
            description: "Recent water adherence.",
            unit: "L",
            accent: "secondary",
            points: dashboard.weekly_hydration_chart.map((item) => ({ label: formatWeekday(item.date), value: Number((item.total_ml / 1000).toFixed(1)) })),
            summary: `Water adherence is averaging ${Math.round(dashboard.challenge.weekly_summary.water_adherence_pct)}%.`,
          },
          compliance: {
            title: "Compliance score",
            description: "Challenge execution trend across the week.",
            unit: "%",
            accent: "primary",
            points: dashboard.challenge.weekly_summary.challenge_chart.map((item) => ({
              label: formatWeekday(String(item.date)),
              value: Number(item.compliance_score ?? 0),
            })),
            summary: `Current day status is ${today.day_status.replaceAll("_", " ")}.`,
          },
        },
        workoutFrequencySummary: {
          totalSessions: dashboard.metrics.weekly_workouts,
          completedDays: [...new Set(dashboard.recent_activity.map((item) => formatWeekday(item.date)))],
          summary: `${dashboard.metrics.weekly_workouts} workout days and ${dashboard.metrics.weekly_prs} PRs have landed in the current window.`,
        },
        cardioMinutesSummary: {
          totalMinutes: dashboard.metrics.cardio_mins,
          averageMinutes: Math.round(dashboard.metrics.cardio_mins / 7),
          summary: `${dashboard.metrics.cardio_cals} calories burned through cardio this week.`,
        },
        recentPrs: dashboard.recent_prs.map((item, index) => ({
          id: `${index}-${item.date}`,
          exercise: item.exercise_name,
          value: `${item.weight} kg x ${item.reps}`,
          dateLabel: formatShortDate(item.date),
        })),
        weekSummary: [
          { label: "Perfect days", value: `${dashboard.challenge.weekly_summary.perfect_days}`, tone: "primary" },
          { label: "Incomplete days", value: `${dashboard.challenge.weekly_summary.incomplete_days}`, tone: "warning" },
          { label: "Workout days", value: `${dashboard.challenge.weekly_summary.workout_consistency}`, tone: "secondary" },
          { label: "Weekly score", value: `${dashboard.metrics.weekly_score}` },
        ],
        nextPlannedWorkout: {
          title: today.split_plan.today_plan,
          focus: `Tomorrow plan: ${today.split_plan.tomorrow_plan}`,
          time: getTodayDateString(),
          note: today.challenge_day.notes || "Use the current split plan to keep the next session low-friction and pre-decided.",
        },
      };
    },
  });
}
