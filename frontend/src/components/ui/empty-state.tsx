import { Inbox } from 'lucide-react'

interface EmptyStateProps {
  title?: string
  message?: string
  action?: React.ReactNode
}

export function EmptyState({
  title = 'Sin datos',
  message = 'No hay contenido para mostrar en esta seccion.',
  action,
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      <Inbox className="h-12 w-12 text-muted-foreground mb-4" />
      <p className="text-lg font-medium text-foreground mb-1">{title}</p>
      <p className="text-sm text-muted-foreground mb-6 max-w-xs">{message}</p>
      {action}
    </div>
  )
}
