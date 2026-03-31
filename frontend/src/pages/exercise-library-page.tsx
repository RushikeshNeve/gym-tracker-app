import { useMemo, useState } from "react";
import { Search } from "lucide-react";

import { LoadingShell } from "@/components/design/loading-shell";
import { SectionCard } from "@/components/design/section-card";
import { StatusChip } from "@/components/design/status-chip";
import { PageHeader } from "@/components/layout/page-header";
import { useExerciseLibraryPage } from "@/hooks/use-exercise-library-page";
import { Button } from "@/components/ui/button";

export function ExerciseLibraryPage() {
  const { data, isLoading } = useExerciseLibraryPage();
  const [selectedFilter, setSelectedFilter] = useState<string>("All");
  const [search, setSearch] = useState("");

  const filtered = useMemo(() => {
    if (!data) return [];
    return data.exercises.filter((exercise) => {
      const matchFilter = selectedFilter === "All" || exercise.muscleGroups.includes(selectedFilter);
      const haystack = `${exercise.title} ${exercise.muscleGroups.join(" ")} ${exercise.equipment}`.toLowerCase();
      return matchFilter && haystack.includes(search.toLowerCase());
    });
  }, [data, search, selectedFilter]);

  if (isLoading || !data) return <LoadingShell />;

  return (
    <div className="space-y-6">
      <PageHeader
        eyebrow="Movement reference"
        title="Exercise Library"
        description="Search quickly, filter by muscle group, and keep the useful setup cues visible without clutter."
        chips={[{ label: "Video-ready", tone: "secondary" }, { label: "Coaching notes", tone: "success" }]}
      />

      <SectionCard title="Search and filters" description="A fast layer for finding the right lift.">
        <div className="space-y-4">
          <label className="flex items-center gap-3 rounded-[1.2rem] border border-white/6 bg-white/[0.03] px-4 py-3">
            <Search className="size-4 text-muted-foreground" />
            <input
              className="w-full bg-transparent text-sm outline-none placeholder:text-muted-foreground"
              onChange={(event) => setSearch(event.target.value)}
              placeholder={data.searchPlaceholder}
              value={search}
            />
          </label>
          <div className="flex flex-wrap gap-3">
            {["All", ...data.filters].map((filter) => (
              <Button key={filter} onClick={() => setSelectedFilter(filter)} variant={selectedFilter === filter ? "default" : "outline"}>
                {filter}
              </Button>
            ))}
          </div>
        </div>
      </SectionCard>

      <div className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
        <SectionCard title="Exercise cards" description="Search results with muscle-group context and setup clarity." action={<StatusChip label={`${filtered.length} results`} tone="secondary" />}>
          <div className="space-y-4">
            {filtered.map((exercise) => (
              <div className="rounded-[1.35rem] border border-white/6 bg-white/[0.03] p-4" key={exercise.id}>
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <p className="text-base font-semibold">{exercise.title}</p>
                    <p className="mt-2 text-sm text-muted-foreground">{exercise.equipment}</p>
                  </div>
                  <div className="flex flex-wrap justify-end gap-2">
                    {exercise.muscleGroups.map((group) => (
                      <StatusChip key={group} label={group} tone="secondary" />
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </SectionCard>

        <SectionCard title={filtered[0]?.title ?? "Exercise detail"} description={filtered[0]?.youtubeTitle ?? "Select an exercise to view coaching notes."}>
          {filtered[0] ? (
            <div className="space-y-5">
              <div className="rounded-[1.5rem] border border-white/6 bg-[linear-gradient(135deg,rgba(25,168,255,0.10),rgba(18,20,24,0.96))] p-5">
                <p className="text-sm font-semibold">Embedded YouTube demo placeholder</p>
                <p className="mt-2 text-sm leading-6 text-muted-foreground">This area is ready for a real YouTube iframe or media component once the backend returns a demo URL.</p>
              </div>
              <Triple title="Instructions" items={filtered[0].instructions} tone="primary" />
              <Triple title="Mistakes" items={filtered[0].mistakes} tone="warning" />
              <Triple title="Tips" items={filtered[0].tips} tone="secondary" />
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">No matching exercises found.</p>
          )}
        </SectionCard>
      </div>
    </div>
  );
}

function Triple({ title, items, tone }: { title: string; items: string[]; tone: "primary" | "secondary" | "warning" }) {
  return (
    <div className="rounded-[1.2rem] border border-white/6 bg-white/[0.03] p-4">
      <p className={tone === "secondary" ? "text-sm font-semibold text-secondary" : tone === "warning" ? "text-sm font-semibold text-warning" : "text-sm font-semibold text-primary"}>{title}</p>
      <ul className="mt-3 space-y-2">
        {items.map((item) => (
          <li className="rounded-[0.95rem] border border-white/6 bg-black/10 px-3 py-2 text-sm leading-6 text-muted-foreground" key={item}>
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}
