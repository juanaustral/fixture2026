import { cn } from '@/lib/utils'

// Base skeleton: animated pulse block
export function Skeleton({ className }: { className?: string }) {
  return (
    <div
      className={cn(
        'animate-pulse rounded-lg bg-gradient-to-r from-muted via-muted/60 to-muted bg-[length:200%_100%]',
        className,
      )}
    />
  )
}

// Card skeleton (rectangular card shape)
export function CardSkeleton() {
  return (
    <div className="rounded-xl border border-border bg-card p-6 space-y-4">
      <Skeleton className="h-5 w-3/5" />
      <Skeleton className="h-8 w-full" />
      <Skeleton className="h-4 w-4/5" />
      <div className="flex gap-2 pt-2">
        <Skeleton className="h-8 w-20 rounded-md" />
        <Skeleton className="h-8 w-20 rounded-md" />
      </div>
    </div>
  )
}

// Table skeleton: header + rows with variable widths
export function TableSkeleton({ rows = 5 }: { rows?: number }) {
  const widths = ['w-3/12', 'w-5/12', 'w-2/12', 'w-2/12']
  return (
    <div className="space-y-3">
      {/* Header */}
      <div className="flex gap-4 pb-2 border-b border-border">
        {widths.map((w, i) => (
          <Skeleton key={`h-${i}`} className={`h-4 ${w}`} />
        ))}
      </div>
      {/* Rows */}
      {Array.from({ length: rows }).map((_, r) => (
        <div key={r} className="flex gap-4 py-2 border-b border-border/50">
          {widths.map((w, i) => (
            <Skeleton key={`r${r}-${i}`} className={`h-4 ${w}`} />
          ))}
        </div>
      ))}
    </div>
  )
}

// List skeleton: avatar + text lines
export function ListSkeleton({ items = 4 }: { items?: number }) {
  return (
    <div className="space-y-3">
      {Array.from({ length: items }).map((_, i) => (
        <div key={i} className="flex items-center gap-3 p-3 rounded-lg">
          <Skeleton className="h-10 w-10 rounded-full shrink-0" />
          <div className="flex-1 space-y-2">
            <Skeleton className="h-4 w-3/5" />
            <Skeleton className="h-3 w-4/5" />
          </div>
        </div>
      ))}
    </div>
  )
}
