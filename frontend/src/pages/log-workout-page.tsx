import { useEffect, useState, type ReactNode } from "react";
import { CalendarRange, CheckCircle2, Flame, MapPin, Play, Plus, RefreshCcw, Timer, Trophy } from "lucide-react";
import { useLocation, useNavigate, useSearchParams } from "react-router-dom";

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
  const location = useLocation();
  const [searchParams, setSearchParams] = useSearchParams();
  const todayDate = getTodayDateString();
  const draftStorageKey = `daily-use:workout-draft:${todayDate}`;
  const [selectedExerciseName, setSelectedExerciseName] = useState<string | undefined>(undefined);
  const [selectedExerciseId, setSelectedExerciseId] = useState<number | undefined>(undefined);
  const { data, isLoading, isError, refetch } = useWorkoutPage(selectedExerciseName, selectedExerciseId);
  const createWorkout = useCreateWorkoutSession();
  const [sessionExercises, setSessionExercises] = useState<WorkoutExercise[]>([]);
  const [draftReps, setDraftReps] = useState("8");
  const [draftWeight, setDraftWeight] = useState("0");
  const [draftDuration, setDraftDuration] = useState("00:45");
  const [draftNotes, setDraftNotes] = useState("");
  const [sessionFeedback, setSessionFeedback] = useState<{ tone: "success" | "warning"; message: string } | null>(null);
  const redirectedExerciseId =
    (location.state as { preselectedExerciseId?: number } | null)?.preselectedExerciseId ??
    (searchParams.get("exerciseId") ? Number.parseInt(searchParams.get("exerciseId") ?? "", 10) : undefined);
  const redirectedExercise =
    (location.state as { preselectedExercise?: string } | null)?.preselectedExercise ?? searchParams.get("exercise") ?? undefined;

  useEffect(() => {
    if (redirectedExerciseId) {
      setSelectedExerciseId(redirectedExerciseId);
    }
    if (redirectedExercise) {
      setSelectedExerciseName(redirectedExercise);
    }
  }, [redirectedExercise, redirectedExerciseId]);

  useEffect(() => {
    if (typeof window === "undefined") return;

    const savedDraft = window.localStorage.getItem(draftStorageKey);
    if (!savedDraft) return;

    try {
      const parsed = JSON.parse(savedDraft) as {
        selectedExerciseName?: string;
        sessionExercises?: WorkoutExercise[];
        draftReps?: string;
        draftWeight?: string;
        draftDuration?: string;
        draftNotes?: string;
      };

      setSelectedExerciseName(redirectedExercise ?? parsed.selectedExerciseName);
      setSelectedExerciseId(redirectedExerciseId);
      setSessionExercises(parsed.sessionExercises ?? []);
      setDraftReps(parsed.draftReps ?? "8");
      setDraftWeight(parsed.draftWeight ?? "0");
      setDraftDuration(parsed.draftDuration ?? "00:45");
      setDraftNotes(parsed.draftNotes ?? "");

      if ((parsed.sessionExercises ?? []).length) {
        setSessionFeedback({
          tone: "warning",
          message: "Your unsaved workout draft was restored after refresh. Use Save session to push it to the backend.",
        });
      }
    } catch {
      window.localStorage.removeItem(draftStorageKey);
    }
  }, [draftStorageKey, redirectedExercise, redirectedExerciseId]);

  useEffect(() => {
    if (typeof window === "undefined") return;

    const isDraftEmpty =
      !sessionExercises.length &&
      !selectedExerciseName &&
      draftReps === "8" &&
      draftWeight === "0" &&
      draftDuration === "00:45" &&
      !draftNotes;

    if (isDraftEmpty) {
      window.localStorage.removeItem(draftStorageKey);
      return;
    }

    window.localStorage.setItem(
      draftStorageKey,
      JSON.stringify({
        selectedExerciseName,
        sessionExercises,
        draftReps,
        draftWeight,
        draftDuration,
        draftNotes,
      }),
    );
  }, [draftDuration, draftNotes, draftReps, draftStorageKey, draftWeight, selectedExerciseName, sessionExercises]);

  useEffect(() => {
    if (!data) return;

    const match = [...sessionExercises].reverse().find((exercise) => exercise.name === data.selectedExercise.title);
    if (match) {
      setDraftReps(match.reps);
      setDraftWeight(match.weight.replace(" kg", ""));
      setDraftDuration(match.duration ?? "00:45");
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
  const timedExercise = isTimedExercise(workoutData.selectedExercise.title, workoutData.dayType);
  const hasDraft = timedExercise ? parseDurationToSeconds(draftDuration) > 0 : Number.parseInt(draftReps, 10) > 0;

  function resetDraft() {
    setDraftReps("8");
    setDraftWeight("0");
    setDraftDuration("00:45");
    setDraftNotes("");
  }

  function completeSet() {
    if (!hasDraft) return;

    const nextExercise: WorkoutExercise = {
      id: `draft-${Date.now()}`,
      name: workoutData.selectedExercise.title,
      muscleGroup: workoutData.selectedExercise.muscleGroup || "General",
      sets: "1",
      reps: timedExercise ? "0" : draftReps,
      duration: timedExercise ? normalizeDurationInput(draftDuration) : undefined,
      weight: `${draftWeight || "0"} kg`,
      previousBest: workoutData.previousPerformance.bestSet,
      pr:
        Number.parseFloat(draftWeight || "0") > extractWeightKg(workoutData.previousPerformance.bestSet) &&
        (timedExercise
          ? parseDurationToSeconds(draftDuration) >= extractDurationSeconds(workoutData.previousPerformance.bestSet)
          : Number.parseInt(draftReps, 10) >= extractReps(workoutData.previousPerformance.bestSet)),
      setLabel: `Set ${nextSetNumber}`,
      note: draftNotes,
      inputMode: timedExercise ? "duration" : "reps",
    };

    setSessionExercises((current) => [nextExercise, ...current]);
    setSelectedExerciseName(workoutData.selectedExercise.title);
    resetDraft();
  }

  function removeSet(exerciseId: string) {
    setSessionExercises((current) => current.filter((exercise) => exercise.id !== exerciseId));
  }

  function handleSaveSession() {
    setSessionFeedback(null);
    createWorkout.mutate(savePayload, {
      onSuccess: (savedWorkout) => {
        setSessionExercises([]);
        setSelectedExerciseName(undefined);
        resetDraft();
        if (typeof window !== "undefined") {
          window.localStorage.removeItem(draftStorageKey);
        }
      setSessionFeedback({
          tone: "success",
          message: `Workout saved to the backend. ${Math.round(savedWorkout.estimated_calories_burned)} kcal was auto-logged for this session.`,
        });
      },
      onError: (error) => {
        const message = error instanceof Error ? error.message : "Workout could not be saved to the backend.";
        setSessionFeedback({ tone: "warning", message });
      },
    });
  }

  const savePayload = {
    date: todayDate,
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
      duration_seconds: exercise.duration ? parseDurationToSeconds(exercise.duration) : null,
      near_failure: false,
      notes: exercise.note || "",
    })),
  };

  return (
    <div className="space-y-5 sm:space-y-6">
      <section className="overflow-hidden rounded-[2rem] border border-white/6 bg-[linear-gradient(135deg,rgba(151,255,147,0.12),rgba(25,168,255,0.12)_38%,rgba(10,12,15,0.98)_74%)] p-4 shadow-[0_20px_64px_rgba(0,0,0,0.38)] sm:rounded-[2.2rem] sm:p-8">
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
            <div className="w-full rounded-[1.5rem] border border-white/8 bg-black/20 px-4 py-4 sm:px-5 lg:min-w-72">
              <p className="text-[0.68rem] uppercase tracking-[0.2em] text-muted-foreground">Live session summary</p>
              <div className="mt-4 grid grid-cols-2 gap-3">
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
          { label: "Save session", onClick: handleSaveSession, disabled: createWorkout.isPending || !sessionExercises.length },
        ]}
      />

      {sessionFeedback ? (
        <div className="rounded-[1.35rem] border border-white/6 bg-white/[0.03] px-4 py-3">
          <StatusChip label={sessionFeedback.tone === "success" ? "Saved to backend" : "Draft only"} tone={sessionFeedback.tone} />
          <p className="mt-2 text-sm leading-6 text-muted-foreground">{sessionFeedback.message}</p>
        </div>
      ) : null}

      <div className="grid gap-6 xl:grid-cols-[1.05fr_0.95fr]">
        <div className="space-y-6">
          <SectionCard
            title="Workout entry"
            description="Choose the movement from your library, then log each working set with its own weight."
            action={
              <div className="flex w-full flex-col items-stretch gap-2 sm:w-auto sm:flex-row sm:flex-wrap sm:items-center sm:justify-end">
                <StatusChip label="Set-by-set logging" tone="success" />
                <Button className="justify-center sm:justify-start" onClick={() => navigate("/workout-timetable")} size="sm" variant="ghost">
                  <CalendarRange className="size-4" />
                  View plan
                </Button>
                <Button
                  className="justify-center sm:justify-start"
                  disabled={createWorkout.isPending || !sessionExercises.length}
                  onClick={handleSaveSession}
                  size="sm"
                  variant="outline"
                >
                  {createWorkout.isPending ? "Saving..." : "Save session"}
                </Button>
              </div>
            }
          >
            <div className="grid gap-4 grid-cols-2">
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
                  onChange={(event) => {
                    const nextExercise = event.target.value;
                    setSelectedExerciseId(undefined);
                    setSelectedExerciseName(nextExercise);
                    setSearchParams((current) => {
                      const next = new URLSearchParams(current);
                      next.set("exercise", nextExercise);
                      next.delete("exerciseId");
                      return next;
                    }, { replace: true });
                  }}
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
                <p className="mt-3 break-words text-lg font-semibold">{workoutData.selectedExercise.title}</p>
                <div className="mt-3 flex flex-wrap items-center gap-2">
                  <StatusChip label={workoutData.selectedExercise.muscleGroup || "General"} tone="secondary" />
                  <StatusChip label={`${workoutData.exerciseOptions.length} exercises in library`} tone="neutral" />
                </div>
                <p className="mt-3 text-sm leading-6 text-muted-foreground">Use different working weights across your sets. For plank and cardio-style movements, log time per set instead of reps. Save session sends the full workout to the backend with calories auto-logged for that session.</p>
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
                <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                  <div className="min-w-0">
                    <p className="text-[0.68rem] uppercase tracking-[0.2em] text-muted-foreground">Selected movement</p>
                    <p className="mt-2 break-words text-xl font-semibold">{workoutData.selectedExercise.title}</p>
                    <p className="mt-2 text-sm text-muted-foreground">{workoutData.previousPerformance.bestSet} best set to beat</p>
                  </div>
                  <StatusChip label={`Set ${nextSetNumber}`} tone="secondary" />
                </div>

                <div className="grid gap-3 sm:grid-cols-2">
                  {timedExercise ? (
                    <Field label="Set time (mm:ss)" onChange={(value) => setDraftDuration(normalizeDurationInput(value))} placeholder="00:45" value={draftDuration} />
                  ) : (
                    <Field label="Reps" onChange={setDraftReps} placeholder="8" value={draftReps} />
                  )}
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
                <BuilderStat label="Completed sets" note="Each tap adds one real set row. Log 2-3 sets per exercise exactly as performed." value={`${totalSets}`} />
                <BuilderStat label="Exercise count" note="Unique exercises already used in this session." value={`${exerciseCount}`} />
                <BuilderStat
                  label="PR pressure"
                  note={timedExercise ? "Longer timed hold or heavier timed effort beats the previous best." : "Beat your previous best set to trigger a PR."}
                  value={
                    timedExercise
                      ? extractDurationSeconds(workoutData.previousPerformance.bestSet) > 0
                        ? `${formatDuration(extractDurationSeconds(workoutData.previousPerformance.bestSet))} target`
                        : "Open target"
                      : extractWeightKg(workoutData.previousPerformance.bestSet) > 0
                        ? `${extractWeightKg(workoutData.previousPerformance.bestSet)} kg target`
                        : "Open target"
                  }
                />
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
                <p className="mt-2 text-sm text-muted-foreground">Enter reps or set time above, then hit complete set. The row lands here immediately.</p>
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
            <div className="rounded-[1.6rem] border border-white/6 bg-[linear-gradient(135deg,rgba(25,168,255,0.12),rgba(18,20,24,0.96))] p-5 sm:p-6">
              <div className="flex flex-col items-start gap-3 sm:flex-row sm:items-center">
                <div className="rounded-[1rem] bg-secondary/12 p-3 text-secondary">
                  <Play className="size-5" />
                </div>
                <div className="min-w-0">
                  <p className="break-all text-base font-semibold sm:text-lg">{workoutData.selectedExercise.youtubeTitle}</p>
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

function extractDurationSeconds(bestSet: string) {
  const match = bestSet.match(/(\d{1,2}):(\d{2})/);
  if (!match) return 0;
  return Number.parseInt(match[1], 10) * 60 + Number.parseInt(match[2], 10);
}

function parseDurationToSeconds(value: string) {
  const normalized = normalizeDurationInput(value);
  const [minutes, seconds] = normalized.split(":");
  return Number.parseInt(minutes, 10) * 60 + Number.parseInt(seconds, 10);
}

function normalizeDurationInput(value: string) {
  const trimmed = value.trim();
  if (!trimmed) return "00:00";
  if (trimmed.includes(":")) {
    const [rawMinutes, rawSeconds = "0"] = trimmed.split(":");
    const minutes = Math.max(0, Number.parseInt(rawMinutes.replace(/\D/g, ""), 10) || 0);
    const seconds = Math.min(59, Math.max(0, Number.parseInt(rawSeconds.replace(/\D/g, ""), 10) || 0));
    return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
  }
  const digits = trimmed.replace(/\D/g, "");
  if (!digits) return "00:00";
  if (digits.length <= 2) {
    return `00:${digits.padStart(2, "0")}`;
  }
  const minutes = digits.slice(0, -2);
  const seconds = digits.slice(-2);
  return `${minutes.padStart(2, "0")}:${seconds}`;
}

function formatDuration(totalSeconds: number) {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}

function isTimedExercise(exerciseName: string, dayType: string) {
  const label = `${exerciseName} ${dayType}`.toLowerCase();
  return ["plank", "cardio", "run", "walk", "cycle", "cycling", "stairmaster", "jump rope", "interval", "jog"].some((keyword) =>
    label.includes(keyword),
  );
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
