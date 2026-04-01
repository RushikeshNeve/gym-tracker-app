import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { api } from "@/lib/api/services";
import { queryKeys } from "@/lib/api/query-keys";
import { getTodayDateString } from "@/lib/date";
import type { WorkoutCreateRequest, WorkoutTimetableResponse } from "@/types/api";
import type { WorkoutPageData, WorkoutTimetableData } from "@/types/tracker-pages";

const exerciseAliasMap: Record<string, string> = {
  "Dumbbell Press": "Flat Dumbbell Press",
  "Barbell Bench Press": "Flat Barbell Bench Press",
  "Chest Fly (DB)": "Cable Fly",
  "DB Lateral Raise": "Dumbbell Lateral Raise",
  "Overhead Cable Ext": "Overhead Rope Extension",
  "DB Overhead Ext": "Overhead Rope Extension",
  "Rope Extension": "Overhead Rope Extension",
  "Machine Row Wide": "Seated Machine Row Wide Grip",
  "Cable Row Wide": "Cable Row",
  "Close Grip Row": "Seated Machine Row Close Grip",
  "Barbell Shrugs": "Shrugs",
  "Machine Shrugs": "Shrugs",
  "Barbell Curl": "EZ Bar Curl",
  "Incline DB Curl": "Dumbbell Curl",
  "Hack Squat": "Squat",
  "Smith Squat": "Smith Machine Squat",
  "Barbell Squat": "Back Squat",
  "Stiff Leg Deadlift": "Romanian Deadlift",
  "Good Mornings": "Romanian Deadlift",
  "Sissy Squat": "Leg Extension",
  "Machine Quad Ext": "Leg Extension",
  "Nordic Curl": "Lying Leg Curl",
  "Standing Raise": "Standing Calf Raise",
  "Seated Raise": "Seated Calf Raise",
  "Leg Press Calf": "Calf Raises",
  "Running (25 min)": "Treadmill Running",
  "Cycling (30 min)": "Cycling",
  "Incline Walk (25 min)": "Incline Walking",
  "Sprint Intervals": "Outdoor Run",
  "Incline DB Press": "Incline Dumbbell Press",
};

function normalizeExerciseName(value: string) {
  return value
    .toLowerCase()
    .replace(/\([^)]*\)/g, " ")
    .replace(/\bdb\b/g, "dumbbell")
    .replace(/\bext\b/g, "extension")
    .replace(/\s+/g, " ")
    .trim();
}

function resolveExerciseName(requestedName: string | undefined, availableNames: string[]) {
  if (!requestedName) return undefined;
  if (availableNames.includes(requestedName)) return requestedName;

  const aliasedName = exerciseAliasMap[requestedName];
  if (aliasedName && availableNames.includes(aliasedName)) {
    return aliasedName;
  }

  const normalizedRequested = normalizeExerciseName(requestedName);
  return (
    availableNames.find((name) => normalizeExerciseName(name) === normalizedRequested) ??
    availableNames.find((name) => normalizeExerciseName(name).includes(normalizedRequested)) ??
    availableNames.find((name) => normalizedRequested.includes(normalizeExerciseName(name))) ??
    requestedName
  );
}

function formatPerformance(weight: number, reps: number, durationSeconds: number | null) {
  if (durationSeconds && durationSeconds > 0) {
    return `${weight > 0 ? `${weight} kg ` : ""}${formatDuration(durationSeconds)}`.trim();
  }
  return `${weight} kg x ${reps}`;
}

function formatDuration(durationSeconds: number) {
  const minutes = Math.floor(durationSeconds / 60);
  const seconds = durationSeconds % 60;
  return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}

export function useWorkoutPage(selectedExerciseName?: string, selectedExerciseId?: number) {
  return useQuery<WorkoutPageData>({
    queryKey: ["workout-page", selectedExerciseName ?? "", selectedExerciseId ?? 0],
    queryFn: async () => {
      const [workouts, exercises] = await Promise.all([api.workouts.list(), api.exercises.list()]);
      const latestWorkout = workouts[0];
      const sortedExerciseNames = [...new Set(exercises.map((item) => item.name))].sort((left, right) => left.localeCompare(right));
      const selectedById = selectedExerciseId ? exercises.find((item) => item.id === selectedExerciseId) : undefined;
      const resolvedRequestedExercise = resolveExerciseName(selectedExerciseName, sortedExerciseNames);
      const exerciseName = selectedById?.name || resolvedRequestedExercise || latestWorkout?.exercises[0]?.exercise_name || sortedExerciseNames[0] || "Exercise";
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
          lastSession: history[0] ? formatPerformance(history[0].weight, history[0].reps, history[0].duration_seconds) : "No history yet",
          bestSet: history[0] ? formatPerformance(history[0].weight, history[0].reps, history[0].duration_seconds) : "No best set yet",
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
          duration: item.duration_seconds ? formatDuration(item.duration_seconds) : undefined,
          weight: `${item.weight} kg`,
          previousBest: history[0] ? formatPerformance(history[0].weight, history[0].reps, history[0].duration_seconds) : "No history yet",
          pr: item.new_pr === "PR" || item.new_pr === "First",
          inputMode: item.duration_seconds ? "duration" : "reps",
        })) || [],
      };
    },
  });
}

export function useWorkoutTimetable() {
  return useQuery<WorkoutTimetableData>({
    queryKey: ["workout-timetable"],
    queryFn: async () => {
      const data: WorkoutTimetableResponse = await api.workoutTimetable.get();
      return {
        weeklySplit: data.weekly_split,
        timetableDays: data.timetable_days.map((day) => ({
          id: day.id,
          dayLabel: day.day_label,
          title: day.title,
          subtitle: day.subtitle,
          accent: day.accent,
          notes: day.notes,
          images: day.images,
          blocks: day.blocks.map((block) => ({
            category: block.category,
            setsReps: block.sets_reps,
            options: block.options,
          })),
        })),
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
