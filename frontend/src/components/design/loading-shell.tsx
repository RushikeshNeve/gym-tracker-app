import { Skeleton } from "@/components/ui/skeleton";

export function LoadingShell() {
  return (
    <div className="space-y-6">
      <Skeleton className="h-52 w-full rounded-[2rem]" />
      <div className="grid gap-4 md:grid-cols-4">
        {Array.from({ length: 4 }).map((_, index) => (
          <Skeleton className="h-32 w-full rounded-[1.5rem]" key={index} />
        ))}
      </div>
      <div className="grid gap-4 xl:grid-cols-2">
        <Skeleton className="h-80 w-full rounded-[1.8rem]" />
        <Skeleton className="h-80 w-full rounded-[1.8rem]" />
      </div>
    </div>
  );
}

