import { Flame, ShieldCheck } from "lucide-react";
import { NavLink } from "react-router-dom";

import { StatusChip } from "@/components/design/status-chip";
import { navItems } from "@/lib/navigation";
import { cn } from "@/lib/utils";

export function SidebarNav() {
  return (
    <aside className="glass-panel surface-glow hidden w-72 shrink-0 flex-col border-r border-white/6 lg:flex">
      <div className="border-b border-white/6 px-6 py-7">
        <div className="flex items-center gap-3">
          <div className="flex size-12 items-center justify-center rounded-[1.2rem] bg-primary text-primary-foreground">
            <ShieldCheck className="size-6" />
          </div>
          <div>
            <p className="font-display text-xl font-black uppercase tracking-tight text-primary">Monolith 75</p>
            <p className="mt-1 text-xs uppercase tracking-[0.18em] text-muted-foreground">
              discipline operating system
            </p>
          </div>
        </div>
        <div className="mt-6 flex items-center justify-between rounded-[1.3rem] border border-white/6 bg-white/[0.03] px-4 py-3">
          <div>
            <p className="text-[0.68rem] font-semibold uppercase tracking-[0.18em] text-muted-foreground">Current run</p>
            <p className="mt-1 font-display text-2xl font-black">Live sync</p>
          </div>
          <StatusChip label="Backend linked" tone="success" />
        </div>
      </div>

      <nav className="flex-1 space-y-1 overflow-y-auto px-4 py-6">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              className={({ isActive }) =>
                cn(
                  "group flex items-center gap-3 rounded-[1.1rem] px-4 py-3 text-sm font-semibold text-muted-foreground transition-all hover:bg-white/[0.04] hover:text-foreground",
                  isActive &&
                    "bg-[linear-gradient(90deg,rgba(151,255,147,0.12),rgba(151,255,147,0.02))] text-primary ring-1 ring-inset ring-primary/12",
                )
              }
              key={item.to}
              to={item.to}
            >
              <Icon className="size-4.5 transition-transform group-hover:scale-105" />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      <div className="border-t border-white/6 px-6 py-5">
        <div className="rounded-[1.4rem] bg-[linear-gradient(180deg,rgba(25,168,255,0.12),rgba(255,255,255,0.02))] p-4">
          <div className="flex items-center gap-2 text-secondary">
            <Flame className="size-4" />
            <span className="text-[0.68rem] font-semibold uppercase tracking-[0.18em]">Streak status</span>
          </div>
          <p className="mt-3 text-sm text-muted-foreground">Training, nutrition, hydration, and compliance status are all coming from the live app state now.</p>
        </div>
      </div>
    </aside>
  );
}
