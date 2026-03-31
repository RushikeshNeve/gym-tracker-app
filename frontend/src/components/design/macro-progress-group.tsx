import { Progress } from "@/components/ui/progress";
import { cn } from "@/lib/utils";
import type { MacroProgressItem } from "@/types/nutrition";

export function MacroProgressGroup({ items }: { items: MacroProgressItem[] }) {
  return (
    <div className="space-y-4">
      {items.map((item) => {
        const percent = Math.min((item.consumed / item.target) * 100, 100);
        return (
          <div className="rounded-[1.3rem] border border-white/6 bg-white/[0.03] p-4" key={item.label}>
            <div className="mb-3 flex items-center justify-between gap-3">
              <div>
                <p className="text-[0.68rem] font-semibold uppercase tracking-[0.18em] text-muted-foreground">{item.label}</p>
                <p className="mt-2 text-lg font-semibold">
                  {item.consumed}
                  {item.unit} / {item.target}
                  {item.unit}
                </p>
              </div>
              <div className="text-sm text-muted-foreground">{Math.round(percent)}%</div>
            </div>
            <Progress
              value={percent}
              indicatorClassName={cn(item.tone === "secondary" && "bg-secondary", item.tone === "warning" && "bg-warning")}
            />
          </div>
        );
      })}
    </div>
  );
}
