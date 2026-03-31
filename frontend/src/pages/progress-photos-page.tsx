import { useRef, useState } from "react";
import { Camera, CheckCircle2, Images, UploadCloud } from "lucide-react";

import { ErrorState } from "@/components/design/error-state";
import { LoadingShell } from "@/components/design/loading-shell";
import { PhotoComparisonCard } from "@/components/design/photo-comparison-card";
import { SectionCard } from "@/components/design/section-card";
import { StatusChip } from "@/components/design/status-chip";
import { PageHeader } from "@/components/layout/page-header";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useProgressPhotosPage, useUploadProgressPhoto } from "@/hooks/use-progress-photos-page";
import { getTodayDateString } from "@/lib/date";

export function ProgressPhotosPage() {
  const inputRef = useRef<HTMLInputElement | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [notes, setNotes] = useState("");
  const [selectedPhotoType, setSelectedPhotoType] = useState<"Front" | "Side" | "Back">("Front");
  const { data, isLoading, isError, refetch } = useProgressPhotosPage();
  const uploadPhoto = useUploadProgressPhoto();
  if (isLoading) return <LoadingShell />;
  if (isError || !data) return <ErrorState title="Progress photos could not load" description="Photo metadata did not arrive from the API." onRetry={() => void refetch()} />;
  const progressPhotosData = data;

  return (
    <div className="space-y-6">
      <PageHeader
        eyebrow="Visual proof"
        title="Progress Photos"
        description="Choose the photo view first, keep uploads organized, and make comparison much easier to trust."
        chips={[{ label: "Front / side / back", tone: "secondary" }, { label: progressPhotosData.todayStatus, tone: "warning" }]}
      />

      <div className="grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
        <SectionCard
          title="Upload photo"
          description="Pick the view before you upload. That is how you decide whether the image is a front, side, or back progress shot."
          action={<StatusChip label={selectedPhotoType} tone="success" />}
        >
          <div className="space-y-5">
            <div className="grid gap-3 sm:grid-cols-3">
              {(["Front", "Side", "Back"] as const).map((type) => (
                <button
                  className={`rounded-[1.3rem] border p-4 text-left transition ${
                    selectedPhotoType === type
                      ? "border-primary/20 bg-[linear-gradient(180deg,rgba(151,255,147,0.10),rgba(17,18,22,0.96))] shadow-[0_14px_28px_rgba(0,0,0,0.16)]"
                      : "border-white/6 bg-white/[0.03]"
                  }`}
                  key={type}
                  onClick={() => setSelectedPhotoType(type)}
                  type="button"
                >
                  <div className="flex items-center justify-between gap-3">
                    <p className="text-base font-semibold">{type} view</p>
                    {selectedPhotoType === type ? <CheckCircle2 className="size-4 text-primary" /> : null}
                  </div>
                  <p className="mt-2 text-sm leading-6 text-muted-foreground">
                    {type === "Front"
                      ? "Best for overall physique change and body symmetry."
                      : type === "Side"
                        ? "Best for waistline, posture, and midsection change."
                        : "Best for back width, rear delts, and overall back shape."}
                  </p>
                  <p className="mt-3 text-xs uppercase tracking-[0.16em] text-muted-foreground">
                    Today: {type === "Front" ? progressPhotosData.todayCounts.front : type === "Side" ? progressPhotosData.todayCounts.side : progressPhotosData.todayCounts.back}
                  </p>
                </button>
              ))}
            </div>

            <div className="rounded-[1.7rem] border border-dashed border-white/10 bg-white/[0.03] p-8 text-center">
              <div className="mx-auto flex size-14 items-center justify-center rounded-[1.2rem] bg-secondary/10 text-secondary">
                <UploadCloud className="size-6" />
              </div>
              <p className="mt-4 text-lg font-semibold">Upload {selectedPhotoType.toLowerCase()} photo</p>
              <p className="mt-2 text-sm leading-6 text-muted-foreground">
                Choose the view first, then pick the file that matches it. That is how you control what view the photo is saved as.
              </p>
              <input
                className="hidden"
                accept="image/png,image/jpeg,image/webp"
                onChange={(event) => setSelectedFile(event.target.files?.[0] ?? null)}
                ref={inputRef}
                type="file"
              />
              <div className="mt-5 flex justify-center">
                <Button onClick={() => inputRef.current?.click()}>Choose {selectedPhotoType.toLowerCase()} photo</Button>
              </div>
              {selectedFile ? (
                <div className="mt-5 rounded-[1.2rem] border border-white/6 bg-black/10 p-4 text-left">
                  <p className="text-[0.68rem] uppercase tracking-[0.18em] text-muted-foreground">Selected files</p>
                  <div className="mt-3 space-y-3">
                    <div className="flex items-center justify-between gap-3 rounded-[1rem] border border-white/6 bg-white/[0.03] px-3 py-3">
                      <p className="text-sm font-medium">{selectedFile.name}</p>
                      <StatusChip label={selectedPhotoType} tone="secondary" />
                    </div>
                    <Textarea
                      onChange={(event) => setNotes(event.target.value)}
                      placeholder="Optional note: morning fasted shot, same lighting, post-workout pumped, etc."
                      value={notes}
                    />
                    <Button
                      disabled={uploadPhoto.isPending}
                      onClick={() =>
                        uploadPhoto.mutate(
                          {
                            file: selectedFile,
                            logDate: getTodayDateString(),
                            photoType: selectedPhotoType,
                            notes,
                          },
                          {
                            onSuccess: () => {
                              setSelectedFile(null);
                              setNotes("");
                              if (inputRef.current) {
                                inputRef.current.value = "";
                              }
                            },
                          },
                        )
                      }
                    >
                      {uploadPhoto.isPending ? "Uploading..." : `Upload ${selectedPhotoType.toLowerCase()} photo`}
                    </Button>
                  </div>
                </div>
              ) : null}
            </div>

            <div className="grid gap-3 sm:grid-cols-3">
              <MiniStat label="Front today" value={`${progressPhotosData.todayCounts.front}`} />
              <MiniStat label="Side today" value={`${progressPhotosData.todayCounts.side}`} />
              <MiniStat label="Back today" value={`${progressPhotosData.todayCounts.back}`} />
            </div>
          </div>
        </SectionCard>

        <div className="space-y-6">
          <PhotoComparisonCard pair={progressPhotosData.comparisonPair} />

          <SectionCard
            title="Photo flow"
            description="Keep the process repeatable so your gallery stays useful."
            action={<StatusChip label={progressPhotosData.selectedDate} tone="secondary" />}
          >
            <div className="grid gap-3 md:grid-cols-3">
              <FlowCard title="1. Pick view" note="Tap Front, Side, or Back before you open the file picker." />
              <FlowCard title="2. Upload matching shot" note="The selected file should match the chosen view." />
              <FlowCard title="3. Compare honestly" note="Use the comparison panel and gallery to track visible changes over time." />
            </div>
          </SectionCard>
        </div>
      </div>

      <SectionCard
        title="Recent gallery"
        description="A cleaner gallery of recent progress shots with the view tag visible at a glance."
        action={<StatusChip label={progressPhotosData.selectedDate} tone="secondary" />}
      >
        <div className="grid gap-4 md:grid-cols-2 2xl:grid-cols-3">
          {progressPhotosData.gallery.map((photo) => (
            <div className="rounded-[1.45rem] border border-white/6 bg-[linear-gradient(180deg,rgba(255,255,255,0.04),rgba(18,20,24,0.96))] p-4" key={photo.id}>
              <div className="aspect-[4/5] rounded-[1.1rem] border border-white/6 bg-[linear-gradient(135deg,rgba(151,255,147,0.08),rgba(18,20,24,0.96))]">
                {photo.url ? (
                  <img alt={`${photo.photoType} progress photo from ${photo.dateLabel}`} className="h-full w-full rounded-[1.1rem] object-cover" src={photo.url} />
                ) : (
                  <div className="flex h-full items-center justify-center text-muted-foreground">
                    <Camera className="size-7" />
                  </div>
                )}
              </div>
              <div className="mt-4 flex items-start justify-between gap-3">
                <div>
                  <p className="text-sm font-semibold">{photo.dateLabel}</p>
                  <p className="mt-1 max-w-[15rem] truncate text-sm text-muted-foreground">{photo.url}</p>
                </div>
                <StatusChip label={photo.photoType} tone="secondary" />
              </div>
            </div>
          ))}
        </div>
      </SectionCard>
    </div>
  );
}

function MiniStat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-[1.15rem] border border-white/6 bg-black/10 px-4 py-4">
      <p className="text-[0.68rem] uppercase tracking-[0.18em] text-muted-foreground">{label}</p>
      <p className="mt-2 text-xl font-semibold">{value}</p>
    </div>
  );
}

function FlowCard({ title, note }: { title: string; note: string }) {
  return (
    <div className="rounded-[1.2rem] border border-white/6 bg-white/[0.03] p-4">
      <div className="flex items-center gap-2 text-sm font-semibold">
        <Images className="size-4 text-secondary" />
        {title}
      </div>
      <p className="mt-3 text-sm leading-6 text-muted-foreground">{note}</p>
    </div>
  );
}
