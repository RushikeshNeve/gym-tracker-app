import { useEffect, useState } from "react";
import { CheckCircle2, Droplets, Flame, Gauge, ListTodo, NotebookPen } from "lucide-react";
import { useNavigate } from "react-router-dom";

import { ChecklistCard } from "@/components/design/checklist-card";
import { EmptyState } from "@/components/design/empty-state";
import { ErrorState } from "@/components/design/error-state";
import { KpiCard } from "@/components/design/kpi-card";
import { LoadingShell } from "@/components/design/loading-shell";
import { ProgressCard } from "@/components/design/progress-card";
import { QuickActionStrip } from "@/components/design/quick-action-strip";
import { SectionCard } from "@/components/design/section-card";
import { StatusChip } from "@/components/design/status-chip";
import { PageHeader } from "@/components/layout/page-header";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useTodaySummary, useUpdateTodayNote, useUpdateTodayTask } from "@/hooks/use-today-summary";
import { formatPercent } from "@/lib/utils";
import type { TodayTask } from "@/types/today";

export function TodayPage() {
  const navigate = useNavigate();
  const { data, isLoading, isError, refetch } = useTodaySummary();
  const updateNote = useUpdateTodayNote();
  const updateTask = useUpdateTodayTask();
  const [notes, setNotes] = useState("");

  useEffect(() => {
    setNotes(data?.notes ?? "");
  }, [data?.notes]);

  if (isLoading) {
    return <LoadingShell />;
  }

  if (isError) {
    return <ErrorState title="Today could not load" description="The live challenge summary did not arrive from the API. Try again." onRetry={() => void refetch()} />;
  }

  if (!data) {
    return <EmptyState title="No today summary yet" description="The API returned no current challenge summary for today." />;
  }

  const completedTasks = data.tasks.filter((task) => task.status === "completed");
  const pendingTasks = data.tasks.filter((task) => task.status === "pending");
  const nextCriticalTask = pendingTasks[0]?.title ?? "All critical items handled";
  const mainFocus =
    pendingTasks[0]?.title ??
    (data.dayStatus === "perfect" ? "Protect recovery and repeat the standard tomorrow." : "The day is closed cleanly.");

  function handleTaskToggle(task: TodayTask) {
    updateTask.mutate({
      field: task.field,
      value: task.status !== "completed",
    });
  }

  function handleTaskNavigate(task: TodayTask) {
    if (task.navigateTo) {
      navigate(task.navigateTo);
    }
  }

  return (
    <div className="space-y-6">
      <section className="overflow-hidden rounded-[2.2rem] border border-white/6 bg-[linear-gradient(135deg,rgba(25,168,255,0.15),rgba(151,255,147,0.08)_35%,rgba(12,14,17,0.96)_72%)] p-6 shadow-[0_20px_64px_rgba(0,0,0,0.38)] sm:p-8">
        <PageHeader
          eyebrow={data.focusLabel}
          title={`Day ${data.dayNumber} / ${data.totalDays}`}
          description={data.heroCopy}
          chips={[
            { label: `${formatPercent(data.completionPercentage)} complete`, tone: "success" },
            { label: `${data.currentStreak} day streak`, tone: "secondary" },
            { label: data.splitLabel, tone: "warning" },
          ]}
          actions={
            <div className="rounded-[1.5rem] border border-white/8 bg-black/20 px-5 py-4">
              <p className="text-[0.68rem] font-semibold uppercase tracking-[0.2em] text-muted-foreground">Today pressure points</p>
              <div className="mt-3 space-y-2 text-sm text-foreground">
                <p>{nextCriticalTask}</p>
                <p className="text-muted-foreground">{data.notes}</p>
              </div>
            </div>
          }
        />

        <div className="mt-8 grid gap-4 md:grid-cols-2 xl:grid-cols-5">
          <KpiCard label="Current streak" value={`${data.currentStreak}`} detail="Consecutive perfect days still alive." tone="primary" />
          <KpiCard label="Perfect days" value={`${data.perfectDays}`} detail="Full-compliance wins banked so far." />
          <KpiCard label="Compliance score" value={`${Math.round(data.complianceScore)}%`} detail={`${data.pendingTasks.length} live blockers still matter today.`} tone="secondary" />
          <KpiCard label="Failed days" value={`${data.failedDays}`} detail="Past misses that can't repeat." tone="warning" />
          <KpiCard label="Checklist" value={`${data.completedCount}/${data.tasks.length}`} detail={`${data.pendingCount} items still open.`} tone="secondary" />
        </div>
      </section>

      <QuickActionStrip
        actions={[
          { label: data.quickActions[0] ?? "Log workout", onClick: () => navigate("/workouts") },
          { label: data.quickActions[1] ?? "Add water", onClick: () => navigate("/hydration") },
          { label: data.quickActions[2] ?? "Open meal plan", onClick: () => navigate("/nutrition") },
        ]}
      />

      <div className="grid gap-6 xl:grid-cols-[1.35fr_0.9fr]">
        <div className="space-y-6">
          <SectionCard
            title="Mission control"
            description="The live daily checklist. Tap a card to log the item or clear it."
            action={<StatusChip label={`${pendingTasks.length} pending`} tone={pendingTasks.length ? "warning" : "success"} />}
          >
            <div className="grid gap-4 md:grid-cols-2">
              {data.tasks.map((task) => (
                <ChecklistCard
                  isPending={updateTask.isPending && updateTask.variables?.field === task.field}
                  key={task.id}
                  onNavigate={handleTaskNavigate}
                  onToggle={handleTaskToggle}
                  task={task}
                />
              ))}
            </div>
          </SectionCard>

          <SectionCard
            title="Daily note"
            description="Keep the note tactical. Use it to protect tonight, not to journal around the work."
            action={
              <div className="flex items-center gap-2">
                <NotebookPen className="size-4 text-muted-foreground" />
                <Button
                  disabled={updateNote.isPending}
                  onClick={() => updateNote.mutate(notes)}
                  size="sm"
                  variant="outline"
                >
                  {updateNote.isPending ? "Saving..." : "Save note"}
                </Button>
              </div>
            }
          >
            <Textarea onChange={(event) => setNotes(event.target.value)} placeholder="What still needs protecting before the day closes?" value={notes} />
          </SectionCard>
        </div>

        <div className="space-y-6">
          <SectionCard title="Live summary" description="A clean, fast read on the parts of the day that move the score.">
            <div className="space-y-4">
              <ProgressCard
                label="Challenge completion"
                value={formatPercent(data.completionPercentage)}
                sublabel={`${data.completedCount} complete, ${data.pendingCount} remaining`}
                percent={data.completionPercentage}
                icon={<Gauge className="size-5" />}
              />
              <ProgressCard
                label="Hydration"
                value={`${data.hydrationLiters.toFixed(1)} / ${data.hydrationTargetLiters.toFixed(1)}L`}
                sublabel={`${(data.hydrationTargetLiters - data.hydrationLiters).toFixed(1)}L left before shutdown`}
                percent={(data.hydrationLiters / data.hydrationTargetLiters) * 100}
                icon={<Droplets className="size-5" />}
                tone="secondary"
              />
              <ProgressCard
                label="Calories"
                value={`${Math.round(data.calories)} / ${Math.round(data.caloriesTarget)}`}
                sublabel={`${Math.max(Math.round(data.caloriesTarget - data.calories), 0)} kcal still available in the plan`}
                percent={(data.calories / data.caloriesTarget) * 100}
                icon={<Flame className="size-5" />}
              />
              <ProgressCard
                label="Protein"
                value={`${Math.round(data.protein)} g`}
                sublabel={`${data.totalSessions} total training block${data.totalSessions === 1 ? "" : "s"} logged today`}
                percent={Math.min((data.protein / 180) * 100, 100)}
                icon={<CheckCircle2 className="size-5" />}
                tone="secondary"
              />
            </div>
          </SectionCard>

          <SectionCard title="Pending tasks" description="These are the items still capable of flipping the day.">
            {pendingTasks.length ? (
              <div className="space-y-3">
                {pendingTasks.map((task) => (
                  <div className="rounded-[1.3rem] border border-white/6 bg-white/[0.03] p-4" key={task.id}>
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <p className="text-sm font-semibold">{task.title}</p>
                        <p className="mt-1 text-sm text-muted-foreground">{task.description}</p>
                      </div>
                      <StatusChip label="Open" tone="warning" />
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <EmptyState title="No pending tasks" description="The day is fully closed from the backend summary." />
            )}
          </SectionCard>

          <SectionCard title="Completed today" description="Momentum matters. Keep the visible wins in front of you.">
            <div className="space-y-3">
              {completedTasks.map((task) => (
                <div className="flex items-center justify-between rounded-[1.2rem] border border-primary/10 bg-primary/6 px-4 py-3" key={task.id}>
                  <div className="flex items-center gap-3">
                    <CheckCircle2 className="size-4 text-primary" />
                    <span className="text-sm font-medium">{task.title}</span>
                  </div>
                  <span className="text-xs uppercase tracking-[0.18em] text-primary">done</span>
                </div>
              ))}
            </div>
          </SectionCard>

          <SectionCard title="Quick read" description="Minimal signal. No clutter.">
            <div className="grid gap-3 sm:grid-cols-2">
              <div className="rounded-[1.3rem] border border-white/6 bg-white/[0.03] p-4">
                <div className="flex items-center gap-2 text-muted-foreground">
                  <ListTodo className="size-4" />
                  <span className="text-xs uppercase tracking-[0.18em]">Execution state</span>
                </div>
                <p className="mt-3 text-lg font-semibold">
                  {data.dayStatus === "perfect"
                    ? "Every required item is locked for today."
                    : `${data.workoutSessions} workout, ${data.cardioSessions} cardio, ${data.outdoorSessions} outdoor session${data.outdoorSessions === 1 ? "" : "s"} logged.`}
                </p>
              </div>
              <div className="rounded-[1.3rem] border border-white/6 bg-white/[0.03] p-4">
                <div className="flex items-center gap-2 text-muted-foreground">
                  <Gauge className="size-4" />
                  <span className="text-xs uppercase tracking-[0.18em]">Main focus</span>
                </div>
                <p className="mt-3 text-lg font-semibold">{mainFocus}</p>
              </div>
            </div>
          </SectionCard>
        </div>
      </div>
    </div>
  );
}
