import type { BodyMetricsPageData } from "@/types/tracker-pages";

export const bodyMetricsPageMock: BodyMetricsPageData = {
  currentStats: [
    { label: "Weight", dayOne: "86.0 kg", current: "81.4 kg", change: "-4.6 kg", tone: "primary" },
    { label: "Waist", dayOne: "93.5 cm", current: "90.0 cm", change: "-3.5 cm", tone: "primary" },
    { label: "Hips", dayOne: "101 cm", current: "99 cm", change: "-2 cm" },
    { label: "Chest", dayOne: "104 cm", current: "102.5 cm", change: "-1.5 cm" },
    { label: "Arms", dayOne: "37 cm", current: "36.5 cm", change: "-0.5 cm" },
    { label: "Thighs", dayOne: "59 cm", current: "57.8 cm", change: "-1.2 cm" },
    { label: "Neck", dayOne: "38.5 cm", current: "38 cm", change: "-0.5 cm" },
    { label: "Body fat", dayOne: "24.5%", current: "21.8%", change: "-2.7%", tone: "secondary" },
  ],
  weeklyChanges: [
    { label: "Weight this week", value: "-0.8 kg", note: "A clean drop without a crash signal." },
    { label: "Waist this week", value: "-0.6 cm", note: "Waist confirms the scale is telling the truth." },
    { label: "Estimated body fat", value: "-0.4%", note: "Trend still moving in the right direction." },
  ],
  milestones: [
    { id: "1", title: "Sub-82 kg", status: "Reached", note: "First big visible bodyweight milestone." },
    { id: "2", title: "Waist below 90 cm", status: "Close", note: "One clean week could finish this." },
    { id: "3", title: "Body fat below 20%", status: "Pending", note: "Requires sustained consistency over the next block." },
  ],
  trends: [
    {
      title: "Weight trend",
      description: "Bodyweight trend over the current week.",
      unit: "kg",
      accent: "primary",
      summary: "Trend remains controlled and steady.",
      points: [
        { label: "Mon", value: 82.4 },
        { label: "Tue", value: 82.1 },
        { label: "Wed", value: 81.9 },
        { label: "Thu", value: 81.8 },
        { label: "Fri", value: 81.7 },
        { label: "Sat", value: 81.5 },
        { label: "Sun", value: 81.4 },
      ],
    },
    {
      title: "Waist trend",
      description: "Waistline progress across the same period.",
      unit: "cm",
      accent: "secondary",
      summary: "Waist reduction is lining up with the goal phase.",
      points: [
        { label: "Mon", value: 90.8 },
        { label: "Tue", value: 90.6 },
        { label: "Wed", value: 90.5 },
        { label: "Thu", value: 90.4 },
        { label: "Fri", value: 90.3 },
        { label: "Sat", value: 90.1 },
        { label: "Sun", value: 90.0 },
      ],
    },
  ],
  entries: [
    {
      id: 1,
      date: "2026-03-31",
      bodyWeight: 81.4,
      waist: 90.0,
      hips: 99.0,
      chest: 102.5,
      arms: 36.5,
      thighs: 57.8,
      neck: 38.0,
      bodyFat: 21.8,
      notes: "Morning check-in",
      progressNotes: "Waist and weight are both trending down in sync.",
    },
  ],
};
