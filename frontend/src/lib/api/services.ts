import { apiClient } from "@/lib/api/client";
import type {
  BodyMetric,
  BodyMetricCreateRequest,
  BodyMetricUpdateRequest,
  CardioLog,
  CardioLogCreateRequest,
  ChallengeDayUpsertRequest,
  DailyTarget,
  DashboardResponse,
  Exercise,
  HydrationChartPoint,
  HydrationDailySummaryResponse,
  HydrationLog,
  HydrationLogCreateRequest,
  MealPlanTemplate,
  MessageResponse,
  NutritionDailySummaryResponse,
  NutritionMealAnalysisRequest,
  NutritionMealAnalysisResult,
  NutritionLog,
  NutritionLogCreateRequest,
  NutritionLogUpdateRequest,
  ProfileWithSummary,
  ProgressPhoto,
  ProgressPhotoCreateRequest,
  Recipe,
  TodayResponse,
  WeeklyReviewRecord,
  WeeklyReviewSummaryResponse,
  WeeklyReviewUpsertRequest,
  Workout,
  WorkoutCreateRequest,
  WorkoutHistoryEntry,
  WorkoutTimetableResponse,
} from "@/types/api";

export const api = {
  today: {
    get: () => apiClient.get<TodayResponse>("/today"),
    update: (date: string, payload: ChallengeDayUpsertRequest) => apiClient.put<TodayResponse["challenge_day"], ChallengeDayUpsertRequest>(`/today/${date}`, payload),
  },
  dashboard: {
    get: () => apiClient.get<DashboardResponse>("/dashboard"),
  },
  workouts: {
    list: () => apiClient.get<Workout[]>("/workouts"),
    create: (payload: WorkoutCreateRequest) => apiClient.post<Workout, WorkoutCreateRequest>("/workouts", payload),
    history: (exerciseName: string) => apiClient.get<WorkoutHistoryEntry[]>(`/workouts/history/${encodeURIComponent(exerciseName)}`),
    delete: (id: number) => apiClient.delete<MessageResponse>(`/workouts/${id}`),
  },
  workoutTimetable: {
    get: () => apiClient.get<WorkoutTimetableResponse>("/workout-timetable"),
  },
  nutrition: {
    daily: (date: string) => apiClient.get<NutritionDailySummaryResponse>(`/nutrition/${date}`),
    create: (payload: NutritionLogCreateRequest) => apiClient.post<NutritionLog, NutritionLogCreateRequest>("/nutrition", payload),
    analyze: (payload: NutritionMealAnalysisRequest) => apiClient.post<NutritionMealAnalysisResult, NutritionMealAnalysisRequest>("/nutrition/analyze", payload),
    update: (id: number, payload: NutritionLogUpdateRequest) => apiClient.patch<NutritionLog, NutritionLogUpdateRequest>(`/nutrition/${id}`, payload),
    delete: (id: number) => apiClient.delete<MessageResponse>(`/nutrition/${id}`),
    duplicate: (sourceDate: string, targetDate: string) => apiClient.post<MessageResponse>("/nutrition/duplicate", undefined, { source_date: sourceDate, target_date: targetDate }),
  },
  hydration: {
    daily: (date: string) => apiClient.get<HydrationDailySummaryResponse>(`/hydration/${date}`),
    weekly: (date: string) => apiClient.get<HydrationChartPoint[]>(`/hydration/weekly/${date}`),
    create: (payload: HydrationLogCreateRequest) => apiClient.post<HydrationLog, HydrationLogCreateRequest>("/hydration", payload),
    delete: (id: number) => apiClient.delete<MessageResponse>(`/hydration/${id}`),
  },
  bodyMetrics: {
    list: () => apiClient.get<BodyMetric[]>("/body-metrics"),
    create: (payload: BodyMetricCreateRequest) => apiClient.post<BodyMetric, BodyMetricCreateRequest>("/body-metrics", payload),
    update: (id: number, payload: BodyMetricUpdateRequest) => apiClient.patch<BodyMetric, BodyMetricUpdateRequest>(`/body-metrics/${id}`, payload),
    delete: (id: number) => apiClient.delete<MessageResponse>(`/body-metrics/${id}`),
  },
  cardio: {
    list: () => apiClient.get<CardioLog[]>("/cardio"),
    create: (payload: CardioLogCreateRequest) => apiClient.post<CardioLog, CardioLogCreateRequest>("/cardio", payload),
    delete: (id: number) => apiClient.delete<MessageResponse>(`/cardio/${id}`),
  },
  progressPhotos: {
    list: (date?: string) => apiClient.get<ProgressPhoto[]>("/progress-photos", date ? { log_date: date } : undefined),
    create: (payload: ProgressPhotoCreateRequest) => apiClient.post<ProgressPhoto, ProgressPhotoCreateRequest>("/progress-photos", payload),
    upload: (file: File, logDate: string, photoType: string, notes?: string) => {
      const formData = new FormData();
      formData.append("photo", file);
      formData.append("log_date", logDate);
      formData.append("photo_type", photoType.toLowerCase());
      if (notes) {
        formData.append("notes", notes);
      }
      return apiClient.uploadForm<ProgressPhoto>("/progress-photos/upload", formData);
    },
  },
  weeklyReview: {
    summary: (weekStart: string) => apiClient.get<WeeklyReviewSummaryResponse>(`/weekly-review/${weekStart}`),
    record: (weekStart: string) => apiClient.get<WeeklyReviewRecord | null>(`/weekly-review/${weekStart}/record`),
    upsert: (weekStart: string, payload: WeeklyReviewUpsertRequest) => apiClient.put<WeeklyReviewRecord, WeeklyReviewUpsertRequest>(`/weekly-review/${weekStart}`, payload),
  },
  profile: {
    get: () => apiClient.get<ProfileWithSummary>("/profile"),
    target: (date: string) => apiClient.get<DailyTarget>(`/profile/targets/${date}`),
  },
  recipes: {
    list: (mealType?: string) => apiClient.get<Recipe[]>("/recipes", mealType ? { meal_type: mealType } : undefined),
  },
  mealPlans: {
    get: (date: string) => apiClient.get<MealPlanTemplate[]>(`/meal-plans/${date}`),
  },
  exercises: {
    list: (search?: string, dayType?: string, muscleGroup?: string) =>
      apiClient.get<Exercise[]>("/exercises", { search, day_type: dayType, muscle_group: muscleGroup }),
    detail: (id: number) => apiClient.get<Exercise>(`/exercises/${id}`),
  },
};
