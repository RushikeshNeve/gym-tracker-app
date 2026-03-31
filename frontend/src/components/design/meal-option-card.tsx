import { CheckCircle2 } from "lucide-react";

import { StatusChip } from "@/components/design/status-chip";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import type { MealOption } from "@/types/nutrition";

export function MealOptionCard({
  option,
  selected,
  onSelect,
}: {
  option: MealOption;
  selected: boolean;
  onSelect: () => void;
}) {
  return (
    <Card
      className={cn(
        "overflow-hidden transition-all duration-200",
        selected && "ring-1 ring-primary/18 bg-[linear-gradient(180deg,rgba(151,255,147,0.12),rgba(18,20,24,0.96))]",
      )}
    >
      <CardContent className="p-5">
        <div className="flex items-start justify-between gap-4">
          <div>
            <p className="text-sm font-semibold">{option.title}</p>
            <p className="mt-2 text-sm leading-6 text-muted-foreground">{option.subtitle}</p>
          </div>
          {selected ? <CheckCircle2 className="size-5 shrink-0 text-primary" /> : null}
        </div>
        <div className="mt-4 flex flex-wrap gap-2">
          {option.tags.map((tag) => (
            <StatusChip key={tag} label={tag} tone={tag === "spicy" ? "warning" : "neutral"} />
          ))}
        </div>
        <div className="mt-4 grid grid-cols-4 gap-2 text-center text-xs text-muted-foreground">
          <Metric value={option.macros.calories} label="kcal" />
          <Metric value={`${option.macros.protein}g`} label="protein" />
          <Metric value={`${option.macros.carbs}g`} label="carbs" />
          <Metric value={`${option.macros.fats}g`} label="fats" />
        </div>
        <Button className="mt-4 w-full" onClick={onSelect} variant={selected ? "default" : "outline"}>
          {selected ? "Selected option" : "Choose this option"}
        </Button>
      </CardContent>
    </Card>
  );
}

function Metric({ value, label }: { value: string | number; label: string }) {
  return (
    <div className="rounded-[1rem] border border-white/6 bg-black/10 px-2 py-3">
      <div className="font-semibold text-foreground">{value}</div>
      {label}
    </div>
  );
}
