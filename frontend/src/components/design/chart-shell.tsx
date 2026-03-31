import type { ReactNode } from "react";

import { SectionCard } from "@/components/design/section-card";

export function ChartShell({
  title,
  description,
  children,
}: {
  title: string;
  description: string;
  children: ReactNode;
}) {
  return (
    <SectionCard title={title} description={description}>
      <div className="flex min-h-48 items-center justify-center rounded-[1.4rem] border border-dashed border-white/10 bg-white/[0.02] text-sm text-muted-foreground">
        {children}
      </div>
    </SectionCard>
  );
}
