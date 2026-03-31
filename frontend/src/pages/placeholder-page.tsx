import { ChartShell } from "@/components/design/chart-shell";
import { EmptyState } from "@/components/design/empty-state";
import { PageHeader } from "@/components/layout/page-header";

export function PlaceholderPage({ title }: { title: string }) {
  return (
    <div className="space-y-6">
      <PageHeader
        eyebrow="Migration in progress"
        title={title}
        description="This route is intentionally scaffolded behind the new app shell so the product can expand page by page without breaking the design system."
        chips={[{ label: "Shell ready", tone: "success" }, { label: "API-ready", tone: "secondary" }]}
      />
      <ChartShell title="Coming next" description="This page will plug into the backend routes once its dedicated UI pass begins.">
        <EmptyState title={`${title} is queued`} description="The route exists, the navigation is wired, and the page can now be built incrementally on top of the shared shell." />
      </ChartShell>
    </div>
  );
}

