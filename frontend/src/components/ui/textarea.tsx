import { cn } from '@/lib/utils'
import type { TextareaHTMLAttributes } from 'react'

interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {}

export function Textarea({ className, ...props }: TextareaProps) {
  return (
    <textarea
      className={cn(
        'w-full rounded-lg border border-border bg-card px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground/60 focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all min-h-[100px] resize-y',
        className
      )}
      {...props}
    />
  )
}
