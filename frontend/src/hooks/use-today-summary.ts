import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { api } from "@/lib/api/services";
import { queryKeys } from "@/lib/api/query-keys";
import { getTodayDateString } from "@/lib/date";
import type { ChallengeDayUpsertRequest, TodayResponse } from "@/types/api";
import type { TodaySummary, TodayTask } from "@/types/today";

function taskFromChallenge(today: TodayResponse): TodayTask[] {
  const challenge = today.challenge_day;
  return [
    {
      id: "workout-1",
      title: "Workout 1",
      description: "Primary session must be completed cleanly.",
      category: "Training",
      status: challenge.workout_1_completed ? "completed" : "pending",
      accent: "primary",
      interaction: "navigate",
      actionLabel: "Open workout log",
      navigateTo: "/workouts",
      field: "workout_1_completed",
    },
    {
      id: "outdoor-workout",
      title: "Outdoor workout",
      description: "At least one session must happen outside.",
      category: "Challenge",
      status: challenge.one_workout_outdoors ? "completed" : "pending",
      accent: "secondary",
      interaction: "navigate",
      actionLabel: "Open cardio",
      navigateTo: "/cardio",
      field: "one_workout_outdoors",
    },
    {
      id: "followed-diet",
      title: "Followed diet",
      description: "Meals stayed aligned with the plan for the day.",
      category: "Nutrition",
      status: challenge.followed_diet ? "completed" : "pending",
      accent: "primary",
      interaction: "toggle",
      pendingActionLabel: "Mark diet followed",
      completedActionLabel: "Mark diet not followed",
      field: "followed_diet",
    },
    {
      id: "no-cheat-meal",
      title: "No cheat meal",
      description: "Zero off-plan meals and no hidden leaks.",
      category: "Nutrition",
      status: challenge.no_cheat_meals ? "completed" : "pending",
      accent: "primary",
      interaction: "toggle",
      pendingActionLabel: "Mark no cheat meal",
      completedActionLabel: "Mark cheat meal happened",
      field: "no_cheat_meals",
    },
    {
      id: "water-goal",
      title: "Water goal",
      description: `${(today.activity.water_target_ml - today.activity.water_total_ml) / 1000 > 0 ? ((today.activity.water_target_ml - today.activity.water_total_ml) / 1000).toFixed(1) : "0.0"}L still left before shutdown.`,
      category: "Hydration",
      status: challenge.water_goal_completed ? "completed" : "pending",
      accent: "secondary",
      interaction: "navigate",
      actionLabel: "Open hydration",
      navigateTo: "/hydration",
      field: "water_goal_completed",
    },
    {
      id: "progress-photo",
      title: "Progress photo",
      description: "Capture the daily proof shot before the day closes.",
      category: "Accountability",
      status: challenge.progress_picture_taken ? "completed" : "pending",
      accent: "primary",
      interaction: "navigate",
      actionLabel: "Open progress photos",
      navigateTo: "/progress-photos",
      field: "progress_picture_taken",
    },
  ];
}

function mapTodayResponse(today: TodayResponse): TodaySummary {
  const tasks = taskFromChallenge(today);
  const completedCount = tasks.filter((task) => task.status === "completed").length;
  return {
    dayNumber: today.day_number,
    totalDays: 75,
    completionPercentage: Math.round((today.total_completed / Math.max(today.required_total, 1)) * 100),
    currentStreak: today.current_streak,
    perfectDays: today.perfect_days,
    failedDays: today.failed_days,
    completedCount,
    pendingCount: tasks.length - completedCount,
    heroCopy:
      today.day_status === "perfect"
        ? "The day is fully locked. Keep the same discipline tomorrow."
        : "The day is still writable. Protect the remaining tasks and close it clean.",
    quickActions: ["Log workout", "Add water", "Open nutrition"],
    notes: today.challenge_day.notes || "Keep the note tactical. Protect the remaining tasks before the day closes.",
    focusLabel: today.day_status.replaceAll("_", " "),
    splitLabel: today.split_plan.today_plan,
    hydrationLiters: today.activity.water_total_ml / 1000,
    hydrationTargetLiters: today.activity.water_target_ml / 1000,
    calories: today.energy_balance.food_calories,
    caloriesTarget: today.energy_balance.target_calories,
    protein: today.energy_balance.protein,
    complianceScore: today.compliance_score,
    totalSessions: today.activity.total_sessions,
    workoutSessions: today.activity.workout_sessions,
    cardioSessions: today.activity.cardio_sessions,
    outdoorSessions: today.activity.outdoor_sessions,
    photoCount: today.challenge_day.progress_picture_taken ? 1 : 0,
    pendingTasks: today.pending_tasks,
    dayStatus: today.day_status,
    tasks,
  };
}

export function useTodaySummary() {
  const todayDate = getTodayDateString();
  return useQuery<TodaySummary>({
    queryKey: queryKeys.today(todayDate),
    queryFn: async () => mapTodayResponse(await api.today.get()),
  });
}

export function useUpdateTodayNote() {
  const queryClient = useQueryClient();
  const todayDate = getTodayDateString();

  return useMutation({
    mutationFn: async (notes: string) => {
      const current = await api.today.get();
      const payload: ChallengeDayUpsertRequest = {
        ...current.challenge_day,
        date: current.date,
        notes,
      };
      return api.today.update(todayDate, payload);
    },
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: queryKeys.today(todayDate) });
      void queryClient.invalidateQueries({ queryKey: queryKeys.dashboard() });
    },
  });
}

export function useUpdateTodayTask() {
  const queryClient = useQueryClient();
  const todayDate = getTodayDateString();

  return useMutation({
    mutationFn: async ({
      field,
      value,
    }: {
      field:
        | "workout_1_completed"
        | "one_workout_outdoors"
        | "followed_diet"
        | "no_cheat_meals"
        | "water_goal_completed"
        | "progress_picture_taken";
      value: boolean;
    }) => {
      const current = await api.today.get();
      const payload: ChallengeDayUpsertRequest = {
        ...current.challenge_day,
        date: current.date,
        [field]: value,
      };
      if (field === "followed_diet") {
        payload.diet_followed = value;
      }
      if (field === "no_cheat_meals") {
        payload.cheat_meal = !value;
      }
      await api.today.update(todayDate, payload);
      return mapTodayResponse(await api.today.get());
    },
    onSuccess: (nextToday) => {
      queryClient.setQueryData(queryKeys.today(todayDate), nextToday);
      void queryClient.refetchQueries({ queryKey: queryKeys.today(todayDate) });
      void queryClient.refetchQueries({ queryKey: queryKeys.dashboard() });
      void queryClient.refetchQueries({ queryKey: ["nutrition-page", todayDate] });
    },
  });
}
