import { NavLink } from "react-router-dom";

import { navItems } from "@/lib/navigation";
import { cn } from "@/lib/utils";

const mobileItems = [navItems[0], navItems[1], navItems[2], navItems[7], navItems[10]];

export function MobileNav() {
  return (
    <nav className="glass-panel fixed inset-x-3 bottom-3 z-40 rounded-[1.6rem] border border-white/8 px-2 py-2 shadow-[0_16px_48px_rgba(0,0,0,0.38)] lg:hidden">
      <div className="flex items-center justify-between gap-1">
        {mobileItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              className={({ isActive }) =>
                cn(
                  "flex min-w-0 flex-1 flex-col items-center gap-1 rounded-[1rem] px-2 py-2 text-[0.64rem] font-semibold uppercase tracking-[0.14em] text-muted-foreground transition-colors",
                  isActive && "bg-white/[0.04] text-primary",
                )
              }
              key={item.to}
              to={item.to}
            >
              <Icon className="size-4.5" />
              <span className="truncate">{item.label}</span>
            </NavLink>
          );
        })}
      </div>
    </nav>
  );
}

