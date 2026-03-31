import { useEffect, useState } from "react";

import { ErrorState } from "@/components/design/error-state";
import { LoadingShell } from "@/components/design/loading-shell";
import { ReflectionCard } from "@/components/design/reflection-card";
import { SectionCard } from "@/components/design/section-card";
import { WeeklyReviewScoreCard } from "@/components/design/weekly-review-score-card";
import { PageHeader } from "@/components/layout/page-header";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useUpsertWeeklyReview, useWeeklyReviewPage } from "@/hooks/use-weekly-review-page";
import { getWeekStartString } from "@/lib/date";

export function WeeklyReviewPage() {
  const { data, isLoading, isError, refetch } = useWeeklyReviewPage();
  const saveReview = useUpsertWeeklyReview();
  const [wins, setWins] = useState("");
  const [misses, setMisses] = useState("");
  const [focus, setFocus] = useState("");
  const [note, setNote] = useState("");

  useEffect(() => {
    if (!data) return;
    setWins(data.reflection.wins.join("\n"));
    setMisses(data.reflection.misses.join("\n"));
    setFocus(data.reflection.nextWeekFocus.join("\n"));
    setNote(data.reflection.note);
  }, [data]);

  if (isLoading) return <LoadingShell />;
  if (isError || !data) return <ErrorState title="Weekly review could not load" description="Weekly summary data did not arrive from the API." onRetry={() => void refetch()} />;

  return (
    <div className="space-y-6">
      <PageHeader
        eyebrow="Weekly close"
        title="Weekly Review"
        description="This page should tell you whether the week was truly aligned, where it leaked, and what next week needs most."
        chips={[{ label: "Reflection-ready", tone: "secondary" }, { label: "Execution score live", tone: "success" }]}
      />

      <div className="grid gap-6 xl:grid-cols-[0.8fr_1.2fr]">
        <WeeklyReviewScoreCard
          description="Strong week overall. The challenge stayed alive because training and food discipline were consistent, even when hydration slipped."
          label="Weekly score"
          score={data.weeklyScore}
        />
        <SectionCard title="Weekly summary" description="The key weekly outputs without burying the signal.">
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            {data.summaryCards.map((item) => (
              <div className="rounded-[1.25rem] border border-white/6 bg-white/[0.03] p-4" key={item.label}>
                <p className="text-xs uppercase tracking-[0.16em] text-muted-foreground">{item.label}</p>
                <p className="mt-3 text-xl font-black tracking-tight">{item.value}</p>
                <p className="mt-2 text-sm leading-6 text-muted-foreground">{item.note}</p>
              </div>
            ))}
          </div>
        </SectionCard>
      </div>

      <SectionCard title="Body changes" description="Weekly physique and recovery notes.">
        <div className="grid gap-4 md:grid-cols-3">
          {data.bodyChanges.map((item) => (
            <div className="rounded-[1.3rem] border border-white/6 bg-white/[0.03] p-4" key={item.label}>
              <p className="text-xs uppercase tracking-[0.16em] text-muted-foreground">{item.label}</p>
              <p className="mt-3 text-2xl font-black tracking-tight">{item.value}</p>
              <p className="mt-2 text-sm leading-6 text-muted-foreground">{item.note}</p>
            </div>
          ))}
        </div>
      </SectionCard>

      <div className="grid gap-6 xl:grid-cols-3">
        <ReflectionCard items={data.reflection.wins} title="Wins" />
        <ReflectionCard items={data.reflection.misses} title="Misses" />
        <ReflectionCard items={data.reflection.nextWeekFocus} title="Next week focus" />
      </div>

      <SectionCard
        title="Review editor"
        description="These fields write back to the weekly review record in the backend."
        action={
          <Button
            disabled={saveReview.isPending}
            onClick={() =>
              saveReview.mutate({
                week_start: getWeekStartString(),
                what_went_well: wins,
                what_was_difficult: misses,
                focus_for_next_week: focus,
                notes: note,
              })
            }
            size="sm"
            variant="outline"
          >
            {saveReview.isPending ? "Saving..." : "Save review"}
          </Button>
        }
      >
        <div className="grid gap-4 xl:grid-cols-2">
          <Textarea onChange={(event) => setWins(event.target.value)} placeholder="What went well" value={wins} />
          <Textarea onChange={(event) => setMisses(event.target.value)} placeholder="What was difficult" value={misses} />
          <Textarea onChange={(event) => setFocus(event.target.value)} placeholder="Focus for next week" value={focus} />
          <Textarea onChange={(event) => setNote(event.target.value)} placeholder="Reflection note" value={note} />
        </div>
      </SectionCard>

      <SectionCard title="Reflection note" description="Keep the takeaway practical enough to change next week.">
        <div className="rounded-[1.4rem] border border-white/6 bg-[linear-gradient(180deg,rgba(25,168,255,0.10),rgba(16,18,22,0.96))] p-5">
          <p className="text-base font-semibold">{data.reflection.note}</p>
        </div>
      </SectionCard>
    </div>
  );
}
