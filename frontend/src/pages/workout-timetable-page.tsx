import { useState } from "react";
import { ArrowRight, CalendarDays, Repeat2 } from "lucide-react";
import { useNavigate } from "react-router-dom";

import { ErrorState } from "@/components/design/error-state";
import { LoadingShell } from "@/components/design/loading-shell";
import { SectionCard } from "@/components/design/section-card";
import { StatusChip } from "@/components/design/status-chip";
import { PageHeader } from "@/components/layout/page-header";
import { Button } from "@/components/ui/button";
import { useWorkoutTimetable } from "@/hooks/use-workout-page";

export function WorkoutTimetablePage() {
  const navigate = useNavigate();
  const { data, isLoading, isError, refetch } = useWorkoutTimetable();
  const [selectedDayId, setSelectedDayId] = useState<string>("push");

  function openExerciseLogger(exerciseId: number, exerciseName: string) {
    navigate(`/workouts?exerciseId=${exerciseId}`, {
      state: { preselectedExerciseId: exerciseId, preselectedExercise: exerciseName },
    });
  }

  if (isLoading) return <LoadingShell />;
  if (isError || !data) {
    return <ErrorState title="Workout timetable could not load" description="The backend timetable data did not arrive from the API." onRetry={() => void refetch()} />;
  }

  const { weeklySplit, timetableDays } = data;
  const selectedDay = timetableDays.find((day) => day.id === selectedDayId) ?? timetableDays[0];

  return (
    <div className="space-y-6">
      <section className="overflow-hidden rounded-[2.2rem] border border-white/6 bg-[linear-gradient(135deg,rgba(151,255,147,0.14),rgba(25,168,255,0.14)_38%,rgba(10,12,15,0.98)_76%)] p-6 shadow-[0_20px_64px_rgba(0,0,0,0.38)] sm:p-8">
        <PageHeader
          eyebrow="Training plan"
          title="Workout Timetable"
          description="A clean 6-day Push Pull Legs + Cardio structure with exercise options you can rotate based on equipment, energy, or gym traffic."
          chips={[
            { label: "6 training days", tone: "success" },
            { label: "PPL + cardio", tone: "secondary" },
            { label: "2-3 options each", tone: "warning" },
          ]}
          actions={
            <div className="rounded-[1.5rem] border border-white/8 bg-black/20 p-4">
              <p className="text-[0.68rem] uppercase tracking-[0.2em] text-muted-foreground">How to use</p>
              <div className="mt-3 space-y-2 text-sm text-foreground">
                <p>Pick one option per block.</p>
                <p className="text-muted-foreground">Stay with it for 2-3 weeks, then rotate options and progress reps or load.</p>
              </div>
            </div>
          }
        />
      </section>

      <SectionCard
        title="Weekly split"
        description="Pick the day you want to view. The plan below will only show that selected day."
        action={<StatusChip label="Progressive overload" tone="success" />}
      >
        <div className="grid gap-3 md:grid-cols-4 xl:grid-cols-7">
          {weeklySplit.map((day, index) => {
            const mappedDayId =
              day.workout === "Push"
                ? "push"
                : day.workout === "Pull"
                  ? "pull"
                  : day.workout === "Legs"
                    ? "legs"
                    : day.workout === "Cardio + Core"
                      ? "cardio-core"
                      : "rest";
            const isSelected = selectedDay?.id === mappedDayId;
            return (
            <button
              className={`rounded-[1.3rem] border p-4 text-left transition ${
                isSelected ? "border-primary/20 bg-primary/10" : "border-white/6 bg-white/[0.03]"
              }`}
              key={`${day.day}-${index}`}
              onClick={() => {
                if (mappedDayId !== "rest") {
                  setSelectedDayId(mappedDayId);
                }
              }}
              type="button"
            >
              <p className="text-[0.68rem] uppercase tracking-[0.18em] text-muted-foreground">{day.day}</p>
              <p className="mt-3 text-base font-semibold">{day.workout}</p>
            </button>
          )})}
        </div>
      </SectionCard>

      <div className="space-y-6">
        {selectedDay ? (
          <SectionCard
            key={selectedDay.id}
            title={`${selectedDay.dayLabel} - ${selectedDay.title}`}
            description={selectedDay.subtitle}
            action={
              <div className="flex items-center gap-2">
                <StatusChip label={selectedDay.subtitle} tone={chipTone(selectedDay.accent)} />
                <Button onClick={() => navigate("/workouts")} size="sm" variant="outline">
                  Open workout log
                </Button>
              </div>
            }
          >
            <div className="grid gap-4 xl:grid-cols-[1.1fr_0.9fr]">
              <div className="space-y-4">
                {selectedDay.notes?.length ? (
                  <div className="rounded-[1.35rem] border border-white/6 bg-white/[0.03] p-4">
                    <div className="flex items-center gap-2 text-xs uppercase tracking-[0.16em] text-muted-foreground">
                      <Repeat2 className="size-4" />
                      Rotation tip
                    </div>
                    <div className="mt-3 space-y-2 text-sm text-muted-foreground">
                      {selectedDay.notes.map((note) => (
                        <p key={note}>{note}</p>
                      ))}
                    </div>
                  </div>
                ) : null}

                <div className="grid gap-4 md:grid-cols-2">
                  {selectedDay.blocks.map((block) => (
                    <div className="rounded-[1.5rem] border border-white/6 bg-[linear-gradient(180deg,rgba(255,255,255,0.05),rgba(255,255,255,0.02))] p-5" key={block.category}>
                      <div className="flex items-start justify-between gap-3">
                        <div>
                          <p className="text-[0.68rem] uppercase tracking-[0.18em] text-muted-foreground">{block.category}</p>
                          <p className="mt-2 text-lg font-semibold">{block.setsReps}</p>
                        </div>
                        <StatusChip label={`${block.options.length} options`} tone={chipTone(selectedDay.accent)} />
                      </div>
                      <div className="mt-4 space-y-2">
                        {block.options.map((option, index) => (
                          <div className="flex items-center justify-between rounded-[1rem] border border-white/6 bg-black/20 px-3 py-3" key={option.id}>
                            <div className="flex items-center gap-3">
                              <span className="flex size-7 items-center justify-center rounded-full bg-white/6 text-xs font-semibold text-muted-foreground">
                                {index + 1}
                              </span>
                              <span className="text-sm font-medium">{option.name}</span>
                            </div>
                            <Button onClick={() => openExerciseLogger(option.id, option.name)} size="sm" variant="ghost">
                              Add sets
                            </Button>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="space-y-4">
                <div className="grid gap-3 sm:grid-cols-2">
                  {selectedDay.images.slice(0, 4).map((image, index) => (
                    <div className="overflow-hidden rounded-[1.4rem] border border-white/6 bg-white/[0.03]" key={`${selectedDay.id}-${index}`}>
                      <img alt={`${selectedDay.title} exercise option ${index + 1}`} className="h-40 w-full object-cover" loading="lazy" src={image} />
                    </div>
                  ))}
                </div>

                <div className="rounded-[1.5rem] border border-white/6 bg-black/20 p-5">
                  <div className="flex items-center gap-2 text-xs uppercase tracking-[0.16em] text-muted-foreground">
                    <CalendarDays className="size-4" />
                    Implementation note
                  </div>
                  <p className="mt-3 text-sm leading-6 text-muted-foreground">
                    Use this page as the plan reference, then log your actual working sets on the workout page. Pick one option per block and keep it stable long enough to measure progress.
                  </p>
                  <Button className="mt-4 gap-2" onClick={() => navigate("/workouts")}>
                    Start logging sets
                    <ArrowRight className="size-4" />
                  </Button>
                </div>
              </div>
            </div>
          </SectionCard>
        ) : null}
      </div>
    </div>
  );
}

function chipTone(accent: "primary" | "secondary" | "warning") {
  if (accent === "primary") return "success" as const;
  return accent;
}
