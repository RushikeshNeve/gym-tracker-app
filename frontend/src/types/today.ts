export type TaskStatus = "pending" | "completed";

export type TodayTask = {
  id: string;
  title: string;
  description: string;
  category: string;
  status: TaskStatus;
  accent: "primary" | "secondary" | "warning";
  interaction: "toggle" | "navigate";
  actionLabel?: string;
  pendingActionLabel?: string;
  completedActionLabel?: string;
  navigateTo?: string;
  field:
    | "workout_1_completed"
    | "one_workout_outdoors"
    | "followed_diet"
    | "no_cheat_meals"
    | "water_goal_completed"
    | "progress_picture_taken";
};

export type TodaySummary = {
  dayNumber: number;
  totalDays: number;
  completionPercentage: number;
  currentStreak: number;
  perfectDays: number;
  failedDays: number;
  completedCount: number;
  pendingCount: number;
  heroCopy: string;
  quickActions: string[];
  notes: string;
  focusLabel: string;
  splitLabel: string;
  hydrationLiters: number;
  hydrationTargetLiters: number;
  calories: number;
  caloriesTarget: number;
  protein: number;
  complianceScore: number;
  totalSessions: number;
  workoutSessions: number;
  cardioSessions: number;
  outdoorSessions: number;
  photoCount: number;
  pendingTasks: string[];
  dayStatus: string;
  tasks: TodayTask[];
};
