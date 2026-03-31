import { useQuery } from "@tanstack/react-query";

import { api } from "@/lib/api/services";
import type { ExerciseLibraryPageData } from "@/types/tracker-pages";

export function useExerciseLibraryPage(search?: string, muscleGroup?: string) {
  return useQuery<ExerciseLibraryPageData>({
    queryKey: ["exercise-library-page", search ?? "", muscleGroup ?? ""],
    queryFn: async () => {
      const exercises = await api.exercises.list(search, undefined, muscleGroup);
      return {
        filters: [...new Set(exercises.map((item) => item.muscle_group).filter(Boolean))],
        searchPlaceholder: "Search exercises, muscle groups, or equipment",
        exercises: exercises.map((exercise) => ({
          id: String(exercise.id),
          title: exercise.name,
          muscleGroups: exercise.muscle_group ? exercise.muscle_group.split("/").map((item) => item.trim()) : [],
          equipment: exercise.day_type || "Equipment not specified",
          youtubeTitle: exercise.youtube_url || exercise.youtube_search_url,
          instructions: exercise.instructions_json,
          mistakes: exercise.common_mistakes_json,
          tips: exercise.tips ? exercise.tips.split(". ").filter(Boolean) : [],
        })),
      };
    },
  });
}
