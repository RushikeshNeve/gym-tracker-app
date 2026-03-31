import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { api } from "@/lib/api/services";
import { queryKeys } from "@/lib/api/query-keys";
import { formatWeekday, getWeekStartString } from "@/lib/date";
import type { WeeklyReviewUpsertRequest } from "@/types/api";
import type { WeeklyReviewPageData } from "@/types/tracker-pages";

function splitNotes(value: string, fallback: string[]) {
  const lines = value
    .split(/\n+/)
    .map((item) => item.trim())
    .filter(Boolean);
  return lines.length ? lines : fallback;
}

export function useWeeklyReviewPage() {
  const weekStart = getWeekStartString();
  return useQuery<WeeklyReviewPageData>({
    queryKey: ["weekly-review-page", weekStart],
    queryFn: async () => {
      const [summary, record] = await Promise.all([api.weeklyReview.summary(weekStart), api.weeklyReview.record(weekStart)]);
      return {
        weeklyScore: `${Math.round((summary.perfect_days * 14 + summary.workout_consistency * 6 + summary.prs * 4 + summary.water_adherence_pct * 0.2))} / 100`,
        summaryCards: [
          { label: "Perfect days", value: `${summary.perfect_days}`, note: "Days closed with full compliance." },
          { label: "Incomplete days", value: `${summary.incomplete_days}`, note: "Days that leaked but did not fail completely." },
          { label: "Failed days", value: `${summary.failed_days}`, note: "Total breakdown days in the current week." },
          { label: "Average calories", value: `${Math.round(summary.avg_calories)}`, note: "Average daily intake this week." },
          { label: "Average protein", value: `${Math.round(summary.avg_protein)} g`, note: "Average daily protein this week." },
          { label: "Workout consistency", value: `${summary.workout_consistency}`, note: "Distinct workout days this week." },
          { label: "Cardio adherence", value: `${summary.cardio_minutes} min`, note: "Total cardio minutes from the weekly summary." },
          { label: "Hydration adherence", value: `${Math.round(summary.water_adherence_pct)}%`, note: "Average hydration adherence this week." },
        ],
        bodyChanges: [
          { label: "Weight", value: `${summary.weight_change > 0 ? "+" : ""}${summary.weight_change} kg`, note: "Net weekly weight movement." },
          { label: "Waist", value: `${summary.waist_change > 0 ? "+" : ""}${summary.waist_change} cm`, note: "Net weekly waist movement." },
          { label: "Week range", value: `${formatWeekday(summary.week_start)} - ${formatWeekday(summary.week_end)}`, note: "Current review window." },
        ],
        reflection: {
          wins: splitNotes(record?.what_went_well ?? "", ["Use the review form below to save weekly wins from the backend."]),
          misses: splitNotes(record?.what_was_difficult ?? "", ["Use the review form below to record what got difficult this week."]),
          nextWeekFocus: splitNotes(record?.focus_for_next_week ?? "", ["Use the review form below to save next-week focus points."]),
          note: record?.notes || "No weekly reflection note has been saved yet.",
        },
      };
    },
  });
}

export function useUpsertWeeklyReview() {
  const queryClient = useQueryClient();
  const weekStart = getWeekStartString();
  return useMutation({
    mutationFn: async (payload: WeeklyReviewUpsertRequest) => api.weeklyReview.upsert(weekStart, payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["weekly-review-page", weekStart] });
      void queryClient.invalidateQueries({ queryKey: queryKeys.weeklyReviewSummary(weekStart) });
      void queryClient.invalidateQueries({ queryKey: queryKeys.weeklyReviewRecord(weekStart) });
      void queryClient.invalidateQueries({ queryKey: queryKeys.dashboard() });
    },
  });
}
