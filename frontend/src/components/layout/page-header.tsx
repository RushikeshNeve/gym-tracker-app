import type { ReactNode } from "react";

import { StatusChip } from "@/components/design/status-chip";

export function PageHeader({
  eyebrow,
  title,
  description,
  chips,
  actions,
}: {
  eyebrow: string;
  title: string;
  description: string;
  chips?: { label: string; tone?: "neutral" | "success" | "secondary" | "warning" | "danger" }[];
  actions?: ReactNode;
}) {
  return (
    <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
      <div className="max-w-3xl min-w-0">
        <p className="text-[0.68rem] font-semibold uppercase tracking-[0.28em] text-primary">{eyebrow}</p>
        <h2 className="mt-3 text-3xl font-black leading-none tracking-tight sm:text-4xl lg:text-5xl">{title}</h2>
        <p className="mt-4 max-w-2xl text-sm leading-6 text-muted-foreground sm:text-base sm:leading-7">{description}</p>
        {chips?.length ? (
          <div className="mt-5 flex flex-wrap gap-2">
            {chips.map((chip) => (
              <StatusChip key={chip.label} label={chip.label} tone={chip.tone} />
            ))}
          </div>
        ) : null}
      </div>
      {actions ? <div className="w-full lg:w-auto lg:max-w-md">{actions}</div> : null}
    </div>
  );
}
