import { cn } from '@/lib/utils'
import type { InputHTMLAttributes } from 'react'

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {}

export function Input({ className, ...props }: InputProps) {
  return (
    <input
      className={cn(
        'w-full rounded-lg border border-border bg-card px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground/60 focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all',
        className
      )}
      {...props}
    />
  )
}
