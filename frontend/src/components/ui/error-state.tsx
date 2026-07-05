import { AlertTriangle, RefreshCw } from 'lucide-react'

interface ErrorStateProps {
  message?: string
  onRetry?: () => void
}

export function ErrorState({
  message = 'Ocurrio un error inesperado',
  onRetry,
}: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      <AlertTriangle className="h-12 w-12 text-red-500 mb-4" />
      <p className="text-lg font-medium text-foreground mb-1">Algo salio mal</p>
      <p className="text-sm text-muted-foreground mb-6 max-w-xs">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-primary text-white text-sm font-medium hover:bg-primary-dark transition-colors"
        >
          <RefreshCw size={16} />
          Intentar de nuevo
        </button>
      )}
    </div>
  )
}
