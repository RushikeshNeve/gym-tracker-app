import { Medal } from "lucide-react";

import { LoadingShell } from "@/components/design/loading-shell";
import { SectionCard } from "@/components/design/section-card";
import { StatusChip } from "@/components/design/status-chip";
import { TrendSummaryCard } from "@/components/design/trend-summary-card";
import { PageHeader } from "@/components/layout/page-header";
import { useProgressPage } from "@/hooks/use-progress-page";

export function ProgressPage() {
  const { data, isLoading } = useProgressPage();
  if (isLoading || !data) return <LoadingShell />;

  return (
    <div className="space-y-6">
      <PageHeader
        eyebrow="Transformation analytics"
        title="Progress"
        description="This is the long-view page: workload, adherence, performance, and body change all in one read."
        chips={[{ label: "Performance + physique", tone: "success" }, { label: "Trend-first", tone: "secondary" }]}
      />

      <div className="grid gap-6 xl:grid-cols-2">
        {data.trends.map((trend) => (
          <TrendSummaryCard key={trend.title} trend={trend} />
        ))}
      </div>

      <div className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
        <SectionCard title="Strongest lifts" description="The lifts that currently define the phase.">
          <div className="space-y-3">
            {data.strongestLifts.map((lift) => (
              <div className="rounded-[1.2rem] border border-white/6 bg-white/[0.03] p-4" key={lift.exercise}>
                <p className="text-sm font-semibold">{lift.exercise}</p>
                <p className="mt-2 text-2xl font-black tracking-tight">{lift.value}</p>
                <p className="mt-2 text-sm leading-6 text-muted-foreground">{lift.note}</p>
              </div>
            ))}
          </div>
        </SectionCard>

        <SectionCard title="PR history" description="A quick read on recent performance spikes." action={<StatusChip label="Recent wins" tone="success" />}>
          <div className="space-y-3">
            {data.prHistory.map((pr) => (
              <div className="flex items-center justify-between rounded-[1.2rem] border border-white/6 bg-white/[0.03] px-4 py-4" key={pr.id}>
                <div className="flex items-center gap-3">
                  <div className="rounded-[0.95rem] bg-primary/10 p-3 text-primary">
                    <Medal className="size-4" />
                  </div>
                  <div>
                    <p className="text-sm font-semibold">{pr.title}</p>
                    <p className="mt-1 text-sm text-muted-foreground">{pr.when}</p>
                  </div>
                </div>
                <p className="text-sm font-semibold">{pr.value}</p>
              </div>
            ))}
          </div>
        </SectionCard>
      </div>

      <SectionCard title="Transformation analytics" description="The highest-signal outcome cards from the challenge so far.">
        <div className="grid gap-4 md:grid-cols-3">
          {data.transformationAnalytics.map((item) => (
            <div className="rounded-[1.3rem] border border-white/6 bg-white/[0.03] p-4" key={item.label}>
              <p className="text-xs uppercase tracking-[0.16em] text-muted-foreground">{item.label}</p>
              <p className="mt-3 text-2xl font-black tracking-tight">{item.value}</p>
              <p className="mt-2 text-sm leading-6 text-muted-foreground">{item.note}</p>
            </div>
          ))}
        </div>
      </SectionCard>
    </div>
  );
}
