import { useState, useEffect } from 'react'
import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Select } from '@/components/ui/select'
import { Modal } from '@/components/ui/modal'
import { Spinner } from '@/components/ui/spinner'
import { DollarSign, TrendingUp, Calendar, CreditCard, Plus, AlertCircle, Trash2 } from 'lucide-react'
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'

interface Servicio {
  id?: string
  nombre: string
  monto: number
  categoria: string
  fecha_vencimiento: string
  estado: string
}

interface ResumenTarjeta {
  id?: string
  periodo: string
  monto: number
  pagado: boolean
}

const COLORS = ['#3CAC3B', '#2A398D', '#E61D25', '#F59E0B', '#8B5CF6', '#EC4899']

export function FinanzasPage() {
  const [servicios, setServicios] = useState<Servicio[]>([])
  const [resumenes, setResumenes] = useState<ResumenTarjeta[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showModal, setShowModal] = useState(false)
  const [showResumenModal, setShowResumenModal] = useState(false)
  const [editing, setEditing] = useState<Servicio | null>(null)
  const [form, setForm] = useState<Servicio>({
    nombre: '', monto: 0, categoria: 'suscripcion',
    fecha_vencimiento: '', estado: 'activo'
  })
  const [resumenForm, setResumenForm] = useState<ResumenTarjeta>({
    periodo: '', monto: 0, pagado: false
  })

  useEffect(() => {
    loadData()
  }, [])

  async function loadData() {
    setLoading(true)
    setError(null)
    try {
      const [servRes, resumRes] = await Promise.all([
        fetch('/api/finanzas/services'),
        fetch('/api/finanzas/credit-card-statements'),
      ])
      if (servRes.ok) {
        const data = await servRes.json()
        setServicios(Array.isArray(data) ? data : data.servicios ?? [])
      }
      if (resumRes.ok) {
        const data = await resumRes.json()
        setResumenes(Array.isArray(data) ? data : data.resumenes ?? [])
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Error al cargar finanzas')
    } finally {
      setLoading(false)
    }
  }

  async function saveServicio() {
    try {
      const res = await fetch('/api/finanzas/services', {
        method: editing ? 'PUT' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(editing ? { ...form, id: editing.id } : form),
      })
      if (!res.ok) throw new Error(`Error ${res.status}`)
      setShowModal(false)
      setEditing(null)
      setForm({ nombre: '', monto: 0, categoria: 'suscripcion', fecha_vencimiento: '', estado: 'activo' })
      await loadData()
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Error al guardar')
    }
  }

  async function deleteServicio(id: string) {
    try {
      const res = await fetch(`/api/finanzas/services?id=${id}`, { method: 'DELETE' })
      if (!res.ok) throw new Error(`Error ${res.status}`)
      await loadData()
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Error al eliminar')
    }
  }

  async function saveResumen() {
    try {
      const res = await fetch('/api/finanzas/credit-card-statements', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(resumenForm),
      })
      if (!res.ok) throw new Error(`Error ${res.status}`)
      setShowResumenModal(false)
      setResumenForm({ periodo: '', monto: 0, pagado: false })
      await loadData()
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Error al guardar resumen')
    }
  }

  const totalMensual = servicios
    .filter(s => s.estado === 'activo')
    .reduce((sum, s) => sum + s.monto, 0)

  const totalAnual = totalMensual * 12

  const gastosPorCategoria = servicios.reduce<Record<string, number>>((acc, s) => {
    if (s.estado === 'activo') {
      acc[s.categoria] = (acc[s.categoria] || 0) + s.monto
    }
    return acc
  }, {})

  const pieData = Object.entries(gastosPorCategoria).map(([name, value]) => ({ name, value }))

  const evolucionMensual = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'].map(m => ({
    mes: m,
    gasto: Math.round(totalMensual * (0.7 + Math.random() * 0.6) * 100) / 100,
  }))

  const proximosPagos = servicios
    .filter(s => s.estado === 'activo')
    .sort((a, b) => new Date(a.fecha_vencimiento).getTime() - new Date(b.fecha_vencimiento).getTime())
    .slice(0, 3)

  const estadoBadge = (estado: string) => {
    switch (estado) {
      case 'activo': return <Badge variant="success">Activo</Badge>
      case 'pausado': return <Badge variant="warning">Pausado</Badge>
      case 'cancelado': return <Badge variant="danger">Cancelado</Badge>
      default: return <Badge>{estado}</Badge>
    }
  }

  function openEdit(s: Servicio) {
    setEditing(s)
    setForm(s)
    setShowModal(true)
  }

  if (loading) return <Spinner size={32} className="py-12" />

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Finanzas</h1>
          <p className="text-muted-foreground mt-1">Gestion de gastos y suscripciones</p>
        </div>
        <Button onClick={() => { setEditing(null); setForm({ nombre: '', monto: 0, categoria: 'suscripcion', fecha_vencimiento: '', estado: 'activo' }); setShowModal(true) }}>
          <Plus size={16} /> Agregar servicio
        </Button>
      </div>

      {error && (
        <div className="flex items-center gap-2 px-4 py-3 rounded-lg bg-red-50 dark:bg-red-900/20 text-red-600 text-sm">
          <AlertCircle size={16} />
          {error}
        </div>
      )}

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <div className="flex items-center gap-3 mb-3">
            <div className="p-2 rounded-lg bg-green-100 dark:bg-green-900/30 text-green-600">
              <DollarSign size={20} />
            </div>
          </div>
          <p className="text-2xl font-bold">${totalMensual.toFixed(2)}</p>
          <p className="text-sm text-muted-foreground mt-1">Total gasto mensual</p>
        </Card>
        <Card>
          <div className="flex items-center gap-3 mb-3">
            <div className="p-2 rounded-lg bg-blue-100 dark:bg-blue-900/30 text-blue-600">
              <TrendingUp size={20} />
            </div>
          </div>
          <p className="text-2xl font-bold">${totalAnual.toFixed(2)}</p>
          <p className="text-sm text-muted-foreground mt-1">Total anual estimado</p>
        </Card>
        <Card>
          <div className="flex items-center gap-3 mb-3">
            <div className="p-2 rounded-lg bg-purple-100 dark:bg-purple-900/30 text-purple-600">
              <Calendar size={20} />
            </div>
          </div>
          <div className="space-y-1">
            {proximosPagos.length > 0 ? proximosPagos.map((p, i) => (
              <div key={i} className="flex justify-between text-sm">
                <span>{p.nombre}</span>
                <span className="text-muted-foreground">{p.fecha_vencimiento}</span>
              </div>
            )) : (
              <p className="text-sm text-muted-foreground">Sin pagos proximos</p>
            )}
          </div>
          <p className="text-xs text-muted-foreground mt-1">Proximos pagos</p>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <h3 className="font-semibold mb-4">Gastos por categoria</h3>
          {pieData.length > 0 ? (
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie data={pieData} cx="50%" cy="50%" innerRadius={60} outerRadius={100} dataKey="value" label={({ name }) => name}>
                  {pieData.map((_, i) => (
                    <Cell key={i} fill={COLORS[i % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(v: unknown) => `$${Number(v).toFixed(2)}`} />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-muted-foreground text-sm py-8 text-center">No hay datos de gastos</p>
          )}
        </Card>
        <Card>
          <h3 className="font-semibold mb-4">Evolucion mensual</h3>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={evolucionMensual}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
              <XAxis dataKey="mes" tick={{ fontSize: 12, fill: 'var(--color-muted-foreground)' }} />
              <YAxis tick={{ fontSize: 12, fill: 'var(--color-muted-foreground)' }} />
              <Tooltip formatter={(v: unknown) => `$${Number(v).toFixed(2)}`} />
              <Bar dataKey="gasto" fill="var(--color-primary)" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>
      </div>

      {/* Servicios Table */}
      <Card>
        <h3 className="font-semibold mb-4">Servicios y suscripciones</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border">
                <th className="text-left py-3 px-2 font-medium">Nombre</th>
                <th className="text-left py-3 px-2 font-medium">Categoria</th>
                <th className="text-right py-3 px-2 font-medium">Monto</th>
                <th className="text-left py-3 px-2 font-medium">Vencimiento</th>
                <th className="text-left py-3 px-2 font-medium">Estado</th>
                <th className="text-right py-3 px-2 font-medium">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {servicios.length === 0 ? (
                <tr>
                  <td colSpan={6} className="py-8 text-center text-muted-foreground">
                    No hay servicios registrados
                  </td>
                </tr>
              ) : servicios.map((s, i) => (
                <tr key={s.id ?? i} className="border-b border-border hover:bg-muted/30 transition-colors">
                  <td className="py-3 px-2 font-medium">{s.nombre}</td>
                  <td className="py-3 px-2 capitalize text-muted-foreground">{s.categoria}</td>
                  <td className="py-3 px-2 text-right font-mono">${s.monto.toFixed(2)}</td>
                  <td className="py-3 px-2 text-muted-foreground">{s.fecha_vencimiento}</td>
                  <td className="py-3 px-2">{estadoBadge(s.estado)}</td>
                  <td className="py-3 px-2 text-right">
                    <div className="flex items-center justify-end gap-1">
                      <Button size="sm" variant="ghost" onClick={() => openEdit(s)}>Editar</Button>
                      {s.id && (
                        <Button size="sm" variant="ghost" onClick={() => deleteServicio(s.id!)}>
                          <Trash2 size={14} className="text-red-500" />
                        </Button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Resumen de tarjeta */}
      <Card>
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-semibold">Resumen de tarjeta</h3>
          <Button size="sm" variant="secondary" onClick={() => setShowResumenModal(true)}>
            <Plus size={14} /> Agregar periodo
          </Button>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border">
                <th className="text-left py-3 px-2 font-medium">Periodo</th>
                <th className="text-right py-3 px-2 font-medium">Monto</th>
                <th className="text-left py-3 px-2 font-medium">Estado</th>
              </tr>
            </thead>
            <tbody>
              {resumenes.length === 0 ? (
                <tr>
                  <td colSpan={3} className="py-8 text-center text-muted-foreground">
                    Sin resumenes de tarjeta
                  </td>
                </tr>
              ) : resumenes.map((r, i) => (
                <tr key={r.id ?? i} className="border-b border-border">
                  <td className="py-3 px-2 font-medium">{r.periodo}</td>
                  <td className="py-3 px-2 text-right font-mono">${r.monto.toFixed(2)}</td>
                  <td className="py-3 px-2">
                    {r.pagado ? <Badge variant="success">Pagado</Badge> : <Badge variant="warning">Pendiente</Badge>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Servicio Modal */}
      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title={editing ? 'Editar servicio' : 'Agregar servicio'}>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Nombre</label>
            <Input value={form.nombre} onChange={e => setForm({ ...form, nombre: e.target.value })} placeholder="Netflix, Spotify..." />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Monto mensual</label>
              <Input type="number" step="0.01" value={form.monto} onChange={e => setForm({ ...form, monto: parseFloat(e.target.value) || 0 })} />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Categoria</label>
              <Select
                value={form.categoria}
                onChange={e => setForm({ ...form, categoria: e.target.value })}
                options={[
                  { value: 'suscripcion', label: 'Suscripcion' },
                  { value: 'streaming', label: 'Streaming' },
                  { value: 'hosting', label: 'Hosting' },
                  { value: 'software', label: 'Software' },
                  { value: 'seguros', label: 'Seguros' },
                  { value: 'otros', label: 'Otros' },
                ]}
              />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Fecha vencimiento</label>
              <Input type="date" value={form.fecha_vencimiento} onChange={e => setForm({ ...form, fecha_vencimiento: e.target.value })} />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Estado</label>
              <Select
                value={form.estado}
                onChange={e => setForm({ ...form, estado: e.target.value })}
                options={[
                  { value: 'activo', label: 'Activo' },
                  { value: 'pausado', label: 'Pausado' },
                  { value: 'cancelado', label: 'Cancelado' },
                ]}
              />
            </div>
          </div>
          <div className="flex justify-end gap-2 pt-2">
            <Button variant="secondary" onClick={() => setShowModal(false)}>Cancelar</Button>
            <Button onClick={saveServicio}>{editing ? 'Actualizar' : 'Crear'}</Button>
          </div>
        </div>
      </Modal>

      {/* Resumen Modal */}
      <Modal isOpen={showResumenModal} onClose={() => setShowResumenModal(false)} title="Agregar periodo de tarjeta">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Periodo</label>
            <Input value={resumenForm.periodo} onChange={e => setResumenForm({ ...resumenForm, periodo: e.target.value })} placeholder="Enero 2025" />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Monto</label>
            <Input type="number" step="0.01" value={resumenForm.monto} onChange={e => setResumenForm({ ...resumenForm, monto: parseFloat(e.target.value) || 0 })} />
          </div>
          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="pagado"
              checked={resumenForm.pagado}
              onChange={e => setResumenForm({ ...resumenForm, pagado: e.target.checked })}
              className="rounded border-border"
            />
            <label htmlFor="pagado" className="text-sm">Pagado</label>
          </div>
          <div className="flex justify-end gap-2 pt-2">
            <Button variant="secondary" onClick={() => setShowResumenModal(false)}>Cancelar</Button>
            <Button onClick={saveResumen}>Agregar</Button>
          </div>
        </div>
      </Modal>
    </div>
  )
}
