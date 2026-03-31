import { Navigate, useRoutes } from "react-router-dom";

import { AppShell } from "@/components/layout/app-shell";
import { BodyMetricsPage } from "@/pages/body-metrics-page";
import { CardioPage } from "@/pages/cardio-page";
import { DashboardPage } from "@/pages/dashboard-page";
import { ExerciseLibraryPage } from "@/pages/exercise-library-page";
import { HydrationPage } from "@/pages/hydration-page";
import { LogWorkoutPage } from "@/pages/log-workout-page";
import { NutritionPage } from "@/pages/nutrition-page";
import { ProgressPage } from "@/pages/progress-page";
import { ProgressPhotosPage } from "@/pages/progress-photos-page";
import { TodayPage } from "@/pages/today-page";
import { WeeklyReviewPage } from "@/pages/weekly-review-page";
import { WorkoutTimetablePage } from "@/pages/workout-timetable-page";

function AppRoutes() {
  return useRoutes([
    {
      path: "/",
      element: <AppShell />,
      children: [
        { index: true, element: <Navigate to="/today" replace /> },
        { path: "today", element: <TodayPage /> },
        { path: "dashboard", element: <DashboardPage /> },
        { path: "workouts", element: <LogWorkoutPage /> },
        { path: "workout-timetable", element: <WorkoutTimetablePage /> },
        { path: "nutrition", element: <NutritionPage /> },
        { path: "hydration", element: <HydrationPage /> },
        { path: "body-metrics", element: <BodyMetricsPage /> },
        { path: "cardio", element: <CardioPage /> },
        { path: "progress", element: <ProgressPage /> },
        { path: "progress-photos", element: <ProgressPhotosPage /> },
        { path: "exercise-library", element: <ExerciseLibraryPage /> },
        { path: "weekly-review", element: <WeeklyReviewPage /> },
      ],
    },
  ]);
}

export function AppRouter() {
  return <AppRoutes />;
}
