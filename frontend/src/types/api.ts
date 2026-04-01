export type IsoDate = string;
export type IsoDateTime = string;

export type MessageResponse = {
  message: string;
};

export type TimestampFields = {
  created_at: IsoDateTime;
  updated_at: IsoDateTime;
};

export type DailyTarget = TimestampFields & {
  id: number;
  profile_id: number;
  date: IsoDate;
  calorie_target: number;
  protein_target: number;
  carbs_target: number;
  fats_target: number;
  fiber_target: number;
  water_target_liters: number;
};

export type NutritionTotals = {
  calories: number;
  protein: number;
  carbs: number;
  fats: number;
  fiber: number;
};

export type TodayResponse = {
  date: IsoDate;
  day_number: number;
  remaining_days: number;
  day_status: string;
  compliance_score: number;
  total_completed: number;
  required_total: number;
  pending_tasks: string[];
  current_streak: number;
  perfect_days: number;
  failed_days: number;
  activity: {
    workout_sessions: number;
    cardio_sessions: number;
    total_sessions: number;
    outdoor_sessions: number;
    water_total_ml: number;
    water_target_ml: number;
    nutrition_totals: NutritionTotals;
  };
  nutrition_bonus_flags: Record<string, boolean>;
  energy_balance: {
    maintenance_calories: number;
    target_calories: number;
    food_calories: number;
    exercise_calories: number;
    net_calories: number;
    deficit_or_surplus: number;
    status: string;
    protein: number;
  };
  split_plan: {
    today_plan: string;
    tomorrow_plan: string;
    missed_recovery: string;
  };
  challenge_day: TimestampFields & {
    id: number;
    profile_id: number;
    date: IsoDate;
    challenge_day_number: number | null;
    workout_1_completed: boolean;
    workout_2_completed: boolean;
    one_workout_outdoors: boolean;
    followed_diet: boolean;
    no_cheat_meals: boolean;
    no_alcohol: boolean;
    water_goal_completed: boolean;
    progress_picture_taken: boolean;
    body_weight: number | null;
    steps: number;
    sleep_hours: number;
    mood: string;
    energy_level: number;
    notes: string;
    selected_diet_plan: string;
    diet_followed: boolean;
    cheat_meal: boolean;
    junk_food: boolean;
    sugary_drinks: boolean;
    hunger_level: number;
    cravings_level: number;
    binge_urge: number;
    diet_notes: string;
    day_status: string;
    compliance_score: number;
  };
};

export type ChallengeDayUpsertRequest = {
  date: IsoDate;
  challenge_day_number?: number | null;
  workout_1_completed?: boolean;
  workout_2_completed?: boolean;
  one_workout_outdoors?: boolean;
  followed_diet?: boolean;
  no_cheat_meals?: boolean;
  no_alcohol?: boolean;
  water_goal_completed?: boolean;
  progress_picture_taken?: boolean;
  body_weight?: number | null;
  steps?: number;
  sleep_hours?: number;
  mood?: string;
  energy_level?: number;
  notes?: string;
  selected_diet_plan?: string;
  diet_followed?: boolean;
  cheat_meal?: boolean;
  junk_food?: boolean;
  sugary_drinks?: boolean;
  hunger_level?: number;
  cravings_level?: number;
  binge_urge?: number;
  diet_notes?: string;
};

export type DashboardResponse = {
  metrics: {
    streak: number;
    weekly_workouts: number;
    weekly_volume: number;
    weekly_prs: number;
    cardio_mins: number;
    cardio_cals: number;
    latest_weight: number | null;
    weekly_score: number;
    consistency_pct: number;
    perfect_days: number;
    failed_days: number;
  };
  energy: TodayResponse["energy_balance"];
  nutrition: {
    totals: NutritionTotals;
    remaining: NutritionTotals;
    targets: DailyTarget;
  };
  hydration: {
    date: IsoDate;
    total_ml: number;
    target_ml: number;
    target_liters: number;
    remaining_ml: number;
    bottle_count: number;
    progress_pct: number;
  };
  challenge: {
    day_status: string;
    compliance_score: number;
    pending_tasks: string[];
    split_plan: TodayResponse["split_plan"];
    weekly_summary: WeeklyReviewSummaryResponse;
  };
  recent_activity: Array<{
    date: IsoDate;
    day_type: string;
    session_type: string;
    is_outdoor: boolean;
    exercise_name: string;
    weight: number;
    reps: number;
    sets: number;
    new_pr: string;
  }>;
  recent_prs: Array<{
    date: IsoDate;
    exercise_name: string;
    weight: number;
    reps: number;
    new_pr: string;
  }>;
  weekly_energy_chart: Array<{
    date: IsoDate;
    maintenance_calories: number;
    target_calories: number;
    food_calories: number;
    exercise_calories: number;
    net_calories: number;
    deficit_or_surplus: number;
    status: string;
    protein: number;
  }>;
  weekly_nutrition_chart: Array<{
    date: IsoDate;
    calories: number;
    protein: number;
    carbs: number;
    fats: number;
    fiber: number;
  }>;
  weekly_hydration_chart: Array<{
    date: IsoDate;
    total_ml: number;
    target_ml: number;
    adherence_pct: number;
  }>;
};

export type WorkoutExercise = TimestampFields & {
  id: number;
  workout_id: number;
  exercise_name: string;
  muscle_group: string;
  weight: number;
  reps: number;
  sets: number;
  duration_seconds: number | null;
  volume: number;
  near_failure: boolean;
  new_pr: string;
  notes: string;
};

export type Workout = TimestampFields & {
  id: number;
  profile_id: number;
  date: IsoDate;
  day_type: string;
  session_type: string;
  is_outdoor: boolean;
  duration_min: number;
  start_time: string | null;
  end_time: string | null;
  session_notes: string;
  estimated_calories_burned: number;
  exercises: WorkoutExercise[];
};

export type WorkoutCreateRequest = {
  date: IsoDate;
  day_type: string;
  session_type: string;
  is_outdoor: boolean;
  duration_min: number;
  start_time?: string | null;
  end_time?: string | null;
  session_notes?: string;
  estimated_calories_burned?: number | null;
  exercises: Array<{
    exercise_name: string;
    muscle_group: string;
    weight: number;
    reps: number;
    sets: number;
    duration_seconds?: number | null;
    near_failure?: boolean;
    notes?: string;
  }>;
};

export type WorkoutHistoryEntry = {
  date: IsoDate;
  exercise_name: string;
  weight: number;
  reps: number;
  sets: number;
  duration_seconds: number | null;
  new_pr: string;
  session_type: string;
  is_outdoor: boolean;
};

export type Exercise = TimestampFields & {
  id: number;
  name: string;
  day_type: string;
  muscle_group: string;
  youtube_url: string;
  youtube_search_url: string;
  instructions_json: string[];
  common_mistakes_json: string[];
  tips: string;
  matched: boolean;
};

export type WorkoutTimetableResponse = {
  weekly_split: Array<{
    day: string;
    workout: string;
  }>;
  timetable_days: Array<{
    id: string;
    day_label: string;
    title: string;
    subtitle: string;
    accent: "primary" | "secondary" | "warning";
    notes: string[];
    images: string[];
    blocks: Array<{
      category: string;
      sets_reps: string;
      options: Array<{
        id: number;
        name: string;
      }>;
    }>;
  }>;
};

export type NutritionLog = TimestampFields & {
  id: number;
  profile_id: number;
  date: IsoDate;
  meal_type: string;
  food_name: string;
  quantity: string;
  serving_count: number;
  calories: number;
  protein: number;
  carbs: number;
  fats: number;
  fiber: number;
  notes: string;
  source_type: string;
  recipe_name: string;
};

export type NutritionDailySummaryResponse = {
  date: IsoDate;
  totals: NutritionTotals;
  remaining: NutritionTotals;
  targets: DailyTarget;
  meals: NutritionLog[];
  compliance_inputs: Record<string, boolean>;
};

export type NutritionLogCreateRequest = {
  date: IsoDate;
  meal_type: string;
  food_name: string;
  quantity?: string;
  serving_count?: number;
  calories?: number;
  protein?: number;
  carbs?: number;
  fats?: number;
  fiber?: number;
  notes?: string;
  source_type?: string;
  recipe_name?: string;
};

export type NutritionLogUpdateRequest = Partial<Omit<NutritionLogCreateRequest, "date">>;

export type NutritionMealAnalysisRequest = {
  meal_type: string;
  meal_description: string;
};

export type NutritionMealAnalysisResult = {
  meal_type: string;
  food_name: string;
  quantity: string;
  calories: number;
  protein: number;
  carbs: number;
  fats: number;
  fiber: number;
  notes: string;
  assumptions: string[];
  source_type: string;
};

export type HydrationLog = TimestampFields & {
  id: number;
  profile_id: number;
  date: IsoDate;
  amount_ml: number;
};

export type HydrationDailySummaryResponse = {
  date: IsoDate;
  total_ml: number;
  target_ml: number;
  target_liters: number;
  remaining_ml: number;
  bottle_count: number;
  progress_pct: number;
  logs: HydrationLog[];
};

export type HydrationChartPoint = {
  date: IsoDate;
  total_ml: number;
  target_ml: number;
  adherence_pct: number;
};

export type HydrationLogCreateRequest = {
  date: IsoDate;
  amount_ml: number;
};

export type BodyMetric = TimestampFields & {
  id: number;
  profile_id: number;
  date: IsoDate;
  body_weight: number | null;
  waist: number | null;
  chest: number | null;
  arms: number | null;
  thigh: number | null;
  body_fat_percent: number | null;
  notes: string;
  hips: number | null;
  neck: number | null;
  thighs: number | null;
  progress_notes: string;
};

export type BodyMetricCreateRequest = {
  date: IsoDate;
  body_weight?: number | null;
  waist?: number | null;
  chest?: number | null;
  arms?: number | null;
  thigh?: number | null;
  body_fat_percent?: number | null;
  notes?: string;
  hips?: number | null;
  neck?: number | null;
  thighs?: number | null;
  progress_notes?: string;
};

export type BodyMetricUpdateRequest = Partial<BodyMetricCreateRequest>;

export type CardioLog = TimestampFields & {
  id: number;
  profile_id: number;
  date: IsoDate;
  cardio_type: string;
  duration_min: number;
  calories: number | null;
  intensity: string | null;
  notes: string;
  is_outdoor: boolean;
  distance_km: number;
  pace_text: string;
  estimated_calories_burned: number;
};

export type CardioLogCreateRequest = {
  date: IsoDate;
  cardio_type: string;
  duration_min: number;
  calories?: number | null;
  intensity?: string | null;
  notes?: string;
  is_outdoor?: boolean;
  distance_km?: number;
  pace_text?: string;
  estimated_calories_burned?: number | null;
};

export type ProgressPhoto = TimestampFields & {
  id: number;
  profile_id: number;
  date: IsoDate;
  photo_type: string;
  file_url: string;
  blob_key: string | null;
  notes: string;
};

export type ProgressPhotoCreateRequest = {
  date: IsoDate;
  photo_type: string;
  file_url: string;
  blob_key?: string | null;
  notes?: string;
};

export type WeeklyReviewSummaryResponse = {
  week_start: IsoDate;
  week_end: IsoDate;
  avg_calories: number;
  avg_protein: number;
  water_adherence_pct: number;
  workout_consistency: number;
  outdoor_workout_consistency: number;
  weight_change: number;
  waist_change: number;
  perfect_days: number;
  incomplete_days: number;
  failed_days: number;
  prs: number;
  total_workout_volume: number;
  cardio_minutes: number;
  nutrition_chart: Array<Record<string, unknown>>;
  hydration_chart: Array<Record<string, unknown>>;
  challenge_chart: Array<Record<string, unknown>>;
};

export type WeeklyReviewRecord = TimestampFields & {
  id: number;
  profile_id: number;
  week_start: IsoDate;
  what_went_well: string;
  what_was_difficult: string;
  focus_for_next_week: string;
  notes: string;
};

export type WeeklyReviewUpsertRequest = {
  week_start: IsoDate;
  what_went_well?: string;
  what_was_difficult?: string;
  focus_for_next_week?: string;
  notes?: string;
};

export type ProfileWithSummary = {
  profile: {
    id: number;
    age: number | null;
    gender: string | null;
    height_cm: number | null;
    current_weight_kg: number | null;
    activity_level: string | null;
    goal: string | null;
    desired_deficit: number | null;
    challenge_start_date: IsoDate | null;
    target_weight_kg: number | null;
    preferred_diet_plan_name: string | null;
    created_at: IsoDateTime;
    updated_at: IsoDateTime;
  };
  summary: {
    bmr: number;
    tdee: number;
    target_calories: number;
    protein_target: number;
  };
};

export type Recipe = TimestampFields & {
  id: number;
  recipe_name: string;
  meal_type: string;
  ingredients_json: Array<Record<string, unknown>>;
  steps_json: string[];
  calories: number;
  protein: number;
  carbs: number;
  fats: number;
  fiber: number;
  portion_note: string;
  is_spicy: boolean;
  is_vegetarian: boolean;
  is_egg_based: boolean;
  is_soya_based: boolean;
};

export type MealPlanTemplate = TimestampFields & {
  id: number;
  day_name: string;
  meal_type: string;
  option_1: string | null;
  option_2: string | null;
  option_3: string | null;
  option_4: string | null;
  notes: string;
};
