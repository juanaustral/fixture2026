import { useState, useEffect, useCallback } from 'react'
import { apiFetch } from '@/lib/api'

interface UseApiResult<T> {
  data: T | null
  loading: boolean
  error: string | null
  refetch: () => void
}

export function useApi<T>(url: string): UseApiResult<T> {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchData = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await apiFetch<T>(url)
      setData(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido')
      setData(null)
    } finally {
      setLoading(false)
    }
  }, [url])

  useEffect(() => {
    fetchData()
  }, [fetchData])

  return { data, loading, error, refetch: fetchData }
}
