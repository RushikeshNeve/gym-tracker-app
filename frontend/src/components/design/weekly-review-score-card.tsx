import { Trophy } from "lucide-react";

import { StatusChip } from "@/components/design/status-chip";
import { Card, CardContent } from "@/components/ui/card";

export function WeeklyReviewScoreCard({
  score,
  label,
  description,
}: {
  score: string;
  label: string;
  description: string;
}) {
  return (
    <Card className="bg-[linear-gradient(180deg,rgba(151,255,147,0.12),rgba(18,20,24,0.96))]">
      <CardContent className="p-6">
        <div className="flex items-start justify-between gap-4">
          <div>
            <p className="text-[0.68rem] uppercase tracking-[0.18em] text-muted-foreground">{label}</p>
            <p className="mt-3 text-4xl font-black tracking-tight">{score}</p>
          </div>
          <div className="rounded-[1rem] bg-primary/12 p-3 text-primary">
            <Trophy className="size-5" />
          </div>
        </div>
        <p className="mt-4 text-sm leading-6 text-muted-foreground">{description}</p>
        <div className="mt-4">
          <StatusChip label="Weekly signal" tone="success" />
        </div>
      </CardContent>
    </Card>
  );
}
