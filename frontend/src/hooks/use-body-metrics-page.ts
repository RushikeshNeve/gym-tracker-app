import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { api } from "@/lib/api/services";
import { queryKeys } from "@/lib/api/query-keys";
import { formatWeekday } from "@/lib/date";
import type { BodyMetricCreateRequest, BodyMetricUpdateRequest } from "@/types/api";
import type { BodyMetricsPageData } from "@/types/tracker-pages";

function changeString(current: number | null, first: number | null, suffix: string) {
  if (current == null || first == null) return `0${suffix}`;
  const diff = current - first;
  return `${diff > 0 ? "+" : ""}${diff.toFixed(1)}${suffix}`;
}

function buildBodyMetricsPageData(metrics: Awaited<ReturnType<typeof api.bodyMetrics.list>>): BodyMetricsPageData {
  const ordered = [...metrics].sort((a, b) => a.date.localeCompare(b.date));
  const first = ordered[0];
  const latest = ordered[ordered.length - 1];
  const recent = ordered.slice(-7);

  return {
    currentStats: [
      { label: "Weight", dayOne: `${first?.body_weight ?? 0} kg`, current: `${latest?.body_weight ?? 0} kg`, change: changeString(latest?.body_weight ?? null, first?.body_weight ?? null, " kg"), tone: "primary" },
      { label: "Waist", dayOne: `${first?.waist ?? 0} cm`, current: `${latest?.waist ?? 0} cm`, change: changeString(latest?.waist ?? null, first?.waist ?? null, " cm"), tone: "primary" },
      { label: "Hips", dayOne: `${first?.hips ?? 0} cm`, current: `${latest?.hips ?? 0} cm`, change: changeString(latest?.hips ?? null, first?.hips ?? null, " cm") },
      { label: "Chest", dayOne: `${first?.chest ?? 0} cm`, current: `${latest?.chest ?? 0} cm`, change: changeString(latest?.chest ?? null, first?.chest ?? null, " cm") },
      { label: "Arms", dayOne: `${first?.arms ?? 0} cm`, current: `${latest?.arms ?? 0} cm`, change: changeString(latest?.arms ?? null, first?.arms ?? null, " cm") },
      { label: "Thighs", dayOne: `${first?.thighs ?? first?.thigh ?? 0} cm`, current: `${latest?.thighs ?? latest?.thigh ?? 0} cm`, change: changeString((latest?.thighs ?? latest?.thigh) ?? null, (first?.thighs ?? first?.thigh) ?? null, " cm") },
      { label: "Neck", dayOne: `${first?.neck ?? 0} cm`, current: `${latest?.neck ?? 0} cm`, change: changeString(latest?.neck ?? null, first?.neck ?? null, " cm") },
      { label: "Body fat", dayOne: `${first?.body_fat_percent ?? 0}%`, current: `${latest?.body_fat_percent ?? 0}%`, change: changeString(latest?.body_fat_percent ?? null, first?.body_fat_percent ?? null, "%"), tone: "secondary" },
    ],
    weeklyChanges: [
      { label: "Weight this week", value: changeString(latest?.body_weight ?? null, recent[0]?.body_weight ?? null, " kg"), note: "Latest seven-entry weight drift." },
      { label: "Waist this week", value: changeString(latest?.waist ?? null, recent[0]?.waist ?? null, " cm"), note: "Most visible cut marker this week." },
      { label: "Body fat trend", value: changeString(latest?.body_fat_percent ?? null, recent[0]?.body_fat_percent ?? null, "%"), note: "Estimated body-fat movement from recent entries." },
    ],
    milestones: [
      { id: "1", title: "Latest bodyweight", status: latest?.body_weight != null ? "Logged" : "Pending", note: latest?.progress_notes || "Add notes to unlock richer milestone context." },
      { id: "2", title: "Latest waist", status: latest?.waist != null ? "Logged" : "Pending", note: latest?.notes || "Track waist for a stronger physique read." },
      { id: "3", title: "Recent trend depth", status: recent.length >= 3 ? "Healthy" : "Shallow", note: "More repeated entries improve the quality of trend cards." },
    ],
    trends: [
      {
        title: "Weight trend",
        description: "Bodyweight trend from the latest recorded entries.",
        unit: "kg",
        accent: "primary",
        summary: latest?.body_weight != null ? `Latest entry is ${latest.body_weight} kg.` : "Add bodyweight entries to unlock the trend.",
        points: recent.map((entry) => ({ label: formatWeekday(entry.date), value: entry.body_weight ?? 0 })),
      },
      {
        title: "Waist trend",
        description: "Waist measurements across the latest recorded entries.",
        unit: "cm",
        accent: "secondary",
        summary: latest?.waist != null ? `Latest waist entry is ${latest.waist} cm.` : "Add waist entries to unlock the trend.",
        points: recent.map((entry) => ({ label: formatWeekday(entry.date), value: entry.waist ?? 0 })),
      },
    ],
    entries: [...metrics].map((entry) => ({
      id: entry.id,
      date: entry.date,
      bodyWeight: entry.body_weight,
      waist: entry.waist,
      hips: entry.hips,
      chest: entry.chest,
      arms: entry.arms,
      thighs: entry.thighs ?? entry.thigh,
      neck: entry.neck,
      bodyFat: entry.body_fat_percent,
      notes: entry.notes,
      progressNotes: entry.progress_notes,
    })),
  };
}

export function useBodyMetricsPage() {
  return useQuery<BodyMetricsPageData>({
    queryKey: queryKeys.bodyMetrics(),
    queryFn: async () => {
      const metrics = await api.bodyMetrics.list();
      return buildBodyMetricsPageData(metrics);
    },
  });
}

export function useCreateBodyMetric() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (payload: BodyMetricCreateRequest) => api.bodyMetrics.create(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: queryKeys.bodyMetrics() });
      void queryClient.invalidateQueries({ queryKey: queryKeys.dashboard() });
    },
  });
}

export function useUpdateBodyMetric() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, payload }: { id: number; payload: BodyMetricUpdateRequest }) => api.bodyMetrics.update(id, payload),
    onSuccess: (updatedMetric) => {
      queryClient.setQueryData<BodyMetricsPageData>(queryKeys.bodyMetrics(), (current) => {
        if (!current) return current;
        return {
          ...current,
          entries: current.entries.map((entry) =>
            entry.id === updatedMetric.id
              ? {
                  id: updatedMetric.id,
                  date: updatedMetric.date,
                  bodyWeight: updatedMetric.body_weight,
                  waist: updatedMetric.waist,
                  hips: updatedMetric.hips,
                  chest: updatedMetric.chest,
                  arms: updatedMetric.arms,
                  thighs: updatedMetric.thighs ?? updatedMetric.thigh,
                  neck: updatedMetric.neck,
                  bodyFat: updatedMetric.body_fat_percent,
                  notes: updatedMetric.notes,
                  progressNotes: updatedMetric.progress_notes,
                }
              : entry,
          ),
        };
      });
      void queryClient.invalidateQueries({ queryKey: queryKeys.bodyMetrics() });
      void queryClient.invalidateQueries({ queryKey: queryKeys.dashboard() });
    },
  });
}

export function useDeleteBodyMetric() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: number) => api.bodyMetrics.delete(id),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: queryKeys.bodyMetrics() });
      void queryClient.invalidateQueries({ queryKey: queryKeys.dashboard() });
    },
  });
}
