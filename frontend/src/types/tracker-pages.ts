export type SimplePoint = {
  label: string;
  value: number;
};

export type TrendData = {
  title: string;
  description: string;
  unit: string;
  accent?: "primary" | "secondary" | "warning";
  points: SimplePoint[];
  summary: string;
};

export type WorkoutExercise = {
  id: string;
  name: string;
  muscleGroup: string;
  sets: string;
  reps: string;
  duration?: string;
  weight: string;
  previousBest: string;
  pr: boolean;
  setLabel?: string;
  note?: string;
  inputMode?: "reps" | "duration";
};

export type TimetableExerciseOption = {
  id: number;
  name: string;
};

export type TimetableOptionGroup = {
  category: string;
  options: TimetableExerciseOption[];
  setsReps: string;
};

export type TimetableDay = {
  id: string;
  dayLabel: string;
  title: string;
  subtitle: string;
  accent: "primary" | "secondary" | "warning";
  notes?: string[];
  images: string[];
  blocks: TimetableOptionGroup[];
};

export type WorkoutTimetableData = {
  weeklySplit: Array<{ day: string; workout: string }>;
  timetableDays: TimetableDay[];
};

export type WorkoutPageData = {
  sessionTitle: string;
  sessionType: string;
  workoutType: string;
  indoorOutdoor: "Indoor" | "Outdoor";
  dayType: string;
  heroDescription: string;
  exerciseOptions: string[];
  selectedExercise: {
    title: string;
    muscleGroup: string;
    youtubeTitle: string;
    previewNote: string;
    instructions: string[];
    mistakes: string[];
    tips: string[];
  };
  previousPerformance: {
    lastSession: string;
    bestSet: string;
    volume: string;
  };
  liveSummary: {
    exercisesLogged: number;
    totalSets: number;
    estimatedCalories: number;
    sessionTime: string;
  };
  exercises: WorkoutExercise[];
};

export type HydrationLog = {
  id: string;
  time: string;
  amountMl: number;
  note: string;
};

export type HydrationPageData = {
  targetMl: number;
  consumedMl: number;
  remainingMl: number;
  quickAdds: number[];
  history: HydrationLog[];
  weeklyTrend: TrendData;
};

export type MetricStat = {
  label: string;
  dayOne: string;
  current: string;
  change: string;
  tone?: "primary" | "secondary" | "warning";
};

export type BodyMetricsPageData = {
  currentStats: MetricStat[];
  weeklyChanges: { label: string; value: string; note: string }[];
  milestones: { id: string; title: string; status: string; note: string }[];
  trends: TrendData[];
  entries: Array<{
    id: number;
    date: string;
    bodyWeight: number | null;
    waist: number | null;
    hips: number | null;
    chest: number | null;
    arms: number | null;
    thighs: number | null;
    neck: number | null;
    bodyFat: number | null;
    notes: string;
    progressNotes: string;
  }>;
};

export type CardioLog = {
  id: string;
  type: string;
  duration: string;
  calories: string;
  distance: string;
  pace: string;
  outdoor: boolean;
  dateLabel: string;
};

export type CardioPageData = {
  sessionPresets: { label: string; note: string }[];
  weeklySummary: { label: string; value: string; note: string }[];
  history: CardioLog[];
  trend: TrendData;
};

export type ProgressPageData = {
  trends: TrendData[];
  strongestLifts: { exercise: string; value: string; note: string }[];
  prHistory: { id: string; title: string; value: string; when: string }[];
  transformationAnalytics: { label: string; value: string; note: string }[];
};

export type ProgressPhoto = {
  id: string;
  dateLabel: string;
  photoType: "Front" | "Side" | "Back";
  url: string;
};

export type ProgressPhotosPageData = {
  todayStatus: string;
  selectedDate: string;
  todayCounts: {
    front: number;
    side: number;
    back: number;
  };
  gallery: ProgressPhoto[];
  comparisonPair: {
    left: ProgressPhoto;
    right: ProgressPhoto;
  };
};

export type ExerciseLibraryItem = {
  id: string;
  title: string;
  muscleGroups: string[];
  equipment: string;
  youtubeTitle: string;
  instructions: string[];
  mistakes: string[];
  tips: string[];
};

export type ExerciseLibraryPageData = {
  filters: string[];
  searchPlaceholder: string;
  exercises: ExerciseLibraryItem[];
};

export type WeeklyReviewPageData = {
  weeklyScore: string;
  summaryCards: { label: string; value: string; note: string }[];
  bodyChanges: { label: string; value: string; note: string }[];
  reflection: {
    wins: string[];
    misses: string[];
    nextWeekFocus: string[];
    note: string;
  };
};
