import type { ReactNode } from "react";

import { Progress } from "@/components/ui/progress";
import { cn } from "@/lib/utils";

export function ProgressCard({
  label,
  value,
  sublabel,
  percent,
  icon,
  tone = "primary",
}: {
  label: string;
  value: string;
  sublabel: string;
  percent: number;
  icon?: ReactNode;
  tone?: "primary" | "secondary";
}) {
  return (
    <div className="rounded-[1.5rem] border border-white/6 bg-white/[0.03] p-5">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <p className="text-[0.68rem] font-semibold uppercase tracking-[0.2em] text-muted-foreground">{label}</p>
          <div className="mt-2 text-2xl font-black tracking-tight">{value}</div>
        </div>
        <div className={cn("rounded-[1rem] p-3", tone === "primary" ? "bg-primary/10 text-primary" : "bg-secondary/10 text-secondary")}>
          {icon}
        </div>
      </div>
      <Progress value={percent} indicatorClassName={tone === "secondary" ? "bg-secondary" : undefined} />
      <p className="mt-3 text-sm text-muted-foreground">{sublabel}</p>
    </div>
  );
}
