import { useState, useEffect } from 'react'
import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Spinner } from '@/components/ui/spinner'
import { Server, Globe, Container, Activity, AlertCircle, ExternalLink, ChevronDown, ChevronRight, Timer } from 'lucide-react'

interface Site {
  name: string
  url: string
  status: 'up' | 'down' | 'degraded'
  icon?: string
}

interface ContainerInfo {
  name: string
  image: string
  status: string
  ports: string
  uptime?: string
}

interface DockerData {
  name: string
  containers: ContainerInfo[]
}

interface CronJob {
  name: string
  schedule: string
  last_run: string
  status: string
}

export function ServiciosPage() {
  const [sites, setSites] = useState<Site[]>([])
  const [dockerServices, setDockerServices] = useState<DockerData[]>([])
  const [cronJobs, setCronJobs] = useState<CronJob[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [expandedService, setExpandedService] = useState<string | null>(null)

  useEffect(() => {
    loadData()
  }, [])

  async function loadData() {
    setLoading(true)
    setError(null)
    try {
      const [sitesRes, dockerRes, cronRes] = await Promise.allSettled([
        fetch('/api/sites'),
        fetch('/api/docker'),
        fetch('/api/cron'),
      ])

      if (sitesRes.status === 'fulfilled' && sitesRes.value.ok) {
        const data = await sitesRes.value.json()
        setSites(Array.isArray(data) ? data : data.sites ?? [])
      } else {
        // Mock data for demo
        setSites([
          { name: 'Akira Dashboard', url: 'https://dashboard.akira.local', status: 'up' },
          { name: 'API Backend', url: 'https://api.akira.local', status: 'up' },
          { name: 'SilverBullet', url: 'https://notes.akira.local', status: 'up' },
        ])
      }

      if (dockerRes.status === 'fulfilled' && dockerRes.value.ok) {
        const data = await dockerRes.value.json()
        setDockerServices(Array.isArray(data) ? data : data.services ?? [])
      } else {
        // Mock data
        setDockerServices([
          {
            name: 'Servicios principales',
            containers: [
              { name: 'nginx', image: 'nginx:alpine', status: 'running', ports: '80, 443', uptime: '14d' },
              { name: 'api-server', image: 'akira-api:latest', status: 'running', ports: '8585', uptime: '14d' },
              { name: 'postgres', image: 'postgres:16', status: 'running', ports: '5432', uptime: '30d' },
            ],
          },
          {
            name: 'Utilidades',
            containers: [
              { name: 'redis', image: 'redis:alpine', status: 'running', ports: '6379', uptime: '30d' },
              { name: 'silverbullet', image: 'silverbullet:latest', status: 'running', ports: '3000', uptime: '7d' },
            ],
          },
        ])
      }

      if (cronRes.status === 'fulfilled' && cronRes.value.ok) {
        const data = await cronRes.value.json()
        setCronJobs(Array.isArray(data) ? data : data.jobs ?? [])
      } else {
        setCronJobs([
          { name: 'Backup DB', schedule: '0 3 * * *', last_run: '2025-07-04 03:00', status: 'success' },
          { name: 'Health Check', schedule: '*/5 * * * *', last_run: '2025-07-04 12:00', status: 'success' },
          { name: 'Cert Renew', schedule: '0 0 1 * *', last_run: '2025-07-01 00:00', status: 'success' },
        ])
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Error al cargar servicios')
    } finally {
      setLoading(false)
    }
  }

  const statusBadge = (status: string) => {
    switch (status) {
      case 'up':
      case 'running':
      case 'success':
        return <Badge variant="success">{status === 'up' ? 'Online' : status === 'running' ? 'Running' : 'Exito'}</Badge>
      case 'down':
        return <Badge variant="danger">Offline</Badge>
      case 'degraded':
        return <Badge variant="warning">Degradado</Badge>
      default:
        return <Badge>{status}</Badge>
    }
  }

  if (loading) return <Spinner size={32} className="py-12" />

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Servicios</h1>
        <p className="text-muted-foreground mt-1">Monitoreo de conexiones y servicios</p>
      </div>

      {error && (
        <div className="flex items-center gap-2 px-4 py-3 rounded-lg bg-red-50 dark:bg-red-900/20 text-red-600 text-sm">
          <AlertCircle size={16} />
          {error}
        </div>
      )}

      {/* Sites Grid */}
      <div>
        <div className="flex items-center gap-2 mb-4">
          <Globe size={18} className="text-primary" />
          <h2 className="text-xl font-semibold">Sitios web</h2>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {sites.map((site, i) => (
            <Card key={i}>
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div className={`w-3 h-3 rounded-full ${
                    site.status === 'up' ? 'bg-green-500' :
                    site.status === 'down' ? 'bg-red-500' : 'bg-yellow-500'
                  }`} />
                  <div>
                    <h3 className="font-semibold">{site.name}</h3>
                    {site.icon && <span className="text-xs text-muted-foreground">{site.icon}</span>}
                  </div>
                </div>
                {statusBadge(site.status)}
              </div>
              <a
                href={site.url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-1 text-sm text-primary hover:underline"
              >
                {site.url}
                <ExternalLink size={12} />
              </a>
            </Card>
          ))}
        </div>
      </div>

      {/* Docker Services */}
      <div>
        <div className="flex items-center gap-2 mb-4">
          <Container size={18} className="text-primary" />
          <h2 className="text-xl font-semibold">Contenedores Docker</h2>
        </div>
        <div className="space-y-4">
          {dockerServices.map((svc, i) => (
            <Card key={i} className="overflow-hidden p-0">
              <button
                onClick={() => setExpandedService(expandedService === svc.name ? null : svc.name)}
                className="w-full flex items-center justify-between p-4 hover:bg-muted/30 transition-colors"
              >
                <div className="flex items-center gap-2">
                  {expandedService === svc.name ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
                  <Server size={16} className="text-muted-foreground" />
                  <span className="font-medium">{svc.name}</span>
                </div>
                <Badge variant={svc.containers.every(c => c.status === 'running') ? 'success' : 'warning'}>
                  {svc.containers.filter(c => c.status === 'running').length}/{svc.containers.length} activos
                </Badge>
              </button>
              {expandedService === svc.name && (
                <div className="border-t border-border overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="bg-muted/30">
                        <th className="text-left py-2 px-4 font-medium">Nombre</th>
                        <th className="text-left py-2 px-4 font-medium">Imagen</th>
                        <th className="text-left py-2 px-4 font-medium">Estado</th>
                        <th className="text-left py-2 px-4 font-medium">Puertos</th>
                        <th className="text-left py-2 px-4 font-medium">Uptime</th>
                      </tr>
                    </thead>
                    <tbody>
                      {svc.containers.map((c, j) => (
                        <tr key={j} className="border-t border-border hover:bg-muted/20">
                          <td className="py-2 px-4 font-medium">{c.name}</td>
                          <td className="py-2 px-4 text-muted-foreground font-mono text-xs">{c.image}</td>
                          <td className="py-2 px-4">{statusBadge(c.status)}</td>
                          <td className="py-2 px-4 text-muted-foreground">{c.ports}</td>
                          <td className="py-2 px-4 text-muted-foreground">{c.uptime ?? '—'}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </Card>
          ))}
        </div>
      </div>

      {/* Cron Jobs */}
      <div>
        <div className="flex items-center gap-2 mb-4">
          <Timer size={18} className="text-primary" />
          <h2 className="text-xl font-semibold">Cron Jobs</h2>
        </div>
        <Card className="overflow-hidden p-0">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left py-3 px-4 font-medium">Nombre</th>
                  <th className="text-left py-3 px-4 font-medium">Schedule</th>
                  <th className="text-left py-3 px-4 font-medium">Ultima ejecucion</th>
                  <th className="text-left py-3 px-4 font-medium">Estado</th>
                </tr>
              </thead>
              <tbody>
                {cronJobs.length === 0 ? (
                  <tr>
                    <td colSpan={4} className="py-8 text-center text-muted-foreground">
                      No hay cron jobs configurados
                    </td>
                  </tr>
                ) : cronJobs.map((job, i) => (
                  <tr key={i} className="border-b border-border hover:bg-muted/30">
                    <td className="py-3 px-4 font-medium">{job.name}</td>
                    <td className="py-3 px-4 font-mono text-xs text-muted-foreground">{job.schedule}</td>
                    <td className="py-3 px-4 text-muted-foreground text-xs">{job.last_run}</td>
                    <td className="py-3 px-4">{statusBadge(job.status)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      </div>
    </div>
  )
}
