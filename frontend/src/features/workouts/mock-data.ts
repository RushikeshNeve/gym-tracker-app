import type { WorkoutPageData } from "@/types/tracker-pages";

export const workoutPageMock: WorkoutPageData = {
  sessionTitle: "Push session",
  sessionType: "Strength",
  workoutType: "Upper body",
  indoorOutdoor: "Indoor",
  dayType: "Day 42 split",
  heroDescription: "Build the session for speed. Log fast, compare to last week, and keep the working sets obvious under fatigue.",
  exerciseOptions: ["Incline Dumbbell Press", "Machine Chest Press", "Cable Lateral Raise", "Overhead Triceps Extension"],
  selectedExercise: {
    title: "Incline Dumbbell Press",
    muscleGroup: "Chest + front delts",
    youtubeTitle: "Incline Dumbbell Press demo",
    previewNote: "Use the preview area as a fast form reminder between sets.",
    instructions: ["Set scapula before the first rep.", "Drive elbows under wrists.", "Control the bottom without bouncing."],
    mistakes: ["Flaring elbows too early.", "Shortening the bottom range.", "Rushing the eccentric."],
    tips: ["Use the same bench angle each week.", "Track the top set and one back-off set.", "Stop one rep before form leaks."],
  },
  previousPerformance: {
    lastSession: "30 kg x 8, 8, 7",
    bestSet: "32.5 kg x 9",
    volume: "1,485 kg",
  },
  liveSummary: {
    exercisesLogged: 4,
    totalSets: 13,
    estimatedCalories: 290,
    sessionTime: "38 min",
  },
  exercises: [
    { id: "1", name: "Incline Dumbbell Press", muscleGroup: "Chest", sets: "3", reps: "8-10", weight: "30 kg", previousBest: "32.5 kg x 9", pr: true },
    { id: "2", name: "Machine Chest Press", muscleGroup: "Chest", sets: "3", reps: "10-12", weight: "55 kg", previousBest: "60 kg x 10", pr: false },
    { id: "3", name: "Cable Lateral Raise", muscleGroup: "Shoulders", sets: "4", reps: "12-15", weight: "10 kg", previousBest: "12.5 kg x 12", pr: false },
    { id: "4", name: "Overhead Triceps Extension", muscleGroup: "Triceps", sets: "3", reps: "10-12", weight: "27.5 kg", previousBest: "30 kg x 11", pr: false },
  ],
};
