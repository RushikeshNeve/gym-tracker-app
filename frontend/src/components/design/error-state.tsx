import { TriangleAlert } from "lucide-react";

import { Button } from "@/components/ui/button";

export function ErrorState({
  title,
  description,
  onRetry,
}: {
  title: string;
  description: string;
  onRetry?: () => void;
}) {
  return (
    <div className="rounded-[1.5rem] border border-[rgba(255,122,99,0.18)] bg-[rgba(255,122,99,0.05)] p-8 text-center">
      <div className="mx-auto flex size-12 items-center justify-center rounded-full bg-[rgba(255,122,99,0.10)] text-danger">
        <TriangleAlert className="size-5" />
      </div>
      <h3 className="mt-4 text-lg font-semibold">{title}</h3>
      <p className="mt-2 text-sm text-muted-foreground">{description}</p>
      {onRetry ? (
        <div className="mt-5 flex justify-center">
          <Button onClick={onRetry} variant="outline">
            Retry
          </Button>
        </div>
      ) : null}
    </div>
  );
}
