import type { ReactNode } from "react";
import { PlayCircle, TriangleAlert } from "lucide-react";

import { StatusChip } from "@/components/design/status-chip";
import { SectionCard } from "@/components/design/section-card";
import type { WorkoutPageData } from "@/types/tracker-pages";

export function ExercisePreviewCard({ preview }: { preview: WorkoutPageData["selectedExercise"] }) {
  return (
    <SectionCard
      title={preview.title}
      description={preview.previewNote}
      action={<StatusChip label={preview.muscleGroup} tone="secondary" />}
    >
      <div className="space-y-5">
        <div className="rounded-[1.5rem] border border-white/6 bg-[linear-gradient(135deg,rgba(25,168,255,0.10),rgba(15,17,21,0.96))] p-4 sm:p-5">
          <div className="flex flex-col items-start gap-3 sm:flex-row sm:items-center">
            <div className="rounded-[1rem] bg-secondary/12 p-3 text-secondary">
              <PlayCircle className="size-5" />
            </div>
            <div className="min-w-0">
              <p className="break-all text-sm font-semibold">{preview.youtubeTitle}</p>
              <p className="mt-1 text-sm text-muted-foreground">Video area placeholder for future embed wiring.</p>
            </div>
          </div>
        </div>
        <div className="grid gap-4 lg:grid-cols-3">
          <ListBlock title="Instructions" items={preview.instructions} />
          <ListBlock title="Tips" items={preview.tips} tone="secondary" />
          <ListBlock title="Common mistakes" items={preview.mistakes} tone="warning" icon={<TriangleAlert className="size-4 text-warning" />} />
        </div>
      </div>
    </SectionCard>
  );
}

function ListBlock({
  title,
  items,
  tone = "primary",
  icon,
}: {
  title: string;
  items: string[];
  tone?: "primary" | "secondary" | "warning";
  icon?: ReactNode;
}) {
  return (
    <div className="rounded-[1.35rem] border border-white/6 bg-white/[0.03] p-4">
      <div className="flex items-center gap-2 text-sm font-semibold">
        {icon}
        <span className={tone === "secondary" ? "text-secondary" : tone === "warning" ? "text-warning" : "text-primary"}>{title}</span>
      </div>
      <ul className="mt-3 space-y-2 text-sm leading-6 text-muted-foreground">
        {items.map((item) => (
          <li className="rounded-[0.95rem] border border-white/6 bg-black/10 px-3 py-2" key={item}>
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}
