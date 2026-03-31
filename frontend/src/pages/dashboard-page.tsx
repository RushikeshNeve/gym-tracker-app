import type { ReactNode } from "react";
import { CalendarCheck2, Dumbbell, Flame, Medal, MoveRight, Scale, TimerReset, Waves } from "lucide-react";

import { ChartSection } from "@/components/design/chart-section";
import { DashboardKpiGrid } from "@/components/design/dashboard-kpi-grid";
import { ErrorState } from "@/components/design/error-state";
import { LoadingShell } from "@/components/design/loading-shell";
import { SectionCard } from "@/components/design/section-card";
import { StatusChip } from "@/components/design/status-chip";
import { PageHeader } from "@/components/layout/page-header";
import { useDashboardData } from "@/hooks/use-dashboard-data";

export function DashboardPage() {
  const { data, isLoading, isError, refetch } = useDashboardData();

  if (isLoading) return <LoadingShell />;
  if (isError || !data) return <ErrorState title="Dashboard could not load" description="The dashboard summary did not arrive from the API." onRetry={() => void refetch()} />;

  return (
    <div className="space-y-6">
      <section className="overflow-hidden rounded-[2.2rem] border border-white/6 bg-[linear-gradient(135deg,rgba(25,168,255,0.16),rgba(151,255,147,0.10)_40%,rgba(10,12,15,0.98)_74%)] p-6 shadow-[0_20px_64px_rgba(0,0,0,0.38)] sm:p-8">
        <PageHeader
          eyebrow={data.heroLabel}
          title={data.heroTitle}
          description={data.heroDescription}
          chips={[
            { label: "Trend-first view", tone: "secondary" },
            { label: "Challenge-aware", tone: "success" },
            { label: "Weekly focus live", tone: "warning" },
          ]}
          actions={
            <div className="min-w-72 rounded-[1.5rem] border border-white/8 bg-black/20 px-5 py-4">
              <p className="text-[0.68rem] font-semibold uppercase tracking-[0.2em] text-muted-foreground">This week summary</p>
              <div className="mt-4 grid gap-3 sm:grid-cols-2">
                {data.weekSummary.map((item) => (
                  <div className="rounded-[1rem] border border-white/6 bg-white/[0.04] px-3 py-3" key={item.label}>
                    <p className="text-xs uppercase tracking-[0.16em] text-muted-foreground">{item.label}</p>
                    <p className="mt-2 text-lg font-semibold">{item.value}</p>
                  </div>
                ))}
              </div>
            </div>
          }
        />

        <div className="mt-8">
          <DashboardKpiGrid items={data.kpis} />
        </div>
      </section>

      <div className="grid gap-6 xl:grid-cols-2">
        <ChartSection trend={data.trends.weight} />
        <ChartSection trend={data.trends.waist} />
        <ChartSection trend={data.trends.calories} />
        <ChartSection trend={data.trends.protein} />
        <ChartSection trend={data.trends.hydration} />
        <ChartSection trend={data.trends.compliance} />
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <div className="space-y-6">
          <SectionCard
            title="Workout frequency summary"
            description="Training density across the current week."
            action={<StatusChip label={`${data.workoutFrequencySummary.totalSessions} sessions`} tone="success" />}
          >
            <div className="grid gap-4 md:grid-cols-[0.8fr_1.2fr]">
              <div className="rounded-[1.5rem] border border-white/6 bg-[linear-gradient(180deg,rgba(151,255,147,0.10),rgba(16,18,22,0.96))] p-5">
                <div className="flex items-center gap-2 text-sm font-semibold">
                  <Dumbbell className="size-4 text-primary" />
                  Sessions landed
                </div>
                <p className="mt-4 text-4xl font-black tracking-tight">{data.workoutFrequencySummary.totalSessions}</p>
                <p className="mt-3 text-sm leading-6 text-muted-foreground">{data.workoutFrequencySummary.summary}</p>
              </div>
              <div className="grid gap-3 sm:grid-cols-4 lg:grid-cols-7">
                {["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].map((day) => {
                  const active = data.workoutFrequencySummary.completedDays.includes(day);
                  return (
                    <div
                      className={
                        active
                          ? "rounded-[1.2rem] border border-primary/14 bg-primary/8 px-4 py-5 text-center"
                          : "rounded-[1.2rem] border border-white/6 bg-white/[0.03] px-4 py-5 text-center"
                      }
                      key={day}
                    >
                      <p className="text-xs uppercase tracking-[0.16em] text-muted-foreground">{day}</p>
                      <p className={active ? "mt-2 text-sm font-semibold text-primary" : "mt-2 text-sm font-semibold"}>{active ? "trained" : "rest"}</p>
                    </div>
                  );
                })}
              </div>
            </div>
          </SectionCard>

          <SectionCard
            title="Recent PRs"
            description="Proof that performance is still moving while the cut stays controlled."
            action={<StatusChip label="Performance rising" tone="success" />}
          >
            <div className="space-y-3">
              {data.recentPrs.map((pr) => (
                <div className="flex items-center justify-between rounded-[1.3rem] border border-white/6 bg-white/[0.03] px-4 py-4" key={pr.id}>
                  <div className="flex items-center gap-3">
                    <div className="flex size-11 items-center justify-center rounded-[1rem] bg-primary/10 text-primary">
                      <Medal className="size-4" />
                    </div>
                    <div>
                      <p className="text-sm font-semibold">{pr.exercise}</p>
                      <p className="mt-1 text-sm text-muted-foreground">{pr.dateLabel}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-semibold">{pr.value}</p>
                    <p className="mt-1 text-xs uppercase tracking-[0.16em] text-primary">new best</p>
                  </div>
                </div>
              ))}
            </div>
          </SectionCard>
        </div>

        <div className="space-y-6">
          <SectionCard
            title="Cardio minutes"
            description="Low-intensity output supporting the challenge without recovery spillover."
            action={<StatusChip label={`${data.cardioMinutesSummary.totalMinutes} min`} tone="secondary" />}
          >
            <div className="grid gap-4 sm:grid-cols-2">
              <QuickTile title="Total cardio" value={`${data.cardioMinutesSummary.totalMinutes}`} subtitle="Minutes this week" icon={<Waves className="size-4 text-secondary" />} />
              <QuickTile title="Daily average" value={`${data.cardioMinutesSummary.averageMinutes}`} subtitle="Minutes per day" icon={<TimerReset className="size-4 text-primary" />} />
            </div>
            <p className="mt-4 rounded-[1.25rem] border border-white/6 bg-black/10 px-4 py-3 text-sm text-muted-foreground">
              {data.cardioMinutesSummary.summary}
            </p>
          </SectionCard>

          <SectionCard
            title="Next planned workout"
            description="The next session should feel decided before the day gets busy."
            action={<StatusChip label={data.nextPlannedWorkout.time} tone="warning" />}
          >
            <div className="rounded-[1.6rem] border border-white/6 bg-[linear-gradient(180deg,rgba(25,168,255,0.10),rgba(16,18,22,0.96))] p-5">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p className="text-2xl font-black tracking-tight">{data.nextPlannedWorkout.title}</p>
                  <p className="mt-3 text-sm leading-6 text-muted-foreground">{data.nextPlannedWorkout.focus}</p>
                </div>
                <div className="rounded-[1rem] bg-secondary/10 p-3 text-secondary">
                  <MoveRight className="size-5" />
                </div>
              </div>
              <p className="mt-4 rounded-[1.2rem] border border-white/6 bg-black/10 px-4 py-3 text-sm text-muted-foreground">
                {data.nextPlannedWorkout.note}
              </p>
            </div>
          </SectionCard>

          <SectionCard title="Quick body read" description="The few signals that matter most this week.">
            <div className="grid gap-3 sm:grid-cols-2">
              <QuickTile title="Bodyweight drift" value="-0.8 kg" subtitle="This week" icon={<Scale className="size-4 text-primary" />} />
              <QuickTile title="Compliance momentum" value="88%" subtitle="Weekly average" icon={<CalendarCheck2 className="size-4 text-secondary" />} />
              <QuickTile title="Protein average" value="154 g" subtitle="Per day" icon={<Flame className="size-4 text-warning" />} />
              <QuickTile title="Outdoor consistency" value="4 sessions" subtitle="This week" icon={<Dumbbell className="size-4 text-primary" />} />
            </div>
          </SectionCard>
        </div>
      </div>
    </div>
  );
}

function QuickTile({ title, value, subtitle, icon }: { title: string; value: string; subtitle: string; icon: ReactNode }) {
  return (
    <div className="rounded-[1.25rem] border border-white/6 bg-white/[0.03] p-4">
      <div className="flex items-center gap-2 text-xs uppercase tracking-[0.16em] text-muted-foreground">
        {icon}
        {title}
      </div>
      <p className="mt-3 text-lg font-semibold">{value}</p>
      <p className="mt-1 text-sm text-muted-foreground">{subtitle}</p>
    </div>
  );
}
