export type RecipeMacro = {
  calories: number;
  protein: number;
  carbs: number;
  fats: number;
  fiber: number;
};

export type RecipeDetail = {
  id: string;
  title: string;
  description: string;
  ingredients: string[];
  steps: string[];
  macros: RecipeMacro;
  portionNote: string;
  tags: string[];
};

export type MealOption = {
  id: string;
  title: string;
  subtitle: string;
  recipeId: string;
  macros: RecipeMacro;
  tags: string[];
};

export type MealPlanMeal = {
  id: string;
  name: string;
  timing: string;
  options: MealOption[];
  selectedOptionId: string;
};

export type MacroProgressItem = {
  label: string;
  consumed: number;
  target: number;
  unit: string;
  tone?: "primary" | "secondary" | "warning";
};

export type NutritionSummary = {
  caloriesConsumed: number;
  caloriesTarget: number;
  proteinConsumed: number;
  proteinTarget: number;
  remainingCalories: number;
  remainingProtein: number;
  macroProgress: MacroProgressItem[];
};

export type EnergyBalance = {
  maintenanceCalories: number;
  targetCalories: number;
  foodCalories: number;
  exerciseCaloriesBurned: number;
  netCalories: number;
  statusLabel: string;
  statusTone: "success" | "warning" | "danger";
  description: string;
};

export type QuickAddNutritionItem = {
  id: string;
  title: string;
  description: string;
  mealType: string;
  quantity?: string;
  sourceType?: string;
  macros: RecipeMacro;
  tags: string[];
};

export type MealLogEntry = {
  id: string;
  time: string;
  mealLabel: string;
  title: string;
  calories: number;
  protein: number;
  note: string;
};

export type NutritionPageData = {
  heroLabel: string;
  heroTitle: string;
  heroDescription: string;
  mealPlan: MealPlanMeal[];
  recipes: Record<string, RecipeDetail>;
  quickAdds: QuickAddNutritionItem[];
  summary: NutritionSummary;
  energyBalance: EnergyBalance;
  mealLog: MealLogEntry[];
};
