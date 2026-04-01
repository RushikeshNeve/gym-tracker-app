import { useEffect, useRef, useState, type ReactNode } from "react";
import { Pencil, Plus, Ruler, Save, Trash2, Weight } from "lucide-react";

import { ErrorState } from "@/components/design/error-state";
import { LoadingShell } from "@/components/design/loading-shell";
import { MetricsComparisonCard } from "@/components/design/metrics-comparison-card";
import { SectionCard } from "@/components/design/section-card";
import { StatusChip } from "@/components/design/status-chip";
import { TrendSummaryCard } from "@/components/design/trend-summary-card";
import { PageHeader } from "@/components/layout/page-header";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import {
  useBodyMetricsPage,
  useCreateBodyMetric,
  useDeleteBodyMetric,
  useUpdateBodyMetric,
} from "@/hooks/use-body-metrics-page";
import { getTodayDateString } from "@/lib/date";

type MetricsFormState = {
  date: string;
  bodyWeight: string;
  waist: string;
  hips: string;
  chest: string;
  arms: string;
  thighs: string;
  neck: string;
  bodyFat: string;
  notes: string;
};

const emptyForm: MetricsFormState = {
  date: getTodayDateString(),
  bodyWeight: "",
  waist: "",
  hips: "",
  chest: "",
  arms: "",
  thighs: "",
  neck: "",
  bodyFat: "",
  notes: "",
};

export function BodyMetricsPage() {
  const { data, isLoading, isError, refetch } = useBodyMetricsPage();
  const createMetric = useCreateBodyMetric();
  const updateMetric = useUpdateBodyMetric();
  const deleteMetric = useDeleteBodyMetric();
  const [editingId, setEditingId] = useState<number | null>(null);
  const [form, setForm] = useState<MetricsFormState>(emptyForm);
  const [formFeedback, setFormFeedback] = useState<{ tone: "success" | "warning"; message: string } | null>(null);
  const formSectionRef = useRef<HTMLDivElement | null>(null);

  const isSaving = createMetric.isPending || updateMetric.isPending;

  useEffect(() => {
    if (editingId == null || !data) return;

    const stillExists = data.entries.some((entry) => entry.id === editingId);
    if (!stillExists) {
      resetForm();
      setFormFeedback({ tone: "warning", message: "That entry no longer exists, so the form was reset to a fresh add state." });
    }
  }, [data, editingId]);

  if (isLoading) return <LoadingShell />;
  if (isError || !data) return <ErrorState title="Body metrics could not load" description="The body-metrics history did not arrive from the API." onRetry={() => void refetch()} />;
  const metricsData = data;

  const formTitle = editingId ? "Edit body metric entry" : "Add body metrics";
  const formDescription = editingId
    ? "Update a recorded entry and keep the trends clean."
    : "Log your latest measurements here. Weight, waist, hips, chest, arms, thighs, neck, body fat, and notes all save into the backend.";

  function updateField<K extends keyof MetricsFormState>(key: K, value: MetricsFormState[K]) {
    setForm((current) => ({ ...current, [key]: value }));
  }

  function resetForm(clearFeedback = true) {
    setEditingId(null);
    if (clearFeedback) {
      setFormFeedback(null);
    }
    setForm({
      date: getTodayDateString(),
      bodyWeight: "",
      waist: "",
      hips: "",
      chest: "",
      arms: "",
      thighs: "",
      neck: "",
      bodyFat: "",
      notes: "",
    });
  }

  function startEdit(entryId: number) {
    const entry = metricsData.entries.find((item) => item.id === entryId);
    if (!entry) return;

    setEditingId(entry.id);
    setFormFeedback({ tone: "warning", message: `Editing entry from ${entry.date}. Change the values you want, then tap Update entry.` });
    setForm({
      date: entry.date,
      bodyWeight: entry.bodyWeight?.toString() ?? "",
      waist: entry.waist?.toString() ?? "",
      hips: entry.hips?.toString() ?? "",
      chest: entry.chest?.toString() ?? "",
      arms: entry.arms?.toString() ?? "",
      thighs: entry.thighs?.toString() ?? "",
      neck: entry.neck?.toString() ?? "",
      bodyFat: entry.bodyFat?.toString() ?? "",
      notes: entry.progressNotes || entry.notes || "",
    });
    formSectionRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  async function handleSubmit() {
    setFormFeedback(null);
    const payload = {
      date: form.date,
      body_weight: parseOptionalNumber(form.bodyWeight),
      waist: parseOptionalNumber(form.waist),
      hips: parseOptionalNumber(form.hips),
      chest: parseOptionalNumber(form.chest),
      arms: parseOptionalNumber(form.arms),
      thighs: parseOptionalNumber(form.thighs),
      neck: parseOptionalNumber(form.neck),
      body_fat_percent: parseOptionalNumber(form.bodyFat),
      notes: form.notes,
      progress_notes: form.notes,
    };

    try {
      if (editingId) {
        await updateMetric.mutateAsync({ id: editingId, payload });
        setFormFeedback({ tone: "success", message: "Body metric entry updated." });
      } else {
        await createMetric.mutateAsync(payload);
        setFormFeedback({ tone: "success", message: "Body metric entry added." });
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : "Could not save the body metric entry.";
      setFormFeedback({ tone: "warning", message });
      return;
    }

    resetForm(false);
  }

  const recentEntries = metricsData.entries.slice(0, 6);

  return (
    <div className="space-y-6">
      <PageHeader
        eyebrow="Body composition"
        title="Body Metrics"
        description="Log the measurements that matter, edit them cleanly, and use the trend cards as confirmation instead of guesswork."
        chips={[{ label: "Add + edit live", tone: "success" }, { label: "Trend aware", tone: "secondary" }]}
      />

      <div className="grid gap-6 xl:grid-cols-[0.92fr_1.08fr]">
        <div ref={formSectionRef}>
          <SectionCard
            title={formTitle}
            description={formDescription}
            action={<StatusChip label={editingId ? `Editing #${editingId}` : "New entry"} tone={editingId ? "warning" : "success"} />}
          >
            <div className="space-y-5">
              {formFeedback ? (
                <div className="rounded-[1.15rem] border border-white/6 bg-white/[0.03] px-4 py-3">
                  <StatusChip label={formFeedback.tone === "success" ? "Saved" : "Needs attention"} tone={formFeedback.tone} />
                  <p className="mt-2 text-sm leading-6 text-muted-foreground">{formFeedback.message}</p>
                </div>
              ) : null}

              <div className="grid gap-3 sm:grid-cols-2">
                <Field
                  icon={<Weight className="size-4 text-primary" />}
                  label="Date"
                  type="date"
                  value={form.date}
                  onChange={(value) => updateField("date", value)}
                />
                <Field
                  icon={<Weight className="size-4 text-primary" />}
                  label="Weight (kg)"
                  placeholder="78.5"
                  value={form.bodyWeight}
                  onChange={(value) => updateField("bodyWeight", value)}
                />
                <Field label="Waist (cm)" placeholder="82" value={form.waist} onChange={(value) => updateField("waist", value)} />
                <Field label="Hips (cm)" placeholder="96" value={form.hips} onChange={(value) => updateField("hips", value)} />
                <Field label="Chest (cm)" placeholder="102" value={form.chest} onChange={(value) => updateField("chest", value)} />
                <Field label="Arms (cm)" placeholder="36" value={form.arms} onChange={(value) => updateField("arms", value)} />
                <Field label="Thighs (cm)" placeholder="58" value={form.thighs} onChange={(value) => updateField("thighs", value)} />
                <Field label="Neck (cm)" placeholder="38" value={form.neck} onChange={(value) => updateField("neck", value)} />
                <Field label="Body fat %" placeholder="18" value={form.bodyFat} onChange={(value) => updateField("bodyFat", value)} />
              </div>

              <Textarea
                onChange={(event) => updateField("notes", event.target.value)}
                placeholder="Optional note: lower waist this week, weight up from sodium, chest pump measurement, etc."
                value={form.notes}
              />

              <div className="flex flex-col gap-3 sm:flex-row">
                <Button className="gap-2 sm:flex-1" disabled={isSaving} onClick={() => void handleSubmit()}>
                  {editingId ? <Save className="size-4" /> : <Plus className="size-4" />}
                  {isSaving ? "Saving..." : editingId ? "Update entry" : "Add entry"}
                </Button>
                <Button className="sm:flex-1" disabled={isSaving} onClick={() => resetForm()} variant="outline">
                  {editingId ? "Cancel edit" : "Reset form"}
                </Button>
              </div>
            </div>
          </SectionCard>
        </div>

        <SectionCard
          title="Recent entries"
          description="Use edit on the exact row you want to change. The form on the left will load that entry."
          action={<StatusChip label={`${metricsData.entries.length} total entries`} tone="secondary" />}
        >
          <div className="space-y-3">
            {!recentEntries.length ? (
              <div className="rounded-[1.2rem] border border-dashed border-white/10 bg-white/[0.02] p-5">
                <p className="text-sm font-semibold">No body-metric entries yet.</p>
                <p className="mt-2 text-sm leading-6 text-muted-foreground">
                  Add your day 1 weight and measurements on the left first. After that, edit will work from this recent-entries list.
                </p>
              </div>
            ) : null}
            {recentEntries.map((entry) => (
              <div
                className={`rounded-[1.35rem] border p-4 transition ${
                  editingId === entry.id
                    ? "border-warning/35 bg-warning/10 ring-1 ring-warning/20"
                    : "border-white/6 bg-white/[0.03]"
                }`}
                key={entry.id}
              >
                <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                  <div className="space-y-3">
                    <div className="flex flex-wrap items-center gap-2">
                      <p className="text-base font-semibold">{entry.date}</p>
                      <StatusChip label={entry.bodyWeight != null ? `${entry.bodyWeight} kg` : "No weight"} tone="success" />
                      <StatusChip label={entry.waist != null ? `${entry.waist} cm waist` : "No waist"} tone="neutral" />
                      {editingId === entry.id ? <StatusChip label="Editing now" tone="warning" /> : null}
                    </div>
                    <div className="grid gap-2 sm:grid-cols-4">
                      <MetricChip label="Hips" value={entry.hips} />
                      <MetricChip label="Chest" value={entry.chest} />
                      <MetricChip label="Arms" value={entry.arms} />
                      <MetricChip label="Thighs" value={entry.thighs} />
                    </div>
                    <p className="text-sm leading-6 text-muted-foreground">{entry.progressNotes || entry.notes || "No notes on this entry."}</p>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    <Button className="gap-2" onClick={() => startEdit(entry.id)} variant="outline">
                      <Pencil className="size-4" />
                      Edit
                    </Button>
                    <Button
                      className="gap-2"
                      disabled={deleteMetric.isPending}
                      onClick={() =>
                        deleteMetric.mutate(entry.id, {
                          onSuccess: () => {
                            if (editingId === entry.id) {
                              resetForm(false);
                              setFormFeedback({ tone: "warning", message: "The entry you were editing was deleted. The form is ready for a new entry now." });
                            }
                          },
                        })
                      }
                      variant="ghost"
                    >
                      <Trash2 className="size-4" />
                      Delete
                    </Button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </SectionCard>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {metricsData.currentStats.map((stat) => (
          <MetricsComparisonCard key={stat.label} stat={stat} />
        ))}
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        {metricsData.trends.map((trend) => (
          <TrendSummaryCard key={trend.title} trend={trend} />
        ))}
      </div>

      <div className="grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
        <SectionCard title="Weekly change cards" description="A short read on what moved this week.">
          <div className="grid gap-4 md:grid-cols-3">
            {metricsData.weeklyChanges.map((item) => (
              <div className="rounded-[1.3rem] border border-white/6 bg-white/[0.03] p-4" key={item.label}>
                <p className="text-xs uppercase tracking-[0.16em] text-muted-foreground">{item.label}</p>
                <p className="mt-3 text-2xl font-black tracking-tight">{item.value}</p>
                <p className="mt-2 text-sm leading-6 text-muted-foreground">{item.note}</p>
              </div>
            ))}
          </div>
        </SectionCard>

        <SectionCard title="Milestones" description="The next visible targets worth caring about.">
          <div className="space-y-3">
            {metricsData.milestones.map((milestone) => (
              <div className="rounded-[1.2rem] border border-white/6 bg-white/[0.03] p-4" key={milestone.id}>
                <div className="flex items-center justify-between gap-3">
                  <p className="text-sm font-semibold">{milestone.title}</p>
                  <StatusChip label={milestone.status} tone={milestone.status === "Reached" ? "success" : milestone.status === "Close" ? "warning" : "neutral"} />
                </div>
                <p className="mt-2 text-sm leading-6 text-muted-foreground">{milestone.note}</p>
              </div>
            ))}
          </div>
        </SectionCard>
      </div>
    </div>
  );
}

function parseOptionalNumber(value: string) {
  const trimmed = value.trim();
  if (!trimmed) return null;
  const parsed = Number.parseFloat(trimmed);
  return Number.isNaN(parsed) ? null : parsed;
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
  icon?: ReactNode;
}) {
  return (
    <label className="rounded-[1.2rem] border border-white/6 bg-black/10 p-3">
      <div className="flex items-center gap-2 text-[0.68rem] uppercase tracking-[0.18em] text-muted-foreground">
        {icon ?? <Ruler className="size-4" />}
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

function MetricChip({ label, value }: { label: string; value: number | null }) {
  return (
    <div className="rounded-[1rem] border border-white/6 bg-black/10 px-3 py-3">
      <p className="text-[0.68rem] uppercase tracking-[0.16em] text-muted-foreground">{label}</p>
      <p className="mt-2 text-sm font-semibold">{value != null ? `${value}` : "—"}</p>
    </div>
  );
}
