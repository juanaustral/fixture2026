import { cn } from '@/lib/utils'
import { ChevronDown } from 'lucide-react'
import type { SelectHTMLAttributes } from 'react'

interface SelectProps extends SelectHTMLAttributes<HTMLSelectElement> {
  options: { value: string; label: string }[]
}

export function Select({ className, options, ...props }: SelectProps) {
  return (
    <div className="relative">
      <select
        className={cn(
          'w-full rounded-lg border border-border bg-card px-3 py-2 text-sm text-foreground appearance-none focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all pr-8',
          className
        )}
        {...props}
      >
        {options.map(opt => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
      <ChevronDown size={16} className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground pointer-events-none" />
    </div>
  )
}
