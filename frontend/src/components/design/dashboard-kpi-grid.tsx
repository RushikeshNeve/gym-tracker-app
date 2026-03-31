import { KpiCard } from "@/components/design/kpi-card";
import type { DashboardKpi } from "@/types/dashboard";

export function DashboardKpiGrid({ items }: { items: DashboardKpi[] }) {
  return (
    <div className="grid gap-4 sm:grid-cols-2 2xl:grid-cols-5">
      {items.map((item) => (
        <KpiCard
          key={item.label}
          label={item.label}
          value={item.value}
          detail={item.detail}
          tone={item.tone}
        />
      ))}
    </div>
  );
}
