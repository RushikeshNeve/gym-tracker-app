import type { CardioPageData } from "@/types/tracker-pages";

export const cardioPageMock: CardioPageData = {
  sessionPresets: [
    { label: "Outdoor incline walk", note: "45 minutes, challenge-safe, low fatigue." },
    { label: "Cycle intervals", note: "Short higher-output conditioning block." },
    { label: "Zone 2 treadmill", note: "Reliable indoor fallback on bad weather days." },
  ],
  weeklySummary: [
    { label: "Total minutes", value: "205", note: "Cardio has stayed consistent this week." },
    { label: "Outdoor sessions", value: "4", note: "Outdoor work is carrying compliance." },
    { label: "Calories burned", value: "1,230", note: "Useful support, not the core strategy." },
  ],
  history: [
    { id: "1", type: "Outdoor walk", duration: "48 min", calories: "330 kcal", distance: "4.6 km", pace: "10:25 / km", outdoor: true, dateLabel: "Today" },
    { id: "2", type: "Treadmill incline", duration: "35 min", calories: "280 kcal", distance: "3.1 km", pace: "11:10 / km", outdoor: false, dateLabel: "Yesterday" },
    { id: "3", type: "Outdoor jog-walk", duration: "42 min", calories: "360 kcal", distance: "5.0 km", pace: "8:24 / km", outdoor: true, dateLabel: "2 days ago" },
  ],
  trend: {
    title: "Weekly cardio trend",
    description: "Minutes of cardio across the week.",
    unit: "min",
    accent: "secondary",
    summary: "Cardio volume is high enough to support the phase without crowding recovery.",
    points: [
      { label: "Mon", value: 30 },
      { label: "Tue", value: 42 },
      { label: "Wed", value: 0 },
      { label: "Thu", value: 35 },
      { label: "Fri", value: 50 },
      { label: "Sat", value: 0 },
      { label: "Sun", value: 48 },
    ],
  },
};
