import type { ReactNode } from "react";
import { Bolt, Timer, Trash2, Trophy } from "lucide-react";

import { StatusChip } from "@/components/design/status-chip";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import type { WorkoutExercise } from "@/types/tracker-pages";

export function WorkoutSessionCard({
  exercise,
  onRemove,
}: {
  exercise: WorkoutExercise;
  onRemove?: () => void;
}) {
  return (
    <Card>
      <CardContent className="p-5">
        <div className="flex items-start justify-between gap-4">
          <div>
            <div className="flex flex-wrap items-center gap-2">
              <p className="text-base font-semibold">{exercise.name}</p>
              {exercise.setLabel ? <StatusChip label={exercise.setLabel} tone="warning" /> : null}
              <StatusChip label={exercise.muscleGroup} tone="secondary" />
              {exercise.pr ? <StatusChip label="PR ready" tone="success" /> : null}
            </div>
            <p className="mt-2 text-sm text-muted-foreground">
              {exercise.setLabel ? `${exercise.reps} reps at ${exercise.weight}` : `${exercise.sets} sets x ${exercise.reps} reps at ${exercise.weight}`}
            </p>
            {exercise.note ? <p className="mt-2 text-sm text-muted-foreground">{exercise.note}</p> : null}
          </div>
          <div className="flex items-center gap-2">
            {onRemove ? (
              <Button aria-label={`Remove ${exercise.name}`} onClick={onRemove} size="icon" variant="ghost">
                <Trash2 className="size-4" />
              </Button>
            ) : null}
            <div className="rounded-[1rem] bg-primary/10 p-3 text-primary">
              {exercise.pr ? <Trophy className="size-4" /> : <Bolt className="size-4" />}
            </div>
          </div>
        </div>
        <div className="mt-4 grid gap-3 sm:grid-cols-3">
          <Metric label="Last best" value={exercise.previousBest} icon={<Trophy className="size-3.5" />} />
          <Metric label={exercise.setLabel ? "Set" : "Sets"} value={exercise.setLabel ?? exercise.sets} icon={<Timer className="size-3.5" />} />
          <Metric label="Working load" value={exercise.weight} icon={<Bolt className="size-3.5" />} />
        </div>
      </CardContent>
    </Card>
  );
}

function Metric({ label, value, icon }: { label: string; value: string; icon: ReactNode }) {
  return (
    <div className="rounded-[1rem] border border-white/6 bg-white/[0.03] p-3">
      <div className="flex items-center gap-2 text-xs uppercase tracking-[0.16em] text-muted-foreground">
        {icon}
        {label}
      </div>
      <p className="mt-2 text-sm font-semibold">{value}</p>
    </div>
  );
}
