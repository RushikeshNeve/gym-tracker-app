import { Droplets } from "lucide-react";

import { Progress } from "@/components/ui/progress";

export function HydrationMeter({
  consumedMl,
  targetMl,
}: {
  consumedMl: number;
  targetMl: number;
}) {
  const percent = Math.min((consumedMl / targetMl) * 100, 100);

  return (
    <div className="rounded-[1.7rem] border border-white/6 bg-[linear-gradient(180deg,rgba(25,168,255,0.12),rgba(16,18,22,0.96))] p-6">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-[0.68rem] uppercase tracking-[0.2em] text-muted-foreground">Water progress</p>
          <p className="mt-2 text-3xl font-black tracking-tight">
            {(consumedMl / 1000).toFixed(1)}L / {(targetMl / 1000).toFixed(1)}L
          </p>
        </div>
        <div className="rounded-[1rem] bg-secondary/12 p-3 text-secondary">
          <Droplets className="size-5" />
        </div>
      </div>
      <Progress className="mt-5" indicatorClassName="bg-secondary" value={percent} />
      <p className="mt-3 text-sm text-muted-foreground">{Math.round(percent)}% of the daily hydration target is closed.</p>
    </div>
  );
}
