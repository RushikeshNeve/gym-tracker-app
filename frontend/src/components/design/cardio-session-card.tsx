import { Footprints, MapPinned, Trash2 } from "lucide-react";

import { StatusChip } from "@/components/design/status-chip";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import type { CardioLog } from "@/types/tracker-pages";

export function CardioSessionCard({ log, onDelete }: { log: CardioLog; onDelete?: () => void }) {
  return (
    <Card>
      <CardContent className="p-5">
        <div className="flex items-start justify-between gap-4">
          <div>
            <div className="flex flex-wrap items-center gap-2">
              <p className="text-base font-semibold">{log.type}</p>
              <StatusChip label={log.outdoor ? "Outdoor" : "Indoor"} tone={log.outdoor ? "success" : "secondary"} />
            </div>
            <p className="mt-2 text-sm text-muted-foreground">{log.dateLabel}</p>
          </div>
          <div className="flex items-center gap-2">
            {onDelete ? (
              <Button aria-label={`Delete ${log.type}`} onClick={onDelete} size="icon" variant="ghost">
                <Trash2 className="size-4" />
              </Button>
            ) : null}
            <div className="rounded-[1rem] bg-secondary/10 p-3 text-secondary">
              {log.outdoor ? <MapPinned className="size-4" /> : <Footprints className="size-4" />}
            </div>
          </div>
        </div>
        <div className="mt-4 grid gap-3 sm:grid-cols-4">
          <Mini label="Duration" value={log.duration} />
          <Mini label="Calories" value={log.calories} />
          <Mini label="Distance" value={log.distance} />
          <Mini label="Pace" value={log.pace} />
        </div>
      </CardContent>
    </Card>
  );
}

function Mini({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-[1rem] border border-white/6 bg-white/[0.03] p-3">
      <p className="text-xs uppercase tracking-[0.16em] text-muted-foreground">{label}</p>
      <p className="mt-2 text-sm font-semibold">{value}</p>
    </div>
  );
}
