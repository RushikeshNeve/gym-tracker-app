import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { api } from "@/lib/api/services";
import { formatWeekday, getTodayDateString } from "@/lib/date";
import type { NutritionLogCreateRequest, NutritionMealAnalysisRequest, Recipe } from "@/types/api";
import type { NutritionAnalysisCard, NutritionPageData } from "@/types/nutrition";

function recipeTags(recipe: Recipe) {
  return [
    recipe.is_spicy ? "spicy" : null,
    recipe.is_vegetarian ? "vegetarian" : null,
    recipe.is_egg_based ? "egg" : null,
    recipe.is_soya_based ? "soya" : null,
  ].filter(Boolean) as string[];
}

function ingredientToText(value: Record<string, unknown>) {
  const parts = Object.values(value).filter(Boolean);
  return parts.length ? parts.join(" ") : JSON.stringify(value);
}

export function useNutritionPage() {
  const todayDate = getTodayDateString();
  return useQuery<NutritionPageData>({
    queryKey: ["nutrition-page", todayDate],
    queryFn: async () => {
      const [daily, recipes, mealPlans, today] = await Promise.all([
        api.nutrition.daily(todayDate),
        api.recipes.list(),
        api.mealPlans.get(todayDate),
        api.today.get(),
      ]);

      const recipeMap = Object.fromEntries(
        recipes.map((recipe) => [
          recipe.recipe_name.toLowerCase(),
          recipe,
        ]),
      );

      const meals = mealPlans.map((plan) => {
        const optionNames = [plan.option_1, plan.option_2, plan.option_3, plan.option_4].filter(Boolean) as string[];
        const options = optionNames
          .map((name) => recipeMap[name.toLowerCase()])
          .filter(Boolean)
          .map((recipe) => ({
            id: `${plan.id}-${recipe.id}`,
            title: recipe.recipe_name,
            subtitle: plan.notes || `Plan option for ${plan.meal_type}.`,
            recipeId: String(recipe.id),
            macros: {
              calories: recipe.calories,
              protein: recipe.protein,
              carbs: recipe.carbs,
              fats: recipe.fats,
              fiber: recipe.fiber,
            },
            tags: recipeTags(recipe),
          }));

        const breakfastDefault = options.find((option) => option.title.toLowerCase().includes("oats") && option.title.toLowerCase().includes("whey"));

        return {
          id: `${plan.id}`,
          name: plan.meal_type,
          timing: plan.day_name,
          options,
          selectedOptionId: breakfastDefault?.id ?? options[0]?.id ?? "",
        };
      });

      const recipesById = Object.fromEntries(
        recipes.map((recipe) => [
          String(recipe.id),
          {
            id: String(recipe.id),
            title: recipe.recipe_name,
            description: `${recipe.meal_type} option from the backend recipe library.`,
            ingredients: recipe.ingredients_json.map((item) => ingredientToText(item)),
            steps: recipe.steps_json,
            macros: {
              calories: recipe.calories,
              protein: recipe.protein,
              carbs: recipe.carbs,
              fats: recipe.fats,
              fiber: recipe.fiber,
            },
            portionNote: recipe.portion_note,
            tags: recipeTags(recipe),
          },
        ]),
      );

      const quickAddRecipes = recipes.filter((recipe) => recipe.recipe_name.toLowerCase().includes("whey") || recipe.is_spicy).slice(0, 3);
      const manualQuickAdds = [
        {
          id: "manual-creatine",
          title: "Creatine 5 g",
          description: "Pre-workout add-on for your daily creatine dose.",
          mealType: "pre_workout",
          quantity: "5 g in water",
          sourceType: "manual",
          macros: { calories: 0, protein: 0, carbs: 0, fats: 0, fiber: 0 },
          tags: ["pre-workout"],
        },
        {
          id: "manual-oatmeal",
          title: "Oatmeal 40 g",
          description: "Easy breakfast carb add-on when you want a stable base.",
          mealType: "breakfast",
          quantity: "40 g dry oats",
          sourceType: "manual",
          macros: { calories: 154, protein: 5, carbs: 27, fats: 3, fiber: 4 },
          tags: ["breakfast"],
        },
        {
          id: "manual-whey",
          title: "Beast Life Whey",
          description: "Protein add-on that stays available for breakfast every day.",
          mealType: "breakfast",
          quantity: "1 scoop",
          sourceType: "manual",
          macros: { calories: 120, protein: 24, carbs: 3, fats: 2, fiber: 0 },
          tags: ["breakfast", "protein"],
        },
      ];

      return {
        heroLabel: "Fuel with intent",
        heroTitle: "Nutrition",
        heroDescription: "Meals, targets, and energy balance are now coming from the backend plan instead of local mock data.",
        mealPlan: meals,
        recipes: recipesById,
        quickAdds: [
          ...manualQuickAdds,
          ...quickAddRecipes.map((recipe) => ({
            id: String(recipe.id),
            title: recipe.recipe_name,
            description: `${recipe.meal_type} quick-add from the recipe library.`,
            mealType: recipe.meal_type,
            quantity: recipe.portion_note,
            sourceType: "recipe",
            macros: {
              calories: recipe.calories,
              protein: recipe.protein,
              carbs: recipe.carbs,
              fats: recipe.fats,
              fiber: recipe.fiber,
            },
            tags: recipeTags(recipe),
          })),
        ],
        summary: {
          caloriesConsumed: daily.totals.calories,
          caloriesTarget: daily.targets.calorie_target,
          proteinConsumed: daily.totals.protein,
          proteinTarget: daily.targets.protein_target,
          remainingCalories: daily.remaining.calories,
          remainingProtein: daily.remaining.protein,
          macroProgress: [
            { label: "Calories", consumed: daily.totals.calories, target: daily.targets.calorie_target, unit: "kcal", tone: "primary" },
            { label: "Protein", consumed: daily.totals.protein, target: daily.targets.protein_target, unit: "g", tone: "secondary" },
            { label: "Carbs", consumed: daily.totals.carbs, target: daily.targets.carbs_target, unit: "g" },
            { label: "Fats", consumed: daily.totals.fats, target: daily.targets.fats_target, unit: "g", tone: "warning" },
            { label: "Fiber", consumed: daily.totals.fiber, target: daily.targets.fiber_target, unit: "g", tone: "secondary" },
          ],
        },
        energyBalance: {
          maintenanceCalories: today.energy_balance.maintenance_calories,
          targetCalories: today.energy_balance.target_calories,
          foodCalories: today.energy_balance.food_calories,
          exerciseCaloriesBurned: today.energy_balance.exercise_calories,
          netCalories: today.energy_balance.net_calories,
          statusLabel: `${today.energy_balance.status.replaceAll("_", " ")} ${Math.round(today.energy_balance.deficit_or_surplus)} kcal`,
          statusTone: today.energy_balance.status === "in_surplus" ? "danger" : today.energy_balance.status === "near_maintenance" ? "warning" : "success",
          description: `Protein logged today: ${today.energy_balance.protein} g.`,
        },
        mealLog: daily.meals.map((meal) => ({
          id: String(meal.id),
          time: formatWeekday(meal.date),
          mealLabel: meal.meal_type,
          title: meal.recipe_name || meal.food_name,
          calories: meal.calories,
          protein: meal.protein,
          note: meal.notes || meal.quantity || meal.source_type,
        })),
      };
    },
  });
}

export function useQuickAddNutritionLog() {
  const queryClient = useQueryClient();
  const todayDate = getTodayDateString();

  return useMutation({
    mutationFn: async (payload: NutritionLogCreateRequest) => api.nutrition.create(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["nutrition-page", todayDate] });
      void queryClient.invalidateQueries({ queryKey: ["today", todayDate] });
      void queryClient.invalidateQueries({ queryKey: ["dashboard"] });
    },
  });
}

export function useAnalyzeNutritionMeal() {
  return useMutation<NutritionAnalysisCard, Error, NutritionMealAnalysisRequest>({
    mutationFn: async (payload) => {
      const result = await api.nutrition.analyze(payload);
      return {
        mealType: result.meal_type,
        title: result.food_name,
        quantity: result.quantity,
        macros: {
          calories: result.calories,
          protein: result.protein,
          carbs: result.carbs,
          fats: result.fats,
          fiber: result.fiber,
        },
        notes: result.notes,
        assumptions: result.assumptions,
        sourceType: result.source_type,
      };
    },
  });
}
