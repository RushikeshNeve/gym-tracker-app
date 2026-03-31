import { ArrowUpRight } from "lucide-react";

import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";

export function KpiCard({
  label,
  value,
  detail,
  tone = "neutral",
}: {
  label: string;
  value: string;
  detail: string;
  tone?: "neutral" | "primary" | "secondary" | "warning";
}) {
  return (
    <Card
      className={cn(
        "overflow-hidden",
        tone === "primary" && "bg-[linear-gradient(180deg,rgba(151,255,147,0.14),rgba(22,24,28,0.94))]",
        tone === "secondary" && "bg-[linear-gradient(180deg,rgba(25,168,255,0.14),rgba(22,24,28,0.94))]",
        tone === "warning" && "bg-[linear-gradient(180deg,rgba(255,209,111,0.16),rgba(22,24,28,0.94))]",
      )}
    >
      <CardContent className="p-5">
        <div className="mb-5 flex items-center justify-between">
          <span className="text-[0.68rem] font-semibold uppercase tracking-[0.22em] text-muted-foreground">
            {label}
          </span>
          <ArrowUpRight className="size-4 text-muted-foreground/60" />
        </div>
        <div className="text-3xl font-black tracking-tight">{value}</div>
        <p className="mt-2 text-sm text-muted-foreground">{detail}</p>
      </CardContent>
    </Card>
  );
}

