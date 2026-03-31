import { cn } from "@/lib/utils";
import type { TrendData } from "@/types/tracker-pages";

export function TrendSummaryCard({ trend }: { trend: TrendData }) {
  const values = trend.points.map((point) => point.value);
  const max = Math.max(...values);
  const min = Math.min(...values);
  const range = Math.max(max - min, 1);

  return (
    <div className="rounded-[1.65rem] border border-white/6 bg-card/90 p-6">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-lg font-semibold">{trend.title}</p>
          <p className="mt-2 text-sm leading-6 text-muted-foreground">{trend.description}</p>
        </div>
        <div className="text-xs uppercase tracking-[0.16em] text-muted-foreground">{trend.unit}</div>
      </div>
      <div className="mt-6 grid h-40 grid-cols-7 items-end gap-3">
        {trend.points.map((point) => {
          const height = ((point.value - min) / range) * 100;
          return (
            <div className="flex h-full flex-col justify-end gap-2" key={point.label}>
              <div
                className={cn(
                  "rounded-[0.95rem]",
                  trend.accent === "secondary" && "bg-[linear-gradient(180deg,rgba(25,168,255,0.95),rgba(25,168,255,0.18))]",
                  trend.accent === "warning" && "bg-[linear-gradient(180deg,rgba(255,209,111,0.95),rgba(255,209,111,0.18))]",
                  (!trend.accent || trend.accent === "primary") &&
                    "bg-[linear-gradient(180deg,rgba(151,255,147,0.95),rgba(151,255,147,0.18))]",
                )}
                style={{ height: `${Math.max(height, 14)}%` }}
              />
              <p className="text-center text-[0.68rem] uppercase tracking-[0.14em] text-muted-foreground">{point.label}</p>
            </div>
          );
        })}
      </div>
      <p className="mt-4 rounded-[1rem] border border-white/6 bg-black/10 px-4 py-3 text-sm text-muted-foreground">{trend.summary}</p>
    </div>
  );
}
