import type { HydrationPageData } from "@/types/tracker-pages";

export const hydrationPageMock: HydrationPageData = {
  targetMl: 4000,
  consumedMl: 2600,
  remainingMl: 1400,
  quickAdds: [250, 500, 1000],
  history: [
    { id: "1", time: "06:15 AM", amountMl: 500, note: "Wake-up bottle" },
    { id: "2", time: "08:50 AM", amountMl: 500, note: "With breakfast" },
    { id: "3", time: "12:30 PM", amountMl: 750, note: "Lunch block" },
    { id: "4", time: "04:40 PM", amountMl: 500, note: "Pre-evening push" },
    { id: "5", time: "07:10 PM", amountMl: 350, note: "Before outdoor walk" },
  ],
  weeklyTrend: {
    title: "Weekly hydration",
    description: "Seven-day water adherence against the 4L standard.",
    unit: "L",
    accent: "secondary",
    summary: "Hydration stays strong until late evenings compress the remaining intake window.",
    points: [
      { label: "Mon", value: 4.2 },
      { label: "Tue", value: 3.9 },
      { label: "Wed", value: 4.0 },
      { label: "Thu", value: 3.4 },
      { label: "Fri", value: 4.1 },
      { label: "Sat", value: 3.8 },
      { label: "Sun", value: 2.6 },
    ],
  },
};
