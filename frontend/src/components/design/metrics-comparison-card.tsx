import { ArrowDownRight, ArrowUpRight } from "lucide-react";

import { Card, CardContent } from "@/components/ui/card";
import type { MetricStat } from "@/types/tracker-pages";

export function MetricsComparisonCard({ stat }: { stat: MetricStat }) {
  const positive = stat.change.startsWith("-");

  return (
    <Card>
      <CardContent className="p-5">
        <div className="flex items-start justify-between gap-4">
          <div>
            <p className="text-[0.68rem] uppercase tracking-[0.18em] text-muted-foreground">{stat.label}</p>
            <p className="mt-3 text-2xl font-black tracking-tight">{stat.current}</p>
          </div>
          <div className={positive ? "rounded-[1rem] bg-primary/10 p-3 text-primary" : "rounded-[1rem] bg-warning/10 p-3 text-warning"}>
            {positive ? <ArrowDownRight className="size-4" /> : <ArrowUpRight className="size-4" />}
          </div>
        </div>
        <div className="mt-4 grid grid-cols-2 gap-3 text-sm">
          <div className="rounded-[1rem] border border-white/6 bg-black/10 px-3 py-3">
            <p className="text-xs uppercase tracking-[0.16em] text-muted-foreground">Day 1</p>
            <p className="mt-2 font-semibold">{stat.dayOne}</p>
          </div>
          <div className="rounded-[1rem] border border-white/6 bg-black/10 px-3 py-3">
            <p className="text-xs uppercase tracking-[0.16em] text-muted-foreground">Change</p>
            <p className={positive ? "mt-2 font-semibold text-primary" : "mt-2 font-semibold text-warning"}>{stat.change}</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
