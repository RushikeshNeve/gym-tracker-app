import {
  BookOpen,
  Camera,
  Droplets,
  Dumbbell,
  Gauge,
  HeartPulse,
  LayoutDashboard,
  LineChart,
  NotebookText,
  Salad,
  SunMedium,
  CalendarRange,
} from "lucide-react";

export const navItems = [
  { label: "Today", to: "/today", icon: SunMedium },
  { label: "Dashboard", to: "/dashboard", icon: LayoutDashboard },
  { label: "Log Workout", to: "/workouts", icon: Dumbbell },
  { label: "Workout Timetable", to: "/workout-timetable", icon: CalendarRange },
  { label: "Nutrition", to: "/nutrition", icon: Salad },
  { label: "Hydration", to: "/hydration", icon: Droplets },
  { label: "Body Metrics", to: "/body-metrics", icon: Gauge },
  { label: "Cardio", to: "/cardio", icon: HeartPulse },
  { label: "Progress", to: "/progress", icon: LineChart },
  { label: "Progress Photos", to: "/progress-photos", icon: Camera },
  { label: "Exercise Library", to: "/exercise-library", icon: BookOpen },
  { label: "Weekly Review", to: "/weekly-review", icon: NotebookText },
] as const;
