import { useMemo, useState } from "react";
import { ArrowRight, Salad, Sparkles } from "lucide-react";

import { EnergyBalanceCard } from "@/components/design/energy-balance-card";
import { ErrorState } from "@/components/design/error-state";
import { LoadingShell } from "@/components/design/loading-shell";
import { MacroProgressGroup } from "@/components/design/macro-progress-group";
import { MealTimelineRow } from "@/components/design/meal-timeline-row";
import { QuickAddNutritionItem } from "@/components/design/quick-add-nutrition-item";
import { RecipeCard } from "@/components/design/recipe-card";
import { SectionCard } from "@/components/design/section-card";
import { StatusChip } from "@/components/design/status-chip";
import { PageHeader } from "@/components/layout/page-header";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useAnalyzeNutritionMeal, useNutritionPage, useQuickAddNutritionLog } from "@/hooks/use-nutrition-page";
import { getTodayDateString } from "@/lib/date";
import type { NutritionAnalysisCard } from "@/types/nutrition";

export function NutritionPage() {
  const { data, isLoading, isError, refetch } = useNutritionPage();
  const addNutrition = useQuickAddNutritionLog();
  const analyzeNutrition = useAnalyzeNutritionMeal();
  const [selectedByMeal, setSelectedByMeal] = useState<Record<string, string>>({});
  const [activeRecipeId, setActiveRecipeId] = useState<string | null>(null);
  const [activeMealId, setActiveMealId] = useState<string | null>(null);
  const [planLocked, setPlanLocked] = useState(false);
  const [manualMealType, setManualMealType] = useState("dinner");
  const [manualMealText, setManualMealText] = useState("");
  const [analyzedMeal, setAnalyzedMeal] = useState<NutritionAnalysisCard | null>(null);

  const resolvedPlan = useMemo(() => {
    if (!data) {
      return [];
    }

    return data.mealPlan.map((meal) => ({
      ...meal,
      selectedOptionId: selectedByMeal[meal.id] ?? meal.selectedOptionId,
    }));
  }, [data, selectedByMeal]);

  const selectedRecipe = useMemo(() => {
    if (!data) {
      return null;
    }

    if (activeRecipeId && data.recipes[activeRecipeId]) {
      return data.recipes[activeRecipeId];
    }

    const firstSelectedOption = resolvedPlan[0]?.options.find((option) => option.id === resolvedPlan[0]?.selectedOptionId);
    if (firstSelectedOption) {
      return data.recipes[firstSelectedOption.recipeId];
    }

    return null;
  }, [activeRecipeId, data, resolvedPlan]);

  if (isLoading) return <LoadingShell />;
  if (isError || !data || !selectedRecipe) return <ErrorState title="Nutrition could not load" description="Meal plans or nutrition totals did not arrive from the API." onRetry={() => void refetch()} />;
  const nutritionData = data;
  const activeMeal = resolvedPlan.find((meal) => meal.id === activeMealId) ?? resolvedPlan[0];
  const activeMealOption = activeMeal?.options.find((option) => option.id === activeMeal.selectedOptionId) ?? activeMeal?.options[0] ?? null;

  function logSelectedMeal(mealId: string) {
    const meal = resolvedPlan.find((entry) => entry.id === mealId);
    if (!meal) return;

    const selectedOption = meal.options.find((option) => option.id === meal.selectedOptionId) ?? meal.options[0];
    if (!selectedOption) return;

    const recipe = nutritionData.recipes[selectedOption.recipeId];
    if (!recipe) return;

    addNutrition.mutate({
      date: getTodayDateString(),
      meal_type: meal.name,
      food_name: recipe.title,
      quantity: recipe.portionNote || "1 serving",
      serving_count: 1,
      calories: recipe.macros.calories,
      protein: recipe.macros.protein,
      carbs: recipe.macros.carbs,
      fats: recipe.macros.fats,
      fiber: recipe.macros.fiber,
      source_type: "recipe",
      recipe_name: recipe.title,
    });
  }

  function quickLogItem(itemId: string) {
    const item = nutritionData.quickAdds.find((entry) => entry.id === itemId);
    if (!item) return;

    addNutrition.mutate({
      date: getTodayDateString(),
      meal_type: item.mealType,
      food_name: item.title,
      quantity: item.quantity || "1 serving",
      serving_count: 1,
      calories: item.macros.calories,
      protein: item.macros.protein,
      carbs: item.macros.carbs,
      fats: item.macros.fats,
      fiber: item.macros.fiber,
      source_type: item.sourceType || "manual",
      recipe_name: item.sourceType === "recipe" ? item.title : undefined,
    });
  }

  function analyzeManualMeal() {
    const trimmed = manualMealText.trim();
    if (!trimmed) return;

    analyzeNutrition.mutate(
      {
        meal_type: manualMealType,
        meal_description: trimmed,
      },
      {
        onSuccess: (result) => {
          setAnalyzedMeal(result);
        },
      },
    );
  }

  function saveAnalyzedMeal() {
    if (!analyzedMeal) return;

    addNutrition.mutate({
      date: getTodayDateString(),
      meal_type: analyzedMeal.mealType,
      food_name: analyzedMeal.title,
      quantity: analyzedMeal.quantity,
      serving_count: 1,
      calories: analyzedMeal.macros.calories,
      protein: analyzedMeal.macros.protein,
      carbs: analyzedMeal.macros.carbs,
      fats: analyzedMeal.macros.fats,
      fiber: analyzedMeal.macros.fiber,
      notes: analyzedMeal.notes,
      source_type: analyzedMeal.sourceType,
    });
  }

  return (
    <div className="space-y-6">
      <section className="overflow-hidden rounded-[2.2rem] border border-white/6 bg-[linear-gradient(135deg,rgba(151,255,147,0.12),rgba(25,168,255,0.14)_38%,rgba(10,12,15,0.98)_74%)] p-6 shadow-[0_20px_64px_rgba(0,0,0,0.38)] sm:p-8">
        <PageHeader
          eyebrow={nutritionData.heroLabel}
          title={nutritionData.heroTitle}
          description={nutritionData.heroDescription}
          chips={[
            { label: `${nutritionData.summary.remainingCalories} kcal remaining`, tone: "success" },
            { label: `${nutritionData.summary.remainingProtein}g protein left`, tone: "secondary" },
            { label: "Meal plan live", tone: "warning" },
          ]}
          actions={
            <div className="min-w-72 rounded-[1.5rem] border border-white/8 bg-black/20 px-5 py-4">
              <p className="text-[0.68rem] font-semibold uppercase tracking-[0.2em] text-muted-foreground">Today intake summary</p>
              <div className="mt-4 grid gap-3 sm:grid-cols-2">
                <SummaryPill label="Calories" value={`${nutritionData.summary.caloriesConsumed} / ${nutritionData.summary.caloriesTarget}`} />
                <SummaryPill label="Protein" value={`${nutritionData.summary.proteinConsumed}g / ${nutritionData.summary.proteinTarget}g`} />
                <SummaryPill label="Remaining kcal" value={`${nutritionData.summary.remainingCalories}`} />
                <SummaryPill label="Remaining protein" value={`${nutritionData.summary.remainingProtein}g`} />
              </div>
            </div>
          }
        />
      </section>

      <div className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <div className="space-y-6">
          <SectionCard
            title="Today's meal plan"
            description="Choose from a fixed list for each meal type, then log the exact option you actually ate."
            action={<StatusChip label={`${resolvedPlan.length} meal blocks`} tone="secondary" />}
          >
            <div className="space-y-5">
              {resolvedPlan.map((meal) => (
                <div
                  className={`rounded-[1.7rem] border p-4 transition sm:p-5 ${
                    activeMeal?.id === meal.id
                      ? "border-primary/20 bg-[linear-gradient(180deg,rgba(151,255,147,0.08),rgba(17,18,22,0.96))] shadow-[0_18px_40px_rgba(0,0,0,0.2)]"
                      : "border-white/6 bg-white/[0.03]"
                  }`}
                  key={meal.id}
                >
                  <div className="rounded-[1.35rem] border border-white/6 bg-black/10 p-4">
                    <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
                      <div className="flex flex-wrap items-start justify-between gap-3">
                        <div>
                          <p className="text-[0.68rem] font-semibold uppercase tracking-[0.18em] text-muted-foreground">{meal.timing}</p>
                          <h3 className="mt-2 text-xl font-semibold">{formatMealLabel(meal.name)}</h3>
                        </div>
                        <div className="flex flex-wrap gap-2">
                          <StatusChip label={`${meal.options.length} options`} tone="neutral" />
                          {activeMeal?.id === meal.id ? <StatusChip label="Open" tone="success" /> : null}
                        </div>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        <Button
                          className="min-w-32"
                          onClick={() => {
                            setActiveMealId(meal.id);
                            const selected = meal.options.find((option) => option.id === meal.selectedOptionId) ?? meal.options[0];
                            if (selected) {
                              setActiveRecipeId(selected.recipeId);
                            }
                          }}
                          variant={activeMeal?.id === meal.id ? "default" : "outline"}
                        >
                          {activeMeal?.id === meal.id ? "Viewing meal" : "Open meal"}
                        </Button>
                        <Button
                          className="min-w-36"
                          disabled={addNutrition.isPending || !meal.selectedOptionId}
                          onClick={() => logSelectedMeal(meal.id)}
                          variant="outline"
                        >
                          Log selected meal
                        </Button>
                      </div>
                    </div>

                    <div className="mt-4 grid gap-4 lg:grid-cols-[1fr_auto] lg:items-center">
                      <div>
                        <p className="text-sm leading-6 text-muted-foreground">
                          {meal.name === "pre_workout"
                            ? "Fast fuel and supplements before training."
                            : meal.name === "breakfast"
                              ? "Start recovery with an easy protein-forward breakfast."
                              : "Keep one decisive choice in front of you and log it cleanly."}
                        </p>
                        <div className="mt-3 space-y-2">
                          <p className="text-[0.68rem] uppercase tracking-[0.18em] text-muted-foreground">Selected option</p>
                          <p className="text-base font-semibold">{meal.options.find((option) => option.id === meal.selectedOptionId)?.title ?? "Choose an option"}</p>
                        </div>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {meal.name === "pre_workout" ? (
                          <Button disabled={addNutrition.isPending} onClick={() => quickLogItem("manual-creatine")} size="sm" variant="ghost">
                            Add creatine
                          </Button>
                        ) : null}
                        {meal.name === "breakfast" ? (
                          <>
                            <Button disabled={addNutrition.isPending} onClick={() => quickLogItem("manual-oatmeal")} size="sm" variant="ghost">
                              Add oatmeal
                            </Button>
                            <Button disabled={addNutrition.isPending} onClick={() => quickLogItem("manual-whey")} size="sm" variant="ghost">
                              Add whey
                            </Button>
                          </>
                        ) : null}
                      </div>
                    </div>

                    {activeMeal?.id === meal.id ? (
                      <div className="mt-5 space-y-3">
                        {meal.options.map((option) => (
                          <button
                            className={`flex w-full items-center justify-between rounded-[1.15rem] border px-4 py-4 text-left transition ${
                              option.id === meal.selectedOptionId
                                ? "border-primary/25 bg-primary/10"
                                : "border-white/6 bg-white/[0.03] hover:border-white/12"
                            }`}
                            key={option.id}
                            onClick={() => {
                              setSelectedByMeal((current) => ({ ...current, [meal.id]: option.id }));
                              setActiveMealId(meal.id);
                              setActiveRecipeId(option.recipeId);
                            }}
                            type="button"
                          >
                            <div>
                              <p className="text-sm font-semibold">{option.title}</p>
                              <p className="mt-1 text-sm text-muted-foreground">{option.subtitle}</p>
                              <div className="mt-2 flex flex-wrap gap-2">
                                <StatusChip label={`${Math.round(option.macros.calories)} kcal`} tone="neutral" />
                                <StatusChip label={`${Math.round(option.macros.protein)} g protein`} tone="secondary" />
                              </div>
                            </div>
                            <StatusChip label={option.id === meal.selectedOptionId ? "Selected" : "Choose"} tone={option.id === meal.selectedOptionId ? "success" : "neutral"} />
                          </button>
                        ))}
                      </div>
                    ) : null}
                  </div>
                </div>
              ))}
            </div>
          </SectionCard>

          <div className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
            <SectionCard
              title="Describe a custom meal"
              description="When you eat something outside the fixed list, describe it here and let OpenAI estimate the calories and macros."
              action={<StatusChip label="OpenAI estimate" tone="warning" />}
            >
              <div className="space-y-4">
                <label className="block">
                  <p className="text-[0.68rem] uppercase tracking-[0.18em] text-muted-foreground">Meal type</p>
                  <select
                    className="mt-3 h-11 w-full rounded-[0.95rem] border border-white/8 bg-white/[0.04] px-3 text-sm font-semibold text-foreground outline-none transition focus:border-primary/45 focus:ring-2 focus:ring-primary/20"
                    onChange={(event) => setManualMealType(event.target.value)}
                    value={manualMealType}
                  >
                    {resolvedPlan.map((meal) => (
                      <option className="bg-[#121212] text-foreground" key={meal.id} value={meal.name}>
                        {formatMealLabel(meal.name)}
                      </option>
                    ))}
                  </select>
                </label>

                <Textarea
                  onChange={(event) => setManualMealText(event.target.value)}
                  placeholder="Example: 2 chapatis, 1 bowl paneer bhurji, half cup curd, 1 tsp ghee"
                  value={manualMealText}
                />

                <div className="flex flex-col gap-3 sm:flex-row">
                  <Button className="sm:flex-1" disabled={analyzeNutrition.isPending || !manualMealText.trim()} onClick={analyzeManualMeal}>
                    {analyzeNutrition.isPending ? "Analyzing..." : "Analyze meal with AI"}
                  </Button>
                  <Button className="sm:flex-1" disabled={addNutrition.isPending || !analyzedMeal} onClick={saveAnalyzedMeal} variant="outline">
                    {addNutrition.isPending ? "Saving..." : "Save analyzed meal"}
                  </Button>
                </div>

                {analyzeNutrition.isError ? (
                  <div className="rounded-[1.15rem] border border-white/6 bg-white/[0.03] px-4 py-3">
                    <StatusChip label="AI unavailable" tone="warning" />
                    <p className="mt-2 text-sm leading-6 text-muted-foreground">{analyzeNutrition.error.message}</p>
                  </div>
                ) : null}

                {analyzedMeal ? (
                  <div className="rounded-[1.35rem] border border-white/6 bg-[linear-gradient(180deg,rgba(25,168,255,0.08),rgba(16,18,22,0.96))] p-4">
                    <div className="flex flex-wrap items-center gap-2">
                      <p className="text-base font-semibold">{analyzedMeal.title}</p>
                      <StatusChip label={formatMealLabel(analyzedMeal.mealType)} tone="secondary" />
                    </div>
                    <p className="mt-2 text-sm leading-6 text-muted-foreground">{analyzedMeal.quantity}</p>
                    <div className="mt-4 grid gap-3 sm:grid-cols-2">
                      <SummaryPill label="Calories" value={`${Math.round(analyzedMeal.macros.calories)} kcal`} />
                      <SummaryPill label="Protein" value={`${Math.round(analyzedMeal.macros.protein)} g`} />
                      <SummaryPill label="Carbs" value={`${Math.round(analyzedMeal.macros.carbs)} g`} />
                      <SummaryPill label="Fats" value={`${Math.round(analyzedMeal.macros.fats)} g`} />
                    </div>
                    {analyzedMeal.notes ? <p className="mt-4 text-sm leading-6 text-muted-foreground">{analyzedMeal.notes}</p> : null}
                    {analyzedMeal.assumptions.length ? (
                      <div className="mt-4 space-y-2">
                        <p className="text-[0.68rem] uppercase tracking-[0.18em] text-muted-foreground">Assumptions</p>
                        {analyzedMeal.assumptions.map((assumption) => (
                          <p className="text-sm leading-6 text-muted-foreground" key={assumption}>
                            {assumption}
                          </p>
                        ))}
                      </div>
                    ) : null}
                  </div>
                ) : null}
              </div>
            </SectionCard>

            <SectionCard
              title="Quick-add fuel"
              description="Fast additions when the day is moving and you still need clean nutrition control."
              action={<StatusChip label="One-click items" tone="warning" />}
            >
              <div className="grid gap-4">
                {nutritionData.quickAdds.map((item) => (
                  <QuickAddNutritionItem
                    disabled={addNutrition.isPending}
                    item={item}
                    key={item.id}
                    onAdd={() => quickLogItem(item.id)}
                  />
                ))}
              </div>
            </SectionCard>

            <SectionCard
              title="Meal log timeline"
              description="A clean view of what has already landed today."
              action={<StatusChip label={`${nutritionData.mealLog.length} entries`} tone="success" />}
            >
              <div className="space-y-3">
                {nutritionData.mealLog.map((entry) => (
                  <MealTimelineRow entry={entry} key={entry.id} />
                ))}
              </div>
            </SectionCard>
          </div>
        </div>

        <div className="space-y-6 xl:sticky xl:top-24 self-start">
          <SectionCard
            title="Selected meal detail"
            description="The recipe panel follows the meal option you click, so you never lose context while logging."
            action={activeMeal ? <StatusChip label={formatMealLabel(activeMeal.name)} tone="secondary" /> : null}
          >
            <div className="rounded-[1.5rem] border border-white/6 bg-[linear-gradient(180deg,rgba(25,168,255,0.08),rgba(16,18,22,0.96))] p-5">
              <p className="text-[0.68rem] uppercase tracking-[0.18em] text-muted-foreground">Current focus</p>
              <p className="mt-3 text-xl font-semibold">{activeMealOption?.title ?? selectedRecipe.title}</p>
              <div className="mt-4 flex flex-wrap gap-2">
                {activeMealOption?.tags.map((tag) => (
                  <StatusChip key={tag} label={tag} tone={tag === "spicy" ? "warning" : "neutral"} />
                ))}
              </div>
              <div className="mt-5 grid grid-cols-2 gap-3">
                <SummaryPill label="Calories" value={`${(activeMealOption?.macros.calories ?? selectedRecipe.macros.calories).toFixed?.(0) ?? activeMealOption?.macros.calories} kcal`} />
                <SummaryPill label="Protein" value={`${activeMealOption?.macros.protein ?? selectedRecipe.macros.protein} g`} />
              </div>
            </div>
          </SectionCard>

          <RecipeCard recipe={selectedRecipe} />

          <SectionCard
            title="Macro progress"
            description="Your nutrition targets for the day, reduced to a fast visual read."
            action={<StatusChip label="Target aware" tone="success" />}
          >
            <MacroProgressGroup items={nutritionData.summary.macroProgress} />
          </SectionCard>

          <EnergyBalanceCard balance={nutritionData.energyBalance} />

          <SectionCard title="Execution note" description="Keep the plan easy to follow when fatigue creeps in.">
            <div className="rounded-[1.4rem] border border-white/6 bg-[linear-gradient(180deg,rgba(25,168,255,0.10),rgba(16,18,22,0.96))] p-5">
              <div className="flex items-start gap-3">
                <div className="rounded-[1rem] bg-secondary/10 p-3 text-secondary">
                  <Sparkles className="size-5" />
                </div>
                <div>
                  <p className="text-lg font-semibold">The easiest clean close is already in front of you.</p>
                  <p className="mt-3 text-sm leading-6 text-muted-foreground">
                    If protein slips late, use whey. If hunger spikes, choose the spicy snack card. If calories are tight, keep dinner lean and stop browsing for variety.
                  </p>
                  <Button
                    className="mt-4"
                    onClick={() => {
                      const dinner = resolvedPlan.find((meal) => meal.name.toLowerCase() === "dinner");
                      const dinnerOption = dinner?.options.find((option) => option.id === dinner.selectedOptionId);
                      if (dinnerOption) {
                        setActiveRecipeId(dinnerOption.recipeId);
                      }
                      setPlanLocked(true);
                    }}
                    variant="outline"
                  >
                    <Salad className="size-4 text-primary" />
                    {planLocked ? "Tonight's plan locked" : "Lock tonight's plan"}
                    <ArrowRight className="size-4" />
                  </Button>
                </div>
              </div>
            </div>
          </SectionCard>
        </div>
      </div>
    </div>
  );
}

function formatMealLabel(value: string) {
  return value.replaceAll("_", " ").replace(/\b\w/g, (match) => match.toUpperCase());
}

function SummaryPill({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-[1rem] border border-white/6 bg-white/[0.04] px-3 py-3">
      <p className="text-xs uppercase tracking-[0.16em] text-muted-foreground">{label}</p>
      <p className="mt-2 text-lg font-semibold">{value}</p>
    </div>
  );
}
