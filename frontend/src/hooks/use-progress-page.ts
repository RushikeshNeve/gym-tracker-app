import { useQuery } from "@tanstack/react-query";

import { progressPageMock } from "@/features/progress/mock-data";
import type { ProgressPageData } from "@/types/tracker-pages";

export function useProgressPage() {
  return useQuery<ProgressPageData>({
    queryKey: ["progress-page"],
    queryFn: async () => progressPageMock,
  });
}
