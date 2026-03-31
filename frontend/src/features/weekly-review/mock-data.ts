import type { WeeklyReviewPageData } from "@/types/tracker-pages";

export const weeklyReviewPageMock: WeeklyReviewPageData = {
  weeklyScore: "88 / 100",
  summaryCards: [
    { label: "Perfect days", value: "5", note: "Five full-compliance days this week." },
    { label: "Incomplete days", value: "2", note: "Both misses came from late hydration pressure." },
    { label: "Failed days", value: "0", note: "No total breakdowns this week." },
    { label: "Average calories", value: "2,040", note: "Still inside the cut plan on average." },
    { label: "Average protein", value: "154 g", note: "Protein floor was strong most days." },
    { label: "Workout consistency", value: "8 sessions", note: "Training stayed on schedule." },
    { label: "Cardio adherence", value: "4 / 5", note: "One session slipped but volume stayed acceptable." },
    { label: "Hydration adherence", value: "5 / 7", note: "The main weekly leak remains water timing." },
  ],
  bodyChanges: [
    { label: "Weight", value: "-0.8 kg", note: "A clean weekly trend." },
    { label: "Waist", value: "-0.6 cm", note: "Visible progress keeps confirming the cut." },
    { label: "Energy", value: "Stable", note: "No major fatigue crash despite the deficit." },
  ],
  reflection: {
    wins: ["Protein stayed high without decision fatigue.", "Outdoor work remained consistent.", "Strength held on the main lifts."],
    misses: ["Hydration was delayed too often into the evening.", "One second workout got compressed late.", "Sleep quality dropped after two long workdays."],
    nextWeekFocus: ["Front-load 2L of water before lunch.", "Pre-decide the second workout window every morning.", "Protect bedtime instead of trading it for scrolling."],
    note: "The system is working. The next step is not more intensity, just fewer leaks in the evening hours.",
  },
};
