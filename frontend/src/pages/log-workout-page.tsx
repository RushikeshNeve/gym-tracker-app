import { useEffect, useState, type ReactNode } from "react";
import { CalendarRange, CheckCircle2, Flame, MapPin, Play, Plus, RefreshCcw, Timer, Trophy } from "lucide-react";
import { useNavigate } from "react-router-dom";

import { ExercisePreviewCard } from "@/components/design/exercise-preview-card";
import { ErrorState } from "@/components/design/error-state";
import { LoadingShell } from "@/components/design/loading-shell";
import { QuickActionStrip } from "@/components/design/quick-action-strip";
import { SectionCard } from "@/components/design/section-card";
import { StatusChip } from "@/components/design/status-chip";
import { WorkoutSessionCard } from "@/components/design/workout-session-card";
import { PageHeader } from "@/components/layout/page-header";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useCreateWorkoutSession, useWorkoutPage } from "@/hooks/use-workout-page";
import { getTodayDateString } from "@/lib/date";
import type { WorkoutExercise } from "@/types/tracker-pages";

export function LogWorkoutPage() {
  const navigate = useNavigate();
  const [selectedExerciseName, setSelectedExerciseName] = useState<string | undefined>(undefined);
  const { data, isLoading, isError, refetch } = useWorkoutPage(selectedExerciseName);
  const createWorkout = useCreateWorkoutSession();
  const [sessionExercises, setSessionExercises] = useState<WorkoutExercise[]>([]);
  const [draftReps, setDraftReps] = useState("8");
  const [draftWeight, setDraftWeight] = useState("0");
  const [draftNotes, setDraftNotes] = useState("");

  useEffect(() => {
    if (!data) return;

    const match = [...sessionExercises].reverse().find((exercise) => exercise.name === data.selectedExercise.title);
    if (match) {
      setDraftReps(match.reps);
      setDraftWeight(match.weight.replace(" kg", ""));
    }
  }, [data, sessionExercises]);

  if (isLoading) return <LoadingShell />;
  if (isError || !data) {
    return <ErrorState title="Workout log could not load" description="Workout history or exercise data did not arrive from the API." onRetry={() => void refetch()} />;
  }

  const workoutData = data;
  const totalSets = sessionExercises.length;
  const exerciseCount = new Set(sessionExercises.map((exercise) => exercise.name)).size;
  const nextSetNumber = sessionExercises.filter((exercise) => exercise.name === workoutData.selectedExercise.title).length + 1;
  const liveBurn = Math.max(workoutData.liveSummary.estimatedCalories, totalSets * 9);
  const hasDraft = Number.parseInt(draftReps, 10) > 0;

  function resetDraft() {
    setDraftReps("8");
    setDraftWeight("0");
    setDraftNotes("");
  }

  function completeSet() {
    if (!hasDraft) return;

    const nextExercise: WorkoutExercise = {
      id: `draft-${Date.now()}`,
      name: workoutData.selectedExercise.title,
      muscleGroup: workoutData.selectedExercise.muscleGroup || "General",
      sets: "1",
      reps: draftReps,
      weight: `${draftWeight || "0"} kg`,
      previousBest: workoutData.previousPerformance.bestSet,
      pr:
        Number.parseFloat(draftWeight || "0") > extractWeightKg(workoutData.previousPerformance.bestSet) &&
        Number.parseInt(draftReps, 10) >= extractReps(workoutData.previousPerformance.bestSet),
      setLabel: `Set ${nextSetNumber}`,
      note: draftNotes,
    };

    setSessionExercises((current) => [nextExercise, ...current]);
    setSelectedExerciseName(workoutData.selectedExercise.title);
    resetDraft();
  }

  function removeSet(exerciseId: string) {
    setSessionExercises((current) => current.filter((exercise) => exercise.id !== exerciseId));
  }

  const savePayload = {
    date: getTodayDateString(),
    day_type: workoutData.dayType,
    session_type: workoutData.sessionType,
    is_outdoor: workoutData.indoorOutdoor === "Outdoor",
    duration_min: Math.max(45, totalSets * 3),
    session_notes: "Logged from the React workout page.",
    exercises: sessionExercises.map((exercise) => ({
      exercise_name: exercise.name,
      muscle_group: exercise.muscleGroup,
      weight: Number.parseFloat(exercise.weight) || 0,
      reps: Number.parseInt(exercise.reps, 10) || 0,
      sets: 1,
      near_failure: false,
      notes: exercise.note || "",
    })),
  };

  return (
    <div className="space-y-6">
      <section className="overflow-hidden rounded-[2.2rem] border border-white/6 bg-[linear-gradient(135deg,rgba(151,255,147,0.12),rgba(25,168,255,0.12)_38%,rgba(10,12,15,0.98)_74%)] p-6 shadow-[0_20px_64px_rgba(0,0,0,0.38)] sm:p-8">
        <PageHeader
          eyebrow={workoutData.dayType}
          title={workoutData.sessionTitle}
          description="Log one set at a time, change the load whenever it changes, and keep the current session clean and fast."
          chips={[
            { label: workoutData.sessionType, tone: "success" },
            { label: workoutData.workoutType, tone: "secondary" },
            { label: workoutData.indoorOutdoor, tone: workoutData.indoorOutdoor === "Outdoor" ? "warning" : "neutral" },
          ]}
          actions={
            <div className="min-w-72 rounded-[1.5rem] border border-white/8 bg-black/20 px-5 py-4">
              <p className="text-[0.68rem] uppercase tracking-[0.2em] text-muted-foreground">Live session summary</p>
              <div className="mt-4 grid gap-3 sm:grid-cols-2">
                <Mini label="Exercises" value={`${exerciseCount}`} />
                <Mini label="Sets" value={`${totalSets}`} />
                <Mini label="Burn" value={`${liveBurn} kcal`} />
                <Mini label="Session state" value={totalSets ? `Next: Set ${nextSetNumber}` : "Ready"} />
              </div>
            </div>
          }
        />
      </section>

      <QuickActionStrip
        actions={[
          { label: "Workout timetable", onClick: () => navigate("/workout-timetable") },
          { label: "Complete set", onClick: completeSet, disabled: !hasDraft },
          { label: "Finish session", onClick: () => createWorkout.mutate(savePayload), disabled: createWorkout.isPending || !sessionExercises.length },
        ]}
      />

      <div className="grid gap-6 xl:grid-cols-[1.05fr_0.95fr]">
        <div className="space-y-6">
          <SectionCard
            title="Workout entry"
            description="Choose the movement from your library, then log each working set with its own weight."
            action={
              <div className="flex items-center gap-2">
                <StatusChip label="Set-by-set logging" tone="success" />
                <Button onClick={() => navigate("/workout-timetable")} size="sm" variant="ghost">
                  <CalendarRange className="size-4" />
                  View plan
                </Button>
                <Button
                  disabled={createWorkout.isPending || !sessionExercises.length}
                  onClick={() => createWorkout.mutate(savePayload)}
                  size="sm"
                  variant="outline"
                >
                  {createWorkout.isPending ? "Saving..." : "Log session"}
                </Button>
              </div>
            }
          >
            <div className="grid gap-4 md:grid-cols-2">
              <Control title="Session type" value={workoutData.sessionType} />
              <Control title="Day type" value={workoutData.dayType} />
              <Control title="Workout type" value={workoutData.workoutType} />
              <Control title="Location" value={workoutData.indoorOutdoor} icon={<MapPin className="size-4 text-secondary" />} />
            </div>
            <div className="mt-5 grid gap-4 lg:grid-cols-[1.1fr_0.9fr]">
              <label className="rounded-[1.35rem] border border-white/6 bg-black/20 p-4">
                <p className="text-[0.68rem] uppercase tracking-[0.18em] text-muted-foreground">Exercise from library</p>
                <select
                  className="mt-3 h-12 w-full rounded-[1rem] border border-white/8 bg-white/[0.04] px-4 text-base font-semibold text-foreground outline-none transition focus:border-primary/45 focus:ring-2 focus:ring-primary/20"
                  onChange={(event) => setSelectedExerciseName(event.target.value)}
                  value={workoutData.selectedExercise.title}
                >
                  {workoutData.exerciseOptions.map((option) => (
                    <option className="bg-[#121212] text-foreground" key={option} value={option}>
                      {option}
                    </option>
                  ))}
                </select>
              </label>

              <div className="rounded-[1.35rem] border border-white/6 bg-white/[0.03] p-4">
                <p className="text-[0.68rem] uppercase tracking-[0.18em] text-muted-foreground">Current selection</p>
                <p className="mt-3 text-lg font-semibold">{workoutData.selectedExercise.title}</p>
                <div className="mt-3 flex flex-wrap items-center gap-2">
                  <StatusChip label={workoutData.selectedExercise.muscleGroup || "General"} tone="secondary" />
                  <StatusChip label={`${workoutData.exerciseOptions.length} exercises in library`} tone="neutral" />
                </div>
                <p className="mt-3 text-sm leading-6 text-muted-foreground">Use different working weights across your sets. Every completed set is logged instantly into the current session below.</p>
              </div>
            </div>
          </SectionCard>

          <ExercisePreviewCard preview={workoutData.selectedExercise} />

          <SectionCard
            title="Set logger"
            description="Complete one set at a time. If your second or third set gets heavier or lighter, just change the weight and log the next set."
            action={<StatusChip label={`${workoutData.selectedExercise.title} - Set ${nextSetNumber}`} tone="success" />}
          >
            <div className="grid gap-4 lg:grid-cols-[1.15fr_0.85fr]">
              <div className="space-y-4 rounded-[1.5rem] border border-white/6 bg-white/[0.03] p-4">
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="text-[0.68rem] uppercase tracking-[0.2em] text-muted-foreground">Selected movement</p>
                    <p className="mt-2 text-xl font-semibold">{workoutData.selectedExercise.title}</p>
                    <p className="mt-2 text-sm text-muted-foreground">{workoutData.previousPerformance.bestSet} best set to beat</p>
                  </div>
                  <StatusChip label={`Set ${nextSetNumber}`} tone="secondary" />
                </div>

                <div className="grid gap-3 sm:grid-cols-2">
                  <Field label="Reps" onChange={setDraftReps} placeholder="8" value={draftReps} />
                  <Field label="Weight (kg)" onChange={setDraftWeight} placeholder="40" value={draftWeight} />
                </div>

                <Textarea
                  onChange={(event) => setDraftNotes(event.target.value)}
                  placeholder="Optional note: top set, short rest, drop set, straps, slower eccentric..."
                  value={draftNotes}
                />

                <div className="flex flex-col gap-3 sm:flex-row">
                  <Button className="gap-2 sm:flex-1" onClick={completeSet}>
                    <Plus className="size-4" />
                    Complete set
                  </Button>
                  <Button className="gap-2 sm:flex-1" onClick={resetDraft} variant="outline">
                    <RefreshCcw className="size-4" />
                    Clear fields
                  </Button>
                </div>
              </div>

              <div className="grid gap-3">
                <BuilderStat label="Completed sets" note="Each tap adds a single set row with its own load." value={`${totalSets}`} />
                <BuilderStat label="Exercise count" note="Unique exercises already used in this session." value={`${exerciseCount}`} />
                <BuilderStat label="PR pressure" note="Beat your previous best set to trigger a PR." value={extractWeightKg(workoutData.previousPerformance.bestSet) > 0 ? `${extractWeightKg(workoutData.previousPerformance.bestSet)} kg target` : "Open target"} />
              </div>
            </div>
          </SectionCard>

          <SectionCard
            title="Completed sets"
            description="Every set row is tracked separately, so you can log 40 kg, 42.5 kg, and 45 kg all in the same exercise."
            action={<StatusChip label={`${sessionExercises.length} sets`} tone="secondary" />}
          >
            {sessionExercises.length ? (
              <div className="space-y-4">
                {sessionExercises.map((exercise) => (
                  <WorkoutSessionCard exercise={exercise} key={exercise.id} onRemove={() => removeSet(exercise.id)} />
                ))}
              </div>
            ) : (
              <div className="rounded-[1.5rem] border border-dashed border-white/10 bg-white/[0.02] px-5 py-8 text-center">
                <CheckCircle2 className="mx-auto size-6 text-primary" />
                <p className="mt-4 text-lg font-semibold">No completed sets yet</p>
                <p className="mt-2 text-sm text-muted-foreground">Enter reps and load above, then hit complete set. The row lands here immediately.</p>
              </div>
            )}
          </SectionCard>
        </div>

        <div className="space-y-6">
          <SectionCard
            title="Previous performance"
            description="Keep the last session close so each working set has context."
            action={<StatusChip label="Comparison live" tone="warning" />}
          >
            <div className="grid gap-4 sm:grid-cols-3">
              <Info icon={<Timer className="size-4 text-secondary" />} title="Last session" value={workoutData.previousPerformance.lastSession} />
              <Info icon={<Trophy className="size-4 text-primary" />} title="Best set" value={workoutData.previousPerformance.bestSet} />
              <Info icon={<Flame className="size-4 text-warning" />} title="Volume" value={workoutData.previousPerformance.volume} />
            </div>
          </SectionCard>

          <SectionCard title="Exercise preview area" description="Reference the demo before you start your next heavy set.">
            <div className="rounded-[1.6rem] border border-white/6 bg-[linear-gradient(135deg,rgba(25,168,255,0.12),rgba(18,20,24,0.96))] p-6">
              <div className="flex items-center gap-3">
                <div className="rounded-[1rem] bg-secondary/12 p-3 text-secondary">
                  <Play className="size-5" />
                </div>
                <div>
                  <p className="text-lg font-semibold">{workoutData.selectedExercise.youtubeTitle}</p>
                  <p className="mt-2 text-sm leading-6 text-muted-foreground">The library demo stays here while you log sets, so switching load mid-session stays fast.</p>
                </div>
              </div>
            </div>
          </SectionCard>
        </div>
      </div>
    </div>
  );
}

function extractWeightKg(bestSet: string) {
  const match = bestSet.match(/(\d+(?:\.\d+)?)\s*kg/i);
  return match ? Number.parseFloat(match[1]) : 0;
}

function extractReps(bestSet: string) {
  const match = bestSet.match(/x\s*(\d+)/i);
  return match ? Number.parseInt(match[1], 10) : 0;
}

function Control({ title, value, icon }: { title: string; value: string; icon?: ReactNode }) {
  return (
    <div className="rounded-[1.2rem] border border-white/6 bg-white/[0.03] p-4">
      <div className="flex items-center gap-2 text-xs uppercase tracking-[0.16em] text-muted-foreground">
        {icon}
        {title}
      </div>
      <p className="mt-3 text-base font-semibold">{value}</p>
    </div>
  );
}

function Info({ title, value, icon }: { title: string; value: string; icon: ReactNode }) {
  return (
    <div className="rounded-[1.2rem] border border-white/6 bg-white/[0.03] p-4">
      <div className="flex items-center gap-2 text-xs uppercase tracking-[0.16em] text-muted-foreground">
        {icon}
        {title}
      </div>
      <p className="mt-3 text-base font-semibold">{value}</p>
    </div>
  );
}

function Mini({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-[1rem] border border-white/6 bg-white/[0.04] px-3 py-3">
      <p className="text-xs uppercase tracking-[0.16em] text-muted-foreground">{label}</p>
      <p className="mt-2 text-lg font-semibold">{value}</p>
    </div>
  );
}

function Field({
  label,
  value,
  onChange,
  placeholder,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  placeholder: string;
}) {
  return (
    <label className="rounded-[1.2rem] border border-white/6 bg-black/20 p-3">
      <p className="text-[0.68rem] uppercase tracking-[0.18em] text-muted-foreground">{label}</p>
      <input
        className="mt-3 h-11 w-full rounded-[0.9rem] border border-white/8 bg-white/[0.04] px-3 text-base font-semibold text-foreground outline-none transition placeholder:text-muted-foreground/55 focus:border-primary/45 focus:ring-2 focus:ring-primary/20"
        inputMode="decimal"
        onChange={(event) => onChange(event.target.value)}
        placeholder={placeholder}
        value={value}
      />
    </label>
  );
}

function BuilderStat({ label, value, note }: { label: string; value: string; note: string }) {
  return (
    <div className="rounded-[1.35rem] border border-white/6 bg-[linear-gradient(180deg,rgba(255,255,255,0.04),rgba(255,255,255,0.02))] p-4">
      <p className="text-[0.68rem] uppercase tracking-[0.18em] text-muted-foreground">{label}</p>
      <p className="mt-3 text-xl font-semibold">{value}</p>
      <p className="mt-2 text-sm leading-6 text-muted-foreground">{note}</p>
    </div>
  );
}
