import { cn } from '@/lib/utils'
import type { ReactNode } from 'react'

interface TabsProps {
  tabs: { id: string; label: string }[]
  active: string
  onChange: (id: string) => void
  className?: string
}

export function Tabs({ tabs, active, onChange, className }: TabsProps) {
  return (
    <div className={cn('flex gap-1 bg-muted/50 p-1 rounded-lg', className)}>
      {tabs.map(tab => (
        <button
          key={tab.id}
          onClick={() => onChange(tab.id)}
          className={cn(
            'px-4 py-2 text-sm font-medium rounded-md transition-all',
            active === tab.id
              ? 'bg-card text-foreground shadow-sm'
              : 'text-muted-foreground hover:text-foreground'
          )}
        >
          {tab.label}
        </button>
      ))}
    </div>
  )
}

interface TabContentProps {
  active: string
  id: string
  children: ReactNode
}

export function TabContent({ active, id, children }: TabContentProps) {
  if (active !== id) return null
  return <div>{children}</div>
}
