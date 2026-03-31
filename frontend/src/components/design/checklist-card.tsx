import { Check, Circle, Waves, Zap } from "lucide-react";

import { StatusChip } from "@/components/design/status-chip";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import type { TodayTask } from "@/types/today";

const accentStyles = {
  primary: "from-primary/18 to-transparent text-primary",
  secondary: "from-secondary/18 to-transparent text-secondary",
  warning: "from-warning/18 to-transparent text-warning",
};

export function ChecklistCard({
  task,
  onToggle,
  onNavigate,
  isPending = false,
}: {
  task: TodayTask;
  onToggle?: (task: TodayTask) => void;
  onNavigate?: (task: TodayTask) => void;
  isPending?: boolean;
}) {
  const complete = task.status === "completed";
  const buttonVariant = task.interaction === "toggle" ? (complete ? "secondary" : "default") : "outline";
  const buttonLabel =
    task.interaction === "toggle"
      ? complete
        ? (task.completedActionLabel ?? "Undo")
        : (task.pendingActionLabel ?? "Mark done")
      : (task.actionLabel ?? "Open");
  return (
    <Card
      className={cn(
        "relative overflow-hidden transition-transform duration-200 hover:-translate-y-0.5",
        complete && "ring-1 ring-primary/18",
      )}
    >
      <div className={cn("absolute inset-x-0 top-0 h-20 bg-gradient-to-b", accentStyles[task.accent])} />
      <CardContent className="relative p-5">
        <div className="mb-5 flex items-start justify-between gap-4">
          <div className="flex items-center gap-3">
            <div
              className={cn(
                "flex size-11 items-center justify-center rounded-[1rem] border border-white/8 bg-white/[0.03]",
                complete && "border-primary/25 bg-primary/10 text-primary",
              )}
            >
              {task.accent === "secondary" ? (
                <Waves className="size-5" />
              ) : task.accent === "warning" ? (
                <Zap className="size-5" />
              ) : (
                <Check className="size-5" />
              )}
            </div>
            <div>
              <p className="text-[0.68rem] font-semibold uppercase tracking-[0.18em] text-muted-foreground">
                {task.category}
              </p>
              <h3 className="mt-1 text-lg font-semibold">{task.title}</h3>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <StatusChip label={complete ? "Completed" : "Pending"} tone={complete ? "success" : "warning"} />
            {complete ? <Check className="size-4 text-primary" /> : <Circle className="size-4 text-warning" />}
          </div>
        </div>
        <p className="text-sm leading-6 text-muted-foreground">{task.description}</p>
        <div className="mt-5 flex items-center justify-between gap-3">
          <p className="text-xs uppercase tracking-[0.16em] text-muted-foreground">
            {task.interaction === "toggle"
              ? complete
                ? "Logged in mission control"
                : "Still open in mission control"
              : "Driven by live source data"}
          </p>
          <Button
            disabled={isPending}
            onClick={() => (task.interaction === "toggle" ? onToggle?.(task) : onNavigate?.(task))}
            size="sm"
            variant={buttonVariant}
          >
            {isPending && task.interaction === "toggle" ? "Saving..." : buttonLabel}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
