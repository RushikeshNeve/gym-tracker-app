import { Outlet } from "react-router-dom";

import { MobileNav } from "@/components/layout/mobile-nav";
import { SidebarNav } from "@/components/layout/sidebar-nav";
import { TopHeader } from "@/components/layout/top-header";

export function AppShell() {
  return (
    <div className="min-h-screen lg:flex">
      <SidebarNav />
      <div className="flex min-h-screen flex-1 flex-col px-4 pb-28 pt-4 sm:px-6 lg:px-8 lg:pb-8">
        <TopHeader />
        <main className="mx-auto flex w-full max-w-[92rem] flex-1 flex-col py-6">
          <Outlet />
        </main>
      </div>
      <MobileNav />
    </div>
  );
}

