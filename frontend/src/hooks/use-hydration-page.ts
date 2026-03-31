import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { api } from "@/lib/api/services";
import { queryKeys } from "@/lib/api/query-keys";
import { formatWeekday, getTodayDateString } from "@/lib/date";
import type { HydrationDailySummaryResponse } from "@/types/api";
import type { TaskStatus, TodaySummary } from "@/types/today";
import type { HydrationPageData } from "@/types/tracker-pages";

function mapHydrationPage(daily: HydrationDailySummaryResponse, weekly: Awaited<ReturnType<typeof api.hydration.weekly>>): HydrationPageData {
  return {
    targetMl: daily.target_ml,
    consumedMl: daily.total_ml,
    remainingMl: daily.remaining_ml,
    quickAdds: [250, 500, 1000],
    history: daily.logs.map((log) => ({
      id: String(log.id),
      time: new Date(log.created_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      amountMl: log.amount_ml,
      note: "Hydration log",
    })),
    weeklyTrend: {
      title: "Weekly hydration",
      description: "Seven-day water adherence against the daily target.",
      unit: "L",
      accent: "secondary",
      summary: `Current hydration progress is ${Math.round(daily.progress_pct)}% for today.`,
      points: weekly.map((point) => ({ label: formatWeekday(point.date), value: Number((point.total_ml / 1000).toFixed(1)) })),
    },
  };
}

export function useHydrationPage() {
  const todayDate = getTodayDateString();
  return useQuery<HydrationPageData>({
    queryKey: ["hydration-page", todayDate],
    queryFn: async () => {
      const [daily, weekly] = await Promise.all([api.hydration.daily(todayDate), api.hydration.weekly(todayDate)]);
      return mapHydrationPage(daily, weekly);
    },
  });
}

export function useAddHydrationLog() {
  const queryClient = useQueryClient();
  const todayDate = getTodayDateString();

  return useMutation({
    mutationFn: async (amountMl: number) =>
      api.hydration.create({
        date: todayDate,
        amount_ml: amountMl,
      }),
    onMutate: async (amountMl) => {
      const pageKey = ["hydration-page", todayDate] as const;
      await queryClient.cancelQueries({ queryKey: pageKey });
      const previous = queryClient.getQueryData<HydrationPageData>(pageKey);
      if (previous) {
        queryClient.setQueryData<HydrationPageData>(pageKey, {
          ...previous,
          consumedMl: previous.consumedMl + amountMl,
          remainingMl: Math.max(0, previous.remainingMl - amountMl),
          history: [
            {
              id: `optimistic-${Date.now()}`,
              time: "Now",
              amountMl,
              note: "Hydration log",
            },
            ...previous.history,
          ],
        });
      }
      const todayKey = queryKeys.today(todayDate);
      const previousToday = queryClient.getQueryData<TodaySummary>(todayKey);
      if (previousToday) {
        const nextHydrationLiters = previousToday.hydrationLiters + amountMl / 1000;
        const waterComplete = nextHydrationLiters >= previousToday.hydrationTargetLiters;
        const nextStatus: TaskStatus = waterComplete ? "completed" : "pending";
        const nextTasks = previousToday.tasks.map((task) =>
          task.id === "water-goal"
            ? {
                ...task,
                status: nextStatus,
                description: `${Math.max(previousToday.hydrationTargetLiters - nextHydrationLiters, 0).toFixed(1)}L still left before shutdown.`,
              }
            : task,
        );
        const completedCount = nextTasks.filter((task) => task.status === "completed").length;
        queryClient.setQueryData<TodaySummary>(todayKey, {
          ...previousToday,
          hydrationLiters: nextHydrationLiters,
          completedCount,
          pendingCount: nextTasks.length - completedCount,
          completionPercentage: Math.round((completedCount / Math.max(nextTasks.length, 1)) * 100),
          tasks: nextTasks,
        });
      }
      return { previous, pageKey, previousToday, todayKey };
    },
    onError: (_error, _amountMl, context) => {
      if (context?.previous) {
        queryClient.setQueryData(context.pageKey, context.previous);
      }
      if (context?.previousToday) {
        queryClient.setQueryData(context.todayKey, context.previousToday);
      }
    },
    onSettled: () => {
      void queryClient.invalidateQueries({ queryKey: ["hydration-page", todayDate] });
      void queryClient.invalidateQueries({ queryKey: queryKeys.hydrationDaily(todayDate) });
      void queryClient.invalidateQueries({ queryKey: queryKeys.hydrationWeekly(todayDate) });
      void queryClient.refetchQueries({ queryKey: queryKeys.today(todayDate) });
      void queryClient.refetchQueries({ queryKey: queryKeys.dashboard() });
    },
  });
}
