import { Camera } from "lucide-react";

import { StatusChip } from "@/components/design/status-chip";
import { SectionCard } from "@/components/design/section-card";
import type { ProgressPhotosPageData } from "@/types/tracker-pages";

export function PhotoComparisonCard({ pair }: { pair: ProgressPhotosPageData["comparisonPair"] }) {
  return (
    <SectionCard title="Comparison layout" description="A cleaner side-by-side read between your oldest and latest recorded photo metadata.">
      <div className="grid gap-4 md:grid-cols-2">
        {[pair.left, pair.right].map((photo) => (
          <div className="rounded-[1.5rem] border border-white/6 bg-white/[0.03] p-4" key={photo.id}>
            <div className="aspect-[4/5] rounded-[1.2rem] border border-white/6 bg-[linear-gradient(135deg,rgba(25,168,255,0.12),rgba(18,20,24,0.96))]">
              {photo.url ? (
                <img
                  alt={`${photo.photoType} progress photo from ${photo.dateLabel}`}
                  className="h-full w-full rounded-[1.2rem] object-cover"
                  src={photo.url}
                />
              ) : (
                <div className="flex h-full items-center justify-center text-muted-foreground">
                  <Camera className="size-8" />
                </div>
              )}
            </div>
            <div className="mt-4 flex items-center justify-between gap-3">
              <div>
                <p className="text-sm font-semibold">{photo.dateLabel}</p>
                <p className="mt-1 max-w-[12rem] truncate text-sm text-muted-foreground">{photo.url}</p>
              </div>
              <StatusChip label={photo.photoType} tone="secondary" />
            </div>
          </div>
        ))}
      </div>
    </SectionCard>
  );
}
