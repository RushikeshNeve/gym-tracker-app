import { cva } from "class-variance-authority";

import { cn } from "@/lib/utils";

const chipVariants = cva(
  "inline-flex items-center gap-2 rounded-full px-3 py-1 text-[0.68rem] font-semibold uppercase tracking-[0.18em]",
  {
    variants: {
      tone: {
        neutral: "bg-white/6 text-muted-foreground ring-1 ring-white/8",
        success: "bg-primary/12 text-primary ring-1 ring-primary/18",
        secondary: "bg-secondary/12 text-secondary ring-1 ring-secondary/18",
        warning: "bg-[rgba(255,209,111,0.12)] text-warning ring-1 ring-[rgba(255,209,111,0.18)]",
        danger: "bg-[rgba(255,122,99,0.12)] text-danger ring-1 ring-[rgba(255,122,99,0.18)]",
      },
    },
    defaultVariants: {
      tone: "neutral",
    },
  },
);

export function StatusChip({
  label,
  tone = "neutral",
  className,
}: {
  label: string;
  tone?: "neutral" | "success" | "secondary" | "warning" | "danger";
  className?: string;
}) {
  return <span className={cn(chipVariants({ tone }), className)}>{label}</span>;
}

