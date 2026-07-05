import { useState, useEffect } from 'react'
import { useTheme } from '@/providers/ThemeProvider'
import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { Spinner } from '@/components/ui/spinner'
import { Sun, Moon, FileText, DollarSign, List, Calendar, Server, Bot, Activity, CreditCard, AlertCircle } from 'lucide-react'
import { useNavigate } from 'react-router'

const quickLinks = [
  { to: '/notas', icon: FileText, label: 'Notas', desc: 'Toma notas y documentacion' },
  { to: '/finanzas', icon: DollarSign, label: 'Finanzas', desc: 'Gastos y suscripciones' },
  { to: '/listas', icon: List, label: 'Listas', desc: 'Peliculas, series y mas' },
  { to: '/calendario', icon: Calendar, label: 'Calendario', desc: 'Eventos y recordatorios' },
  { to: '/servicios', icon: Server, label: 'Servicios', desc: 'Monitoreo de VPS' },
  { to: '/akira', icon: Bot, label: 'Akira', desc: 'Agentes e IA' },
]

interface VpsData {
  cpu?: number
  ram?: number
  disco?: number
}

interface NotasCount {
  count: number
}

interface SitesData {
  count: number
}

interface CalendarEvent {
  title: string
  date: string
  type: string
}

interface DashboardData {
  servicios_activos: number
  gastos_mes: number
  notas_recientes: number
  prox_vencimiento: string | null
  cpu?: number
  ram?: number
  disco?: number
  eventos?: CalendarEvent[]
}

export function HomePage() {
  const { theme, toggle } = useTheme()
  const navigate = useNavigate()
  const [data, setData] = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function load() {
      setLoading(true)
      setError(null)
      try {
        const results = await Promise.allSettled([
          fetch('/api/vps'),
          fetch('/api/notas'),
          fetch('/api/sites'),
          fetch('/api/calendar'),
        ])

        let servicios_activos = 0
        let gastos_mes = 0
        let notas_recientes = 0
        let prox_vencimiento: string | null = null
        let cpu: number | undefined
        let ram: number | undefined
        let disco: number | undefined
        let eventos: CalendarEvent[] | undefined

        // VPS — backend returns {cpu: "7.1", mem: {total, used}, disk: {total, used, pct}}
        if (results[0].status === 'fulfilled' && results[0].value.ok) {
          const vpsResp = await results[0].value.json()
          cpu = parseFloat(vpsResp.cpu) || 0
          const memTotal = parseInt(vpsResp.mem?.total) || 1
          const memUsed = parseInt(vpsResp.mem?.used) || 0
          ram = Math.round((memUsed / memTotal) * 100)
          const pctStr = vpsResp.disk?.pct || '0%'
          disco = parseInt(pctStr) || 0
          servicios_activos = cpu > 0 ? 1 : 0
        }

        // Notas — backend returns {notas: [{title, modified}, ...]}
        if (results[1].status === 'fulfilled' && results[1].value.ok) {
          const notasResp = await results[1].value.json()
          const lista = Array.isArray(notasResp) ? notasResp : notasResp.notas ?? []
          notas_recientes = lista.length
        }

        // Sites — backend returns {sites: [{name, url, status, icon}, ...]}
        if (results[2].status === 'fulfilled' && results[2].value.ok) {
          const sitesResp = await results[2].value.json()
          const lista = Array.isArray(sitesResp) ? sitesResp : sitesResp.sites ?? []
          servicios_activos = lista.filter((s: any) => s.status === 'up').length
        }

        // Calendar — backend returns {events: [{summary, start, location}], error?}
        if (results[3].status === 'fulfilled' && results[3].value.ok) {
          const calResp = await results[3].value.json()
          const raw: any[] = Array.isArray(calResp) ? calResp : calResp.events ?? []
          const mapped: CalendarEvent[] = raw.map((e: any) => ({ title: e.summary || e.title || '', date: e.start || e.date || '', type: 'evento' }))
          eventos = mapped
          if (mapped.length > 0) {
            const sorted = [...mapped].sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
            const next = sorted.find((e: any) => new Date(e.date) >= new Date())
            prox_vencimiento = next ? next.date : sorted[0].date
          }
        }

        setData({
          servicios_activos,
          gastos_mes,
          notas_recientes,
          prox_vencimiento,
          cpu,
          ram,
          disco,
          eventos,
        })
      } catch (e) {
        setError(e instanceof Error ? e.message : 'Error al cargar datos')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
          <p className="text-muted-foreground mt-1">Bienvenido de vuelta, Juan</p>
        </div>
        <button
          onClick={toggle}
          className="p-2.5 rounded-xl bg-card border border-border hover:bg-muted/50 transition-all"
        >
          {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
        </button>
      </div>

      {loading ? (
        <Spinner size={32} className="py-12" />
      ) : error ? (
        <Card className="p-6 text-center">
          <AlertCircle className="mx-auto mb-2 text-muted-foreground" size={32} />
          <p className="text-muted-foreground">{error}</p>
        </Card>
      ) : (
        <>
          {/* Stat Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <Card>
              <div className="flex items-center gap-3 mb-3">
                <div className="p-2 rounded-lg bg-green-100 dark:bg-green-900/30 text-green-600">
                  <Server size={20} />
                </div>
              </div>
              <p className="text-2xl font-bold">{data?.servicios_activos ?? 0}</p>
              <p className="text-sm text-muted-foreground mt-1">Servicios activos</p>
            </Card>
            <Card>
              <div className="flex items-center gap-3 mb-3">
                <div className="p-2 rounded-lg bg-blue-100 dark:bg-blue-900/30 text-blue-600">
                  <DollarSign size={20} />
                </div>
              </div>
              <p className="text-2xl font-bold">${data?.gastos_mes?.toFixed(2) ?? '0.00'}</p>
              <p className="text-sm text-muted-foreground mt-1">Gastos del mes</p>
            </Card>
            <Card>
              <div className="flex items-center gap-3 mb-3">
                <div className="p-2 rounded-lg bg-purple-100 dark:bg-purple-900/30 text-purple-600">
                  <FileText size={20} />
                </div>
              </div>
              <p className="text-2xl font-bold">{data?.notas_recientes ?? 0}</p>
              <p className="text-sm text-muted-foreground mt-1">Notas recientes</p>
            </Card>
            <Card>
              <div className="flex items-center gap-3 mb-3">
                <div className="p-2 rounded-lg bg-yellow-100 dark:bg-yellow-900/30 text-yellow-600">
                  <Calendar size={20} />
                </div>
              </div>
              <p className="text-2xl font-bold">{data?.prox_vencimiento ?? '—'}</p>
              <p className="text-sm text-muted-foreground mt-1">Prox. vencimiento</p>
            </Card>
          </div>

          {/* Quick Access Grid */}
          <div>
            <h2 className="text-xl font-semibold mb-4">Acceso rapido</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {quickLinks.map(link => (
                <button
                  key={link.to}
                  onClick={() => navigate(link.to)}
                  className="bg-card border border-border rounded-xl p-5 text-left hover:shadow-md hover:border-primary/30 transition-all group"
                >
                  <div className="flex items-center gap-3 mb-2">
                    <div className="p-2 rounded-lg bg-primary/10 text-primary group-hover:bg-primary/20 transition-colors">
                      <link.icon size={20} />
                    </div>
                    <span className="font-semibold">{link.label}</span>
                  </div>
                  <p className="text-sm text-muted-foreground">{link.desc}</p>
                </button>
              ))}
            </div>
          </div>

          {/* VPS Status */}
          {(data?.cpu !== undefined || data?.ram !== undefined || data?.disco !== undefined) && (
            <Card>
              <div className="flex items-center gap-2 mb-4">
                <Activity size={18} className="text-primary" />
                <h3 className="font-semibold">Estado del VPS</h3>
              </div>
              <div className="space-y-4">
                <Progress value={data.cpu ?? 0} label="CPU" />
                <Progress value={data.ram ?? 0} label="RAM" />
                <Progress value={data.disco ?? 0} label="Disco" />
              </div>
            </Card>
          )}

          {/* Upcoming Events */}
          {data?.eventos && data.eventos.length > 0 && (
            <Card>
              <div className="flex items-center gap-2 mb-4">
                <Calendar size={18} className="text-primary" />
                <h3 className="font-semibold">Proximos eventos</h3>
              </div>
              <div className="space-y-3">
                {data.eventos.slice(0, 5).map((ev, i) => (
                  <div key={i} className="flex items-center justify-between py-2 border-b border-border last:border-0">
                    <div className="flex items-center gap-3">
                      <div className={`w-2 h-2 rounded-full ${
                        ev.type === 'pago' ? 'bg-red-500' :
                        ev.type === 'evento' ? 'bg-green-500' : 'bg-blue-500'
                      }`} />
                      <span className="text-sm">{ev.title}</span>
                    </div>
                    <span className="text-xs text-muted-foreground">{ev.date}</span>
                  </div>
                ))}
              </div>
            </Card>
          )}
        </>
      )}
    </div>
  )
}
