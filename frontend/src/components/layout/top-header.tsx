import { BellDot, Flame, Search } from "lucide-react";

import { Button } from "@/components/ui/button";
import { StatusChip } from "@/components/design/status-chip";

export function TopHeader() {
  return (
    <header className="glass-panel sticky top-0 z-30 flex items-center justify-between rounded-[1.6rem] border border-white/6 px-5 py-4">
      <div>
        <p className="text-[0.68rem] font-semibold uppercase tracking-[0.22em] text-muted-foreground">Today status</p>
        <div className="mt-2 flex flex-wrap items-center gap-3">
          <h1 className="font-display text-2xl font-black tracking-tight sm:text-3xl">Fitness Tracker</h1>
          <StatusChip label="Live backend" tone="success" />
          <StatusChip label="Ready to log" tone="secondary" />
        </div>
      </div>
      <div className="hidden items-center gap-3 md:flex">
        <Button disabled size="icon" variant="ghost">
          <Search className="size-4" />
        </Button>
        <Button disabled size="icon" variant="ghost">
          <BellDot className="size-4" />
        </Button>
        <div className="flex items-center gap-3 rounded-full border border-white/8 bg-white/[0.03] px-3 py-2">
          <div className="flex size-9 items-center justify-center rounded-full bg-primary/12 text-primary">
            <Flame className="size-4" />
          </div>
          <div>
            <p className="text-xs font-semibold">Execution streak</p>
            <p className="text-xs text-muted-foreground">Live data replaces placeholder shell metrics</p>
          </div>
        </div>
      </div>
    </header>
  );
}
