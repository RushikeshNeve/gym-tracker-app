import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { api } from "@/lib/api/services";
import { formatShortDate, formatWeekday } from "@/lib/date";
import { queryKeys } from "@/lib/api/query-keys";
import type { CardioLogCreateRequest } from "@/types/api";
import type { CardioPageData } from "@/types/tracker-pages";

export function useCardioPage() {
  return useQuery<CardioPageData>({
    queryKey: queryKeys.cardio(),
    queryFn: async () => {
      const cardio = await api.cardio.list();
      const recent = [...cardio].sort((a, b) => a.date.localeCompare(b.date)).slice(-7);
      const totalMinutes = cardio.reduce((sum, item) => sum + item.duration_min, 0);
      const totalCalories = cardio.reduce((sum, item) => sum + (item.calories ?? item.estimated_calories_burned), 0);
      return {
        sessionPresets: [
          { label: "Outdoor incline walk", note: "The simplest low-friction 75 Hard cardio session." },
          { label: "Zone 2 treadmill", note: "Reliable indoor fallback when weather or schedule gets messy." },
          { label: "Cycle intervals", note: "Shorter higher-output conditioning when recovery allows." },
        ],
        weeklySummary: [
          { label: "Total minutes", value: `${totalMinutes}`, note: "Minutes logged across available cardio entries." },
          { label: "Outdoor sessions", value: `${cardio.filter((item) => item.is_outdoor).length}`, note: "Outdoor cardio and workout entries keep compliance alive." },
          { label: "Calories burned", value: `${Math.round(totalCalories)}`, note: "Estimated cardio energy burn from the backend logs." },
        ],
        history: cardio.map((item) => ({
          id: String(item.id),
          type: item.cardio_type,
          duration: `${item.duration_min} min`,
          calories: `${Math.round(item.calories ?? item.estimated_calories_burned)} kcal`,
          distance: `${item.distance_km.toFixed(1)} km`,
          pace: item.pace_text || "N/A",
          outdoor: item.is_outdoor,
          dateLabel: formatShortDate(item.date),
        })),
        trend: {
          title: "Weekly cardio trend",
          description: "Recent cardio minutes pulled from the backend history.",
          unit: "min",
          accent: "secondary",
          summary: `${cardio.length} cardio sessions are currently logged.`,
          points: recent.map((item) => ({ label: formatWeekday(item.date), value: item.duration_min })),
        },
      };
    },
  });
}

export function useCreateCardioLog() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (payload: CardioLogCreateRequest) => api.cardio.create(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: queryKeys.cardio() });
      void queryClient.invalidateQueries({ queryKey: queryKeys.today(new Date().toISOString().slice(0, 10)) });
      void queryClient.invalidateQueries({ queryKey: queryKeys.dashboard() });
    },
  });
}

export function useDeleteCardioLog() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: number) => api.cardio.delete(id),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: queryKeys.cardio() });
      void queryClient.invalidateQueries({ queryKey: queryKeys.dashboard() });
    },
  });
}
