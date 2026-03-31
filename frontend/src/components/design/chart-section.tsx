import { SectionCard } from "@/components/design/section-card";
import { cn } from "@/lib/utils";
import type { DashboardTrend } from "@/types/dashboard";

export function ChartSection({ trend }: { trend: DashboardTrend }) {
  const values = trend.points.map((point) => point.value);
  const max = Math.max(...values);
  const min = Math.min(...values);
  const range = Math.max(max - min, 1);

  return (
    <SectionCard title={trend.title} description={trend.description} className="h-full">
      <div className="space-y-5">
        <div className="grid h-48 grid-cols-7 items-end gap-3">
          {trend.points.map((point) => {
            const height = ((point.value - min) / range) * 100;
            return (
              <div className="flex h-full flex-col justify-end gap-3" key={point.label}>
                <div className="text-center text-xs text-muted-foreground">
                  {point.value}
                  {trend.unit}
                </div>
                <div className="relative h-full rounded-[1.3rem] border border-white/6 bg-white/[0.03] p-2">
                  <div
                    className={cn(
                      "absolute inset-x-2 bottom-2 rounded-[0.95rem] transition-all duration-300",
                      trend.accent === "secondary" && "bg-[linear-gradient(180deg,rgba(25,168,255,0.95),rgba(25,168,255,0.22))]",
                      trend.accent === "warning" && "bg-[linear-gradient(180deg,rgba(255,209,111,0.95),rgba(255,209,111,0.20))]",
                      (!trend.accent || trend.accent === "primary") &&
                        "bg-[linear-gradient(180deg,rgba(151,255,147,0.95),rgba(151,255,147,0.18))]",
                    )}
                    style={{ height: `${Math.max(height, 10)}%` }}
                  />
                </div>
                <div className="text-center text-xs uppercase tracking-[0.16em] text-muted-foreground">{point.label}</div>
              </div>
            );
          })}
        </div>
        <div className="rounded-[1.3rem] border border-white/6 bg-white/[0.03] px-4 py-3 text-sm text-muted-foreground">
          {trend.summary}
        </div>
      </div>
    </SectionCard>
  );
}
