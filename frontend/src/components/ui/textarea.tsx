import * as React from "react";

import { cn } from "@/lib/utils";

export const Textarea = React.forwardRef<HTMLTextAreaElement, React.TextareaHTMLAttributes<HTMLTextAreaElement>>(
  ({ className, ...props }, ref) => (
    <textarea
      ref={ref}
      className={cn(
        "min-h-28 w-full rounded-[1.2rem] border border-white/8 bg-white/[0.03] px-4 py-3 text-sm text-foreground outline-none transition focus-visible:ring-2 focus-visible:ring-ring placeholder:text-muted-foreground/70",
        className,
      )}
      {...props}
    />
  ),
);

Textarea.displayName = "Textarea";

