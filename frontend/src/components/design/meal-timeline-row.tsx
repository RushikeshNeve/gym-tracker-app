import { Clock3, PencilLine } from "lucide-react";

import { StatusChip } from "@/components/design/status-chip";
import { Card, CardContent } from "@/components/ui/card";
import type { MealLogEntry } from "@/types/nutrition";

export function MealTimelineRow({ entry }: { entry: MealLogEntry }) {
  return (
    <Card>
      <CardContent className="flex items-start justify-between gap-4 p-5">
        <div className="flex gap-4">
          <div className="flex size-11 shrink-0 items-center justify-center rounded-[1rem] border border-white/8 bg-white/[0.03]">
            <Clock3 className="size-4 text-secondary" />
          </div>
          <div>
            <div className="flex flex-wrap items-center gap-2">
              <p className="text-sm font-semibold">{entry.title}</p>
              <StatusChip label={entry.mealLabel} tone="secondary" />
            </div>
            <p className="mt-1 text-sm text-muted-foreground">{entry.time}</p>
            <p className="mt-3 text-sm leading-6 text-muted-foreground">{entry.note}</p>
          </div>
        </div>
        <div className="text-right">
          <p className="text-sm font-semibold">{entry.calories} kcal</p>
          <p className="mt-1 text-sm text-muted-foreground">{entry.protein}g protein</p>
          <div className="mt-4 inline-flex items-center gap-2 rounded-full border border-white/8 px-3 py-1 text-xs uppercase tracking-[0.16em] text-muted-foreground">
            <PencilLine className="size-4" />
            editable
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
