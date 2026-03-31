import type { ExerciseLibraryPageData } from "@/types/tracker-pages";

export const exerciseLibraryPageMock: ExerciseLibraryPageData = {
  filters: ["Chest", "Back", "Legs", "Shoulders", "Arms", "Bodyweight", "Machines"],
  searchPlaceholder: "Search exercises, muscle groups, or equipment",
  exercises: [
    {
      id: "1",
      title: "Incline Dumbbell Press",
      muscleGroups: ["Chest", "Shoulders", "Triceps"],
      equipment: "Dumbbells + bench",
      youtubeTitle: "Incline Dumbbell Press demo",
      instructions: ["Set feet hard into the floor.", "Press with the elbows under the wrists.", "Lower with control."],
      mistakes: ["Too much bench angle.", "Short range at the bottom.", "Letting shoulders drift forward."],
      tips: ["Use the same setup weekly.", "Track top set plus back-off.", "Stop before rep speed collapses."],
    },
    {
      id: "2",
      title: "Romanian Deadlift",
      muscleGroups: ["Hamstrings", "Glutes", "Lower back"],
      equipment: "Barbell",
      youtubeTitle: "Romanian Deadlift demo",
      instructions: ["Push hips back first.", "Keep the bar close.", "Pause near the stretch."],
      mistakes: ["Turning it into a squat.", "Rounding the upper back.", "Losing tension at the bottom."],
      tips: ["Use straps only if grip is the limiter.", "Stay strict with tempo.", "Stop where spine position stays clean."],
    },
    {
      id: "3",
      title: "Lat Pulldown",
      muscleGroups: ["Lats", "Upper back", "Biceps"],
      equipment: "Cable machine",
      youtubeTitle: "Lat Pulldown demo",
      instructions: ["Set the chest up before the pull.", "Drive elbows down.", "Control the return."],
      mistakes: ["Yanking with momentum.", "Pulling too low.", "Shrugging the shoulders."],
      tips: ["Slight lean only.", "Use straps if needed.", "Think elbows to pockets."],
    },
  ],
};
