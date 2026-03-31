import { Plus } from "lucide-react";

import { StatusChip } from "@/components/design/status-chip";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import type { QuickAddNutritionItem as QuickAddNutritionItemType } from "@/types/nutrition";

export function QuickAddNutritionItem({
  item,
  onAdd,
  disabled,
}: {
  item: QuickAddNutritionItemType;
  onAdd?: () => void;
  disabled?: boolean;
}) {
  return (
    <Card>
      <CardContent className="p-5">
        <div className="flex items-start justify-between gap-3">
          <div>
            <p className="text-sm font-semibold">{item.title}</p>
            <p className="mt-2 text-sm leading-6 text-muted-foreground">{item.description}</p>
          </div>
          <Button disabled={disabled} onClick={onAdd} size="icon" variant="outline">
            <Plus className="size-4" />
          </Button>
        </div>
        <div className="mt-4 flex flex-wrap gap-2">
          <StatusChip label={item.mealType.replaceAll("_", " ")} tone="secondary" />
          {item.tags.map((tag) => (
            <StatusChip key={tag} label={tag} tone={tag === "spicy" ? "warning" : "neutral"} />
          ))}
        </div>
        <div className="mt-4 grid grid-cols-2 gap-2 text-sm">
          <div className="rounded-[1rem] border border-white/6 bg-black/10 px-3 py-2">{item.macros.calories} kcal</div>
          <div className="rounded-[1rem] border border-white/6 bg-black/10 px-3 py-2">{item.macros.protein}g protein</div>
        </div>
      </CardContent>
    </Card>
  );
}
