import { Bolt, ChevronRight } from "lucide-react";

import { Button } from "@/components/ui/button";

type QuickAction = string | { label: string; onClick?: () => void; disabled?: boolean };

export function QuickActionStrip({ actions }: { actions: QuickAction[] }) {
  return (
    <div className="grid gap-3 sm:grid-cols-3">
      {actions.map((action) => {
        const item = typeof action === "string" ? { label: action } : action;
        return (
        <Button className="h-auto justify-between rounded-[1.25rem] px-4 py-3 text-left sm:h-11 sm:py-2" disabled={item.disabled} key={item.label} onClick={item.onClick} variant="outline">
          <span className="flex min-w-0 items-center gap-2">
            <Bolt className="size-4 text-primary" />
            <span className="truncate">{item.label}</span>
          </span>
          <ChevronRight className="size-4 text-muted-foreground" />
        </Button>
      )})}
    </div>
  );
}
