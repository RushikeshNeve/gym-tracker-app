import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { api } from "@/lib/api/services";
import { queryKeys } from "@/lib/api/query-keys";
import { getTodayDateString } from "@/lib/date";
import type { WorkoutCreateRequest } from "@/types/api";
import type { WorkoutPageData } from "@/types/tracker-pages";

export function useWorkoutPage(selectedExerciseName?: string) {
  return useQuery<WorkoutPageData>({
    queryKey: ["workout-page", selectedExerciseName ?? ""],
    queryFn: async () => {
      const [workouts, exercises] = await Promise.all([api.workouts.list(), api.exercises.list()]);
      const latestWorkout = workouts[0];
      const sortedExerciseNames = [...new Set(exercises.map((item) => item.name))].sort((left, right) => left.localeCompare(right));
      const exerciseName = selectedExerciseName || latestWorkout?.exercises[0]?.exercise_name || sortedExerciseNames[0] || "Exercise";
      const [history] = await Promise.all([api.workouts.history(exerciseName)]);
      const selectedExercise = exercises.find((item) => item.name === exerciseName) ?? exercises[0];

      return {
        sessionTitle: latestWorkout?.day_type || "Workout session",
        sessionType: latestWorkout?.session_type || "Workout 1",
        workoutType: selectedExercise?.day_type || "Strength",
        indoorOutdoor: latestWorkout?.is_outdoor ? "Outdoor" : "Indoor",
        dayType: latestWorkout?.day_type || "Current split",
        heroDescription: "Your current session is now reading from backend workouts and exercise history.",
        exerciseOptions: sortedExerciseNames,
        selectedExercise: {
          title: selectedExercise?.name || exerciseName,
          muscleGroup: selectedExercise?.muscle_group || "",
          youtubeTitle: selectedExercise?.youtube_url || selectedExercise?.youtube_search_url || "Exercise demo",
          previewNote: "Demo, instructions, and mistakes are now being driven from the exercise library endpoint.",
          instructions: selectedExercise?.instructions_json || [],
          mistakes: selectedExercise?.common_mistakes_json || [],
          tips: selectedExercise?.tips ? selectedExercise.tips.split(". ").filter(Boolean) : [],
        },
        previousPerformance: {
          lastSession: history[0] ? `${history[0].weight} kg x ${history[0].reps}` : "No history yet",
          bestSet: history[0] ? `${history[0].weight} kg x ${history[0].reps}` : "No best set yet",
          volume: history[0] ? `${history[0].weight * history[0].reps * history[0].sets} kg` : "0 kg",
        },
        liveSummary: {
          exercisesLogged: latestWorkout?.exercises.length || 0,
          totalSets: latestWorkout?.exercises.reduce((sum, item) => sum + item.sets, 0) || 0,
          estimatedCalories: Math.round(latestWorkout?.estimated_calories_burned || 0),
          sessionTime: `${latestWorkout?.duration_min || 0} min`,
        },
        exercises: latestWorkout?.exercises.map((item) => ({
          id: String(item.id),
          name: item.exercise_name,
          muscleGroup: item.muscle_group,
          sets: String(item.sets),
          reps: String(item.reps),
          weight: `${item.weight} kg`,
          previousBest: history[0] ? `${history[0].weight} kg x ${history[0].reps}` : "No history yet",
          pr: item.new_pr === "PR" || item.new_pr === "First",
        })) || [],
      };
    },
  });
}

export function useCreateWorkoutSession() {
  const queryClient = useQueryClient();
  const todayDate = getTodayDateString();

  return useMutation({
    mutationFn: async (payload: WorkoutCreateRequest) => api.workouts.create(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: queryKeys.workouts() });
      void queryClient.invalidateQueries({ queryKey: ["workout-page"] });
      void queryClient.invalidateQueries({ queryKey: queryKeys.today(todayDate) });
      void queryClient.invalidateQueries({ queryKey: queryKeys.dashboard() });
    },
  });
}
