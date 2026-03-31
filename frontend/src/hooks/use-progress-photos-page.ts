import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { api } from "@/lib/api/services";
import { formatShortDate, getTodayDateString } from "@/lib/date";
import { queryKeys } from "@/lib/api/query-keys";
import type { ProgressPhotosPageData } from "@/types/tracker-pages";

export function useProgressPhotosPage() {
  const todayDate = getTodayDateString();
  return useQuery<ProgressPhotosPageData>({
    queryKey: ["progress-photos-page", todayDate],
    queryFn: async () => {
      const [todayPhotos, allPhotos] = await Promise.all([
        api.progressPhotos.list(todayDate),
        api.progressPhotos.list(),
      ]);
      const ordered = [...allPhotos].sort((a, b) => b.date.localeCompare(a.date));
      const left = ordered[ordered.length - 1] ?? ordered[0];
      const right = ordered[0];
      return {
        todayStatus:
          todayPhotos.length > 0
            ? `${todayPhotos.length} progress photo${todayPhotos.length > 1 ? "s" : ""} logged today.`
            : "No progress photos logged today yet.",
        selectedDate: todayDate,
        todayCounts: {
          front: todayPhotos.filter((photo) => photo.photo_type.toLowerCase() === "front").length,
          side: todayPhotos.filter((photo) => photo.photo_type.toLowerCase() === "side").length,
          back: todayPhotos.filter((photo) => photo.photo_type.toLowerCase() === "back").length,
        },
        gallery: ordered.map((photo) => ({
          id: String(photo.id),
          dateLabel: formatShortDate(photo.date),
          photoType: (photo.photo_type.charAt(0).toUpperCase() + photo.photo_type.slice(1)) as "Front" | "Side" | "Back",
          url: photo.file_url,
        })),
        comparisonPair: {
          left: {
            id: String(left?.id ?? 0),
            dateLabel: left ? formatShortDate(left.date) : "N/A",
            photoType: ((left?.photo_type ?? "front").charAt(0).toUpperCase() + (left?.photo_type ?? "front").slice(1)) as "Front" | "Side" | "Back",
            url: left?.file_url ?? "",
          },
          right: {
            id: String(right?.id ?? 0),
            dateLabel: right ? formatShortDate(right.date) : "N/A",
            photoType: ((right?.photo_type ?? "front").charAt(0).toUpperCase() + (right?.photo_type ?? "front").slice(1)) as "Front" | "Side" | "Back",
            url: right?.file_url ?? "",
          },
        },
      };
    },
  });
}

export function useUploadProgressPhoto() {
  const queryClient = useQueryClient();
  const todayDate = getTodayDateString();

  return useMutation({
    mutationFn: async ({
      file,
      logDate,
      photoType,
      notes,
    }: {
      file: File;
      logDate: string;
      photoType: "Front" | "Side" | "Back";
      notes?: string;
    }) => api.progressPhotos.upload(file, logDate, photoType, notes),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: queryKeys.progressPhotos() });
      void queryClient.invalidateQueries({ queryKey: ["progress-photos-page", todayDate] });
      void queryClient.invalidateQueries({ queryKey: queryKeys.today(todayDate) });
    },
  });
}
