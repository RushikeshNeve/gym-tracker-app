import { useState } from "react";
import { Bike, Clock3, Flame, MapPinned } from "lucide-react";

import { ErrorState } from "@/components/design/error-state";
import { LoadingShell } from "@/components/design/loading-shell";
import { CardioSessionCard } from "@/components/design/cardio-session-card";
import { SectionCard } from "@/components/design/section-card";
import { StatusChip } from "@/components/design/status-chip";
import { TrendSummaryCard } from "@/components/design/trend-summary-card";
import { PageHeader } from "@/components/layout/page-header";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useCardioPage, useCreateCardioLog, useDeleteCardioLog } from "@/hooks/use-cardio-page";
import { getTodayDateString } from "@/lib/date";

type CardioFormState = {
  date: string;
  cardioType: string;
  duration: string;
  distance: string;
  pace: string;
  calories: string;
  intensity: string;
  notes: string;
  outdoor: boolean;
};

const emptyForm: CardioFormState = {
  date: getTodayDateString(),
  cardioType: "Outdoor incline walk",
  duration: "30",
  distance: "",
  pace: "",
  calories: "",
  intensity: "Moderate",
  notes: "",
  outdoor: true,
};

export function CardioPage() {
  const { data, isLoading, isError, refetch } = useCardioPage();
  const createCardio = useCreateCardioLog();
  const deleteCardio = useDeleteCardioLog();
  const [form, setForm] = useState<CardioFormState>(emptyForm);
  if (isLoading) return <LoadingShell />;
  if (isError || !data) return <ErrorState title="Cardio could not load" description="The cardio logs did not arrive from the API." onRetry={() => void refetch()} />;
  const cardioData = data;

  function updateField<K extends keyof CardioFormState>(key: K, value: CardioFormState[K]) {
    setForm((current) => ({ ...current, [key]: value }));
  }

  async function handleSubmit() {
    await createCardio.mutateAsync({
      date: form.date,
      cardio_type: form.cardioType,
      duration_min: Number.parseInt(form.duration, 10) || 1,
      distance_km: Number.parseFloat(form.distance) || 0,
      pace_text: form.pace,
      calories: form.calories.trim() ? Number.parseInt(form.calories, 10) || 0 : null,
      intensity: form.intensity || null,
      notes: form.notes,
      is_outdoor: form.outdoor,
    });

    setForm({
      ...emptyForm,
      date: getTodayDateString(),
      cardioType: form.cardioType,
      outdoor: form.outdoor,
    });
  }

  return (
    <div className="space-y-6">
      <PageHeader
        eyebrow="Conditioning"
        title="Cardio"
        description="Keep cardio supportive, repeatable, and easy to recover from. The goal is consistency, not drama."
        chips={[{ label: "Outdoor-aware", tone: "success" }, { label: "Recovery-safe", tone: "secondary" }]}
      />

      <div className="grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
        <SectionCard
          title="Log cardio"
          description="Add a cardio session with duration, distance, pace, calories, and outdoor status."
          action={<StatusChip label={createCardio.isPending ? "Saving..." : "Live form"} tone="success" />}
        >
          <div className="space-y-5">
            <div className="grid gap-3 sm:grid-cols-2">
              <Field icon={<Clock3 className="size-4 text-secondary" />} label="Date" type="date" value={form.date} onChange={(value) => updateField("date", value)} />
              <Field icon={<Bike className="size-4 text-secondary" />} label="Cardio type" value={form.cardioType} onChange={(value) => updateField("cardioType", value)} />
              <Field label="Duration (min)" value={form.duration} onChange={(value) => updateField("duration", value)} placeholder="30" />
              <Field label="Distance (km)" value={form.distance} onChange={(value) => updateField("distance", value)} placeholder="3.5" />
              <Field label="Pace" value={form.pace} onChange={(value) => updateField("pace", value)} placeholder="8:20 / km" />
              <Field icon={<Flame className="size-4 text-warning" />} label="Calories" value={form.calories} onChange={(value) => updateField("calories", value)} placeholder="240" />
              <Field label="Intensity" value={form.intensity} onChange={(value) => updateField("intensity", value)} placeholder="Moderate" />
              <label className="rounded-[1.2rem] border border-white/6 bg-black/10 p-3">
                <div className="flex items-center gap-2 text-[0.68rem] uppercase tracking-[0.18em] text-muted-foreground">
                  <MapPinned className="size-4 text-primary" />
                  Location
                </div>
                <div className="mt-3 flex gap-2">
                  <Button className="flex-1" onClick={() => updateField("outdoor", true)} type="button" variant={form.outdoor ? "default" : "outline"}>
                    Outdoor
                  </Button>
                  <Button className="flex-1" onClick={() => updateField("outdoor", false)} type="button" variant={!form.outdoor ? "default" : "outline"}>
                    Indoor
                  </Button>
                </div>
              </label>
            </div>

            <Textarea
              onChange={(event) => updateField("notes", event.target.value)}
              placeholder="Optional note: incline walk after lift, zone 2 treadmill, easy recovery ride, weather conditions..."
              value={form.notes}
            />

            <div className="flex flex-col gap-3 sm:flex-row">
              <Button className="sm:flex-1" disabled={createCardio.isPending} onClick={() => void handleSubmit()}>
                {createCardio.isPending ? "Saving..." : "Log cardio"}
              </Button>
              <Button className="sm:flex-1" onClick={() => setForm({ ...emptyForm, date: getTodayDateString() })} variant="outline">
                Reset form
              </Button>
            </div>
          </div>
        </SectionCard>
        <SectionCard title="Cardio presets" description="Fast-start session templates for the days you don't want to think.">
          <div className="space-y-3">
            {cardioData.sessionPresets.map((preset) => (
              <div className="rounded-[1.25rem] border border-white/6 bg-white/[0.03] p-4" key={preset.label}>
                <p className="text-sm font-semibold">{preset.label}</p>
                <p className="mt-2 text-sm leading-6 text-muted-foreground">{preset.note}</p>
                <Button
                  className="mt-4"
                  onClick={() => {
                    updateField("cardioType", preset.label);
                    updateField("outdoor", preset.label.toLowerCase().includes("outdoor"));
                  }}
                  size="sm"
                  variant="outline"
                >
                  Use preset
                </Button>
              </div>
            ))}
          </div>
        </SectionCard>
        <TrendSummaryCard trend={cardioData.trend} />
      </div>

      <SectionCard title="Weekly cardio summary" description="The minimum signal needed to see if conditioning is on plan.">
        <div className="grid gap-4 md:grid-cols-3">
          {cardioData.weeklySummary.map((item) => (
            <div className="rounded-[1.3rem] border border-white/6 bg-white/[0.03] p-4" key={item.label}>
              <p className="text-xs uppercase tracking-[0.16em] text-muted-foreground">{item.label}</p>
              <p className="mt-3 text-2xl font-black tracking-tight">{item.value}</p>
              <p className="mt-2 text-sm leading-6 text-muted-foreground">{item.note}</p>
            </div>
          ))}
        </div>
      </SectionCard>

      <SectionCard title="Cardio history" description="Recent sessions with distance, pace, and burn visible.">
        <div className="space-y-4">
          {cardioData.history.map((log) => (
            <CardioSessionCard key={log.id} log={log} onDelete={() => deleteCardio.mutate(Number(log.id))} />
          ))}
        </div>
      </SectionCard>
    </div>
  );
}

function Field({
  label,
  value,
  onChange,
  placeholder,
  type = "text",
  icon,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  type?: "text" | "date";
  icon?: React.ReactNode;
}) {
  return (
    <label className="rounded-[1.2rem] border border-white/6 bg-black/10 p-3">
      <div className="flex items-center gap-2 text-[0.68rem] uppercase tracking-[0.18em] text-muted-foreground">
        {icon ?? <Clock3 className="size-4" />}
        {label}
      </div>
      <input
        className="mt-3 h-11 w-full rounded-[0.95rem] border border-white/8 bg-white/[0.04] px-3 text-sm font-semibold text-foreground outline-none transition placeholder:text-muted-foreground/60 focus:border-primary/45 focus:ring-2 focus:ring-primary/20"
        inputMode={type === "date" ? undefined : "decimal"}
        onChange={(event) => onChange(event.target.value)}
        placeholder={placeholder}
        type={type}
        value={value}
      />
    </label>
  );
}
