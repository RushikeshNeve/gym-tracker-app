import { ChefHat, Flame, ListChecks } from "lucide-react";

import { StatusChip } from "@/components/design/status-chip";
import { SectionCard } from "@/components/design/section-card";
import type { RecipeDetail } from "@/types/nutrition";

export function RecipeCard({ recipe }: { recipe: RecipeDetail }) {
  return (
    <SectionCard
      title={recipe.title}
      description={recipe.description}
      action={<StatusChip label={`${recipe.macros.calories} kcal`} tone="secondary" />}
      className="h-full"
    >
      <div className="space-y-5">
        <div className="flex flex-wrap gap-2">
          {recipe.tags.map((tag) => (
            <StatusChip key={tag} label={tag} tone={tag === "spicy" ? "warning" : "neutral"} />
          ))}
        </div>

        <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-5">
          <MacroTile label="Protein" value={`${recipe.macros.protein}g`} />
          <MacroTile label="Carbs" value={`${recipe.macros.carbs}g`} />
          <MacroTile label="Fats" value={`${recipe.macros.fats}g`} />
          <MacroTile label="Fiber" value={`${recipe.macros.fiber}g`} />
          <MacroTile label="Portion" value={recipe.portionNote} long />
        </div>

        <div className="grid gap-4 xl:grid-cols-2">
          <div className="rounded-[1.4rem] border border-white/6 bg-white/[0.03] p-5">
            <div className="flex items-center gap-2 text-sm font-semibold">
              <ChefHat className="size-4 text-primary" />
              Ingredients
            </div>
            <ul className="mt-4 space-y-3 text-sm text-muted-foreground">
              {recipe.ingredients.map((ingredient) => (
                <li className="rounded-[1rem] border border-white/6 bg-black/10 px-3 py-2" key={ingredient}>
                  {ingredient}
                </li>
              ))}
            </ul>
          </div>

          <div className="rounded-[1.4rem] border border-white/6 bg-white/[0.03] p-5">
            <div className="flex items-center gap-2 text-sm font-semibold">
              <ListChecks className="size-4 text-secondary" />
              Cooking steps
            </div>
            <ol className="mt-4 space-y-3">
              {recipe.steps.map((step, index) => (
                <li className="flex gap-3 rounded-[1rem] border border-white/6 bg-black/10 px-3 py-3 text-sm text-muted-foreground" key={step}>
                  <span className="flex size-6 shrink-0 items-center justify-center rounded-full bg-secondary/12 text-xs font-semibold text-secondary">
                    {index + 1}
                  </span>
                  <span className="leading-6">{step}</span>
                </li>
              ))}
            </ol>
          </div>
        </div>

        <div className="flex items-center gap-2 rounded-[1.3rem] border border-primary/12 bg-primary/6 px-4 py-3 text-sm text-foreground">
          <Flame className="size-4 text-primary" />
          Recipe macros are pre-balanced so you can swap options without breaking the day.
        </div>
      </div>
    </SectionCard>
  );
}

function MacroTile({ label, value, long }: { label: string; value: string; long?: boolean }) {
  return (
    <div className="rounded-[1.25rem] border border-white/6 bg-white/[0.03] p-4">
      <p className="text-[0.68rem] uppercase tracking-[0.18em] text-muted-foreground">{label}</p>
      <p className={long ? "mt-2 text-sm leading-6 text-foreground" : "mt-2 text-xl font-bold"}>{value}</p>
    </div>
  );
}
