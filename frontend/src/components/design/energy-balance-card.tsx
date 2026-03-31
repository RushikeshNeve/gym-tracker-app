import { ArrowDown, ArrowUp } from "lucide-react";

import { StatusChip } from "@/components/design/status-chip";
import { SectionCard } from "@/components/design/section-card";
import type { EnergyBalance } from "@/types/nutrition";

export function EnergyBalanceCard({ balance }: { balance: EnergyBalance }) {
  return (
    <SectionCard
      title="Energy balance"
      description="The daily calorie picture after food intake and exercise output."
      action={<StatusChip label={balance.statusLabel} tone={balance.statusTone} />}
    >
      <div className="space-y-4">
        <div className="grid gap-3 sm:grid-cols-2">
          <Metric label="Maintenance" value={`${balance.maintenanceCalories} kcal`} />
          <Metric label="Target" value={`${balance.targetCalories} kcal`} tone="secondary" />
          <Metric label="Food calories" value={`${balance.foodCalories} kcal`} />
          <Metric label="Exercise burn" value={`${balance.exerciseCaloriesBurned} kcal`} tone="primary" />
        </div>
        <div className="rounded-[1.5rem] border border-white/6 bg-[linear-gradient(135deg,rgba(151,255,147,0.10),rgba(14,16,19,0.96))] p-5">
          <div className="flex items-center justify-between gap-4">
            <div>
              <p className="text-[0.68rem] uppercase tracking-[0.2em] text-muted-foreground">Net calories</p>
              <p className="mt-2 text-3xl font-black tracking-tight">{balance.netCalories} kcal</p>
            </div>
            <div className="rounded-[1rem] bg-primary/10 p-3 text-primary">
              {balance.statusTone === "danger" ? <ArrowUp className="size-5" /> : <ArrowDown className="size-5" />}
            </div>
          </div>
          <p className="mt-4 text-sm leading-6 text-muted-foreground">{balance.description}</p>
        </div>
      </div>
    </SectionCard>
  );
}

function Metric({
  label,
  value,
  tone = "neutral",
}: {
  label: string;
  value: string;
  tone?: "neutral" | "primary" | "secondary";
}) {
  return (
    <div className="rounded-[1.25rem] border border-white/6 bg-white/[0.03] p-4">
      <p className="text-[0.68rem] uppercase tracking-[0.18em] text-muted-foreground">{label}</p>
      <p className={tone === "primary" ? "mt-2 text-xl font-bold text-primary" : tone === "secondary" ? "mt-2 text-xl font-bold text-secondary" : "mt-2 text-xl font-bold"}>
        {value}
      </p>
    </div>
  );
}
