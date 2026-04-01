import { Grid2X2, X } from "lucide-react";
import { useMemo, useState } from "react";
import { NavLink, useLocation } from "react-router-dom";

import { navItems } from "@/lib/navigation";
import { cn } from "@/lib/utils";

const mobileItems = [
  { ...navItems[0], mobileLabel: "Today" },
  { ...navItems[2], mobileLabel: "Workout" },
  { ...navItems[3], mobileLabel: "Plan" },
  { ...navItems[7], mobileLabel: "Cardio" },
  { ...navItems[10], mobileLabel: "Library" },
];

const primaryPaths = new Set<string>(mobileItems.map((item) => item.to));

export function MobileNav() {
  const location = useLocation();
  const [isMoreOpen, setIsMoreOpen] = useState(false);
  const moreItems = useMemo(() => navItems.filter((item) => !primaryPaths.has(item.to)), []);
  const moreActive = moreItems.some((item) => location.pathname.startsWith(item.to));

  return (
    <div className="fixed inset-x-3 bottom-3 z-40 lg:hidden">
      {isMoreOpen ? (
        <div className="glass-panel mb-3 rounded-[1.6rem] border border-white/8 p-3 shadow-[0_16px_48px_rgba(0,0,0,0.38)]">
          <div className="mb-3 flex items-center justify-between px-1">
            <p className="text-[0.68rem] font-semibold uppercase tracking-[0.18em] text-muted-foreground">More tabs</p>
            <button
              className="flex size-9 items-center justify-center rounded-full border border-white/8 bg-white/[0.03] text-muted-foreground transition hover:bg-white/[0.06] hover:text-foreground"
              onClick={() => setIsMoreOpen(false)}
              type="button"
            >
              <X className="size-4" />
            </button>
          </div>
          <div className="grid gap-2 sm:grid-cols-2">
            {moreItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname.startsWith(item.to);
              return (
                <NavLink
                  className={cn(
                    "flex items-center gap-3 rounded-[1rem] border border-white/6 bg-white/[0.03] px-4 py-3 text-sm font-semibold text-muted-foreground transition-colors",
                    isActive && "border-primary/20 bg-primary/10 text-primary",
                  )}
                  key={item.to}
                  onClick={() => setIsMoreOpen(false)}
                  to={item.to}
                >
                  <Icon className="size-4" />
                  <span>{item.label}</span>
                </NavLink>
              );
            })}
          </div>
        </div>
      ) : null}

      <nav className="glass-panel rounded-[1.6rem] border border-white/8 px-1.5 py-1.5 shadow-[0_16px_48px_rgba(0,0,0,0.38)]">
        <div className="flex items-center justify-between gap-1">
          {mobileItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                className={({ isActive }) =>
                  cn(
                    "flex min-w-0 flex-1 flex-col items-center gap-1 rounded-[1rem] px-1.5 py-2 text-[0.58rem] font-semibold uppercase tracking-[0.1em] text-muted-foreground transition-colors",
                    isActive && "bg-white/[0.04] text-primary",
                  )
                }
                key={item.to}
                onClick={() => setIsMoreOpen(false)}
                to={item.to}
              >
                <Icon className="size-4.5" />
                <span className="truncate">{item.mobileLabel}</span>
              </NavLink>
            );
          })}

          <button
            className={cn(
              "flex min-w-0 flex-1 flex-col items-center gap-1 rounded-[1rem] px-1.5 py-2 text-[0.58rem] font-semibold uppercase tracking-[0.1em] text-muted-foreground transition-colors",
              (isMoreOpen || moreActive) && "bg-white/[0.04] text-primary",
            )}
            onClick={() => setIsMoreOpen((current) => !current)}
            type="button"
          >
            <Grid2X2 className="size-4.5" />
            <span className="truncate">More</span>
          </button>
        </div>
      </nav>
    </div>
  );
}
