import type { ProgressPhotosPageData } from "@/types/tracker-pages";

const photos = [
  { id: "1", dateLabel: "Mar 31", photoType: "Front" as const, url: "blob://front-mar-31" },
  { id: "2", dateLabel: "Mar 31", photoType: "Side" as const, url: "blob://side-mar-31" },
  { id: "3", dateLabel: "Mar 31", photoType: "Back" as const, url: "blob://back-mar-31" },
  { id: "4", dateLabel: "Mar 01", photoType: "Front" as const, url: "blob://front-mar-01" },
];

export const progressPhotosPageMock: ProgressPhotosPageData = {
  todayStatus: "Today's front and side shots are done. Back shot is still open.",
  selectedDate: "2026-03-31",
  todayCounts: {
    front: 1,
    side: 1,
    back: 0,
  },
  gallery: photos,
  comparisonPair: {
    left: photos[3],
    right: photos[0],
  },
};
