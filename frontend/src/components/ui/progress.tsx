import { cn } from '@/lib/utils'

interface ProgressProps {
  value: number
  max?: number
  className?: string
  barClassName?: string
  label?: string
}

export function Progress({ value, max = 100, className, barClassName, label }: ProgressProps) {
  const pct = Math.min(Math.round((value / max) * 100), 100)

  return (
    <div className={cn('space-y-1', className)}>
      {label && (
        <div className="flex justify-between text-xs text-muted-foreground">
          <span>{label}</span>
          <span>{pct}%</span>
        </div>
      )}
      <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
        <div
          className={cn(
            'h-full rounded-full transition-all duration-500',
            pct > 80 ? 'bg-red-500' : pct > 50 ? 'bg-yellow-500' : 'bg-primary',
            barClassName
          )}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  )
}
