export type DashboardTone = "neutral" | "primary" | "secondary" | "warning";

export type DashboardKpi = {
  label: string;
  value: string;
  detail: string;
  tone?: DashboardTone;
};

export type TrendPoint = {
  label: string;
  value: number;
};

export type DashboardTrend = {
  title: string;
  description: string;
  unit: string;
  accent?: "primary" | "secondary" | "warning";
  points: TrendPoint[];
  summary: string;
};

export type RecentPr = {
  id: string;
  exercise: string;
  value: string;
  dateLabel: string;
};

export type WeekSummaryItem = {
  label: string;
  value: string;
  tone?: "primary" | "secondary" | "warning";
};

export type DashboardSummary = {
  heroLabel: string;
  heroTitle: string;
  heroDescription: string;
  kpis: DashboardKpi[];
  trends: {
    weight: DashboardTrend;
    waist: DashboardTrend;
    calories: DashboardTrend;
    protein: DashboardTrend;
    hydration: DashboardTrend;
    compliance: DashboardTrend;
  };
  workoutFrequencySummary: {
    totalSessions: number;
    completedDays: string[];
    summary: string;
  };
  cardioMinutesSummary: {
    totalMinutes: number;
    averageMinutes: number;
    summary: string;
  };
  recentPrs: RecentPr[];
  weekSummary: WeekSummaryItem[];
  nextPlannedWorkout: {
    title: string;
    focus: string;
    time: string;
    note: string;
  };
};
