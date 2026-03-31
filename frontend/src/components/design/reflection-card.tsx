import { NotebookPen } from "lucide-react";

import { SectionCard } from "@/components/design/section-card";

export function ReflectionCard({
  title,
  items,
}: {
  title: string;
  items: string[];
}) {
  return (
    <SectionCard title={title} description="Written as clear operating notes for next week.">
      <div className="space-y-3">
        {items.map((item) => (
          <div className="flex gap-3 rounded-[1.2rem] border border-white/6 bg-white/[0.03] px-4 py-4" key={item}>
            <div className="rounded-[0.85rem] bg-secondary/10 p-2 text-secondary">
              <NotebookPen className="size-4" />
            </div>
            <p className="text-sm leading-6 text-muted-foreground">{item}</p>
          </div>
        ))}
      </div>
    </SectionCard>
  );
}
