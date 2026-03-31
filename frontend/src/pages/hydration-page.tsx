import { Plus } from "lucide-react";

import { ErrorState } from "@/components/design/error-state";
import { HydrationMeter } from "@/components/design/hydration-meter";
import { LoadingShell } from "@/components/design/loading-shell";
import { SectionCard } from "@/components/design/section-card";
import { StatusChip } from "@/components/design/status-chip";
import { TrendSummaryCard } from "@/components/design/trend-summary-card";
import { PageHeader } from "@/components/layout/page-header";
import { Button } from "@/components/ui/button";
import { useAddHydrationLog, useHydrationPage } from "@/hooks/use-hydration-page";

export function HydrationPage() {
  const { data, isLoading, isError, refetch } = useHydrationPage();
  const addHydration = useAddHydrationLog();
  if (isLoading) return <LoadingShell />;
  if (isError || !data) return <ErrorState title="Hydration could not load" description="The hydration summary did not arrive from the API." onRetry={() => void refetch()} />;

  return (
    <div className="space-y-6">
      <PageHeader
        eyebrow="Daily water control"
        title="Hydration"
        description="Keep water simple, visible, and front-loaded so the evening doesn’t turn into a scramble."
        chips={[
          { label: `${data.consumedMl / 1000}L consumed`, tone: "secondary" },
          { label: `${data.remainingMl / 1000}L remaining`, tone: "warning" },
        ]}
      />

      <div className="grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
        <div className="space-y-6">
          <HydrationMeter consumedMl={data.consumedMl} targetMl={data.targetMl} />
          <SectionCard title="Quick add" description="Fast taps for the most common intake sizes." action={<StatusChip label="One tap" tone="success" />}>
            <div className="grid gap-3 sm:grid-cols-3">
              {data.quickAdds.map((amount) => (
                <Button className="justify-between rounded-[1.25rem]" disabled={addHydration.isPending} key={amount} onClick={() => addHydration.mutate(amount)} variant="outline">
                  {amount < 1000 ? `${amount} ml` : `${amount / 1000} L`}
                  <Plus className="size-4 text-secondary" />
                </Button>
              ))}
            </div>
          </SectionCard>
        </div>
        <TrendSummaryCard trend={data.weeklyTrend} />
      </div>

      <SectionCard title="Today's history" description="Every intake block that has already landed." action={<StatusChip label={`${data.history.length} entries`} tone="secondary" />}>
        <div className="space-y-3">
          {data.history.map((entry) => (
            <div className="flex items-center justify-between rounded-[1.2rem] border border-white/6 bg-white/[0.03] px-4 py-4" key={entry.id}>
              <div>
                <p className="text-sm font-semibold">{entry.time}</p>
                <p className="mt-1 text-sm text-muted-foreground">{entry.note}</p>
              </div>
              <div className="text-right">
                <p className="text-base font-semibold">{entry.amountMl} ml</p>
                <p className="mt-1 text-xs uppercase tracking-[0.16em] text-secondary">logged</p>
              </div>
            </div>
          ))}
        </div>
      </SectionCard>
    </div>
  );
}
