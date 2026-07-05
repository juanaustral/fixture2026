import { useState, useEffect, useRef } from 'react'
import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Select } from '@/components/ui/select'
import { Modal } from '@/components/ui/modal'
import { Spinner } from '@/components/ui/spinner'
import { Calendar as CalendarIcon, Plus, AlertCircle } from 'lucide-react'
import FullCalendar from '@fullcalendar/react'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import type { EventClickArg, DateSelectArg } from '@fullcalendar/core'

interface CalendarEvent {
  id?: string
  title: string
  date: string
  type: 'pago' | 'evento' | 'tarea'
  description?: string
}

const typeColors: Record<string, { bg: string; border: string; text: string }> = {
  pago: { bg: '#FEE2E2', border: '#EF4444', text: '#991B1B' },
  evento: { bg: '#DCFCE7', border: '#22C55E', text: '#166534' },
  tarea: { bg: '#DBEAFE', border: '#3B82F6', text: '#1E40AF' },
}

const typeColorsDark: Record<string, string> = {
  pago: '#7F1D1D',
  evento: '#14532D',
  tarea: '#1E3A5F',
}

export function CalendarioPage() {
  const [events, setEvents] = useState<CalendarEvent[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showModal, setShowModal] = useState(false)
  const [selectedDate, setSelectedDate] = useState('')
  const [form, setForm] = useState<CalendarEvent>({
    title: '', date: '', type: 'evento', description: ''
  })
  const calendarRef = useRef<FullCalendar>(null)

  useEffect(() => {
    loadEvents()
  }, [])

  async function loadEvents() {
    setLoading(true)
    setError(null)
    try {
      const res = await fetch('/api/calendar')
      if (!res.ok) throw new Error(`Error ${res.status}`)
      const data = await res.json()
      setEvents(Array.isArray(data) ? data : data.events ?? [])
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Error al cargar eventos')
      setEvents([])
    } finally {
      setLoading(false)
    }
  }

  async function saveEvent() {
    try {
      const res = await fetch('/api/events', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      })
      if (!res.ok) throw new Error(`Error ${res.status}`)
      setShowModal(false)
      setForm({ title: '', date: '', type: 'evento', description: '' })
      await loadEvents()
    } catch (e) {
      // Local fallback
      setEvents(prev => [...prev, { ...form, id: `local-${Date.now()}` }])
      setShowModal(false)
      setForm({ title: '', date: '', type: 'evento', description: '' })
    }
  }

  function handleDateSelect(selectInfo: DateSelectArg) {
    setSelectedDate(selectInfo.startStr.split('T')[0])
    setForm(prev => ({ ...prev, date: selectInfo.startStr.split('T')[0] }))
    setShowModal(true)
  }

  function handleEventClick(clickInfo: EventClickArg) {
    if (confirm(`Eliminar "${clickInfo.event.title}"?`)) {
      const extId = clickInfo.event.extendedProps._id
      if (extId) {
        fetch(`/api/events?id=${extId}`, { method: 'DELETE' }).catch(() => {})
      }
      setEvents(prev => prev.filter(e => e.id !== extId))
    }
  }

  const fullCalendarEvents = events.map(ev => ({
    id: ev.id,
    title: ev.title,
    start: ev.date,
    allDay: true,
    backgroundColor: typeColors[ev.type]?.bg,
    borderColor: typeColors[ev.type]?.border,
    textColor: typeColors[ev.type]?.text,
    extendedProps: { _id: ev.id, type: ev.type, description: ev.description },
  }))

  const nextEvents = [...events]
    .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
    .filter(e => new Date(e.date) >= new Date())
    .slice(0, 5)

  const typeLabel = (t: string) => {
    switch (t) {
      case 'pago': return <Badge variant="danger">Pago</Badge>
      case 'evento': return <Badge variant="success">Evento</Badge>
      case 'tarea': return <Badge variant="info">Tarea</Badge>
      default: return <Badge>{t}</Badge>
    }
  }

  if (loading) return <Spinner size={32} className="py-12" />

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Calendario</h1>
          <p className="text-muted-foreground mt-1">Sincronizado con Google Calendar</p>
        </div>
        <Button onClick={() => { setSelectedDate(''); setForm({ title: '', date: '', type: 'evento', description: '' }); setShowModal(true) }}>
          <Plus size={16} /> Nuevo evento
        </Button>
      </div>

      {error && (
        <div className="flex items-center gap-2 px-4 py-3 rounded-lg bg-red-50 dark:bg-red-900/20 text-red-600 text-sm">
          <AlertCircle size={16} />
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Calendar */}
        <div className="lg:col-span-3 bg-card border border-border rounded-xl p-4 overflow-hidden">
          <style>{`
            .fc { --fc-border-color: var(--color-border); --fc-page-bg-color: transparent; --fc-neutral-bg-color: var(--color-muted); --fc-today-bg-color: rgba(60, 172, 59, 0.1); --fc-list-event-hover-bg-color: var(--color-muted); --fc-event-text-color: inherit; }
            .fc .fc-toolbar-title { font-size: 1.1rem; font-weight: 600; }
            .fc .fc-button { background: var(--color-card) !important; border: 1px solid var(--color-border) !important; color: var(--color-foreground) !important; font-size: 0.8rem !important; padding: 0.3rem 0.6rem !important; border-radius: 0.5rem !important; }
            .fc .fc-button-primary:not(:disabled).fc-button-active { background: var(--color-primary) !important; color: white !important; }
            .fc .fc-daygrid-day-number { font-size: 0.85rem; padding: 4px; color: var(--color-foreground); }
            .fc .fc-col-header-cell-cushion { font-size: 0.8rem; padding: 6px 4px; color: var(--color-muted-foreground); text-decoration: none; }
            .fc .fc-daygrid-day.fc-day-today { background: rgba(60, 172, 59, 0.08); }
            .fc .fc-daygrid-event { border-radius: 4px; padding: 1px 4px; font-size: 0.75rem; }
            .dark .fc { --fc-page-bg-color: transparent; }
            .dark .fc .fc-button { background: var(--color-card) !important; }
          `}</style>
          <FullCalendar
            ref={calendarRef}
            plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
            initialView="dayGridMonth"
            headerToolbar={{
              left: 'prev,next today',
              center: 'title',
              right: 'dayGridMonth,timeGridWeek',
            }}
            events={fullCalendarEvents}
            selectable={true}
            select={handleDateSelect}
            eventClick={handleEventClick}
            height="auto"
            locale="es"
          />
        </div>

        {/* Sidebar */}
        <div className="space-y-4">
          <Card>
            <div className="flex items-center gap-2 mb-3">
              <CalendarIcon size={16} className="text-primary" />
              <h3 className="font-semibold text-sm">Proximos eventos</h3>
            </div>
            {nextEvents.length === 0 ? (
              <p className="text-xs text-muted-foreground">No hay eventos proximos</p>
            ) : (
              <div className="space-y-2">
                {nextEvents.map((ev, i) => (
                  <div key={ev.id ?? i} className="flex items-start gap-3 py-2 border-b border-border last:border-0">
                    <div className={`w-2 h-2 rounded-full mt-1.5 shrink-0 ${
                      ev.type === 'pago' ? 'bg-red-500' :
                      ev.type === 'evento' ? 'bg-green-500' : 'bg-blue-500'
                    }`} />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium truncate">{ev.title}</p>
                      <p className="text-xs text-muted-foreground">{ev.date}</p>
                    </div>
                    {typeLabel(ev.type)}
                  </div>
                ))}
              </div>
            )}
          </Card>

          {/* Legend */}
          <Card>
            <h3 className="font-semibold text-sm mb-3">Leyenda</h3>
            <div className="space-y-2">
              {[
                { label: 'Pago', color: 'bg-red-500', badge: 'danger' },
                { label: 'Evento', color: 'bg-green-500', badge: 'success' },
                { label: 'Tarea', color: 'bg-blue-500', badge: 'info' },
              ].map(item => (
                <div key={item.label} className="flex items-center gap-2">
                  <div className={`w-3 h-3 rounded-full ${item.color}`} />
                  <span className="text-sm">{item.label}</span>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </div>

      {/* Create Event Modal */}
      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="Nuevo evento">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Titulo</label>
            <Input value={form.title} onChange={e => setForm({ ...form, title: e.target.value })} placeholder="Nombre del evento" />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Fecha</label>
            <Input type="date" value={form.date || selectedDate} onChange={e => setForm({ ...form, date: e.target.value })} />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Tipo</label>
            <Select
              value={form.type}
              onChange={e => setForm({ ...form, type: e.target.value as CalendarEvent['type'] })}
              options={[
                { value: 'evento', label: 'Evento' },
                { value: 'pago', label: 'Pago' },
                { value: 'tarea', label: 'Tarea' },
              ]}
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Descripcion (opcional)</label>
            <Input value={form.description ?? ''} onChange={e => setForm({ ...form, description: e.target.value })} />
          </div>
          <div className="flex justify-end gap-2 pt-2">
            <Button variant="secondary" onClick={() => setShowModal(false)}>Cancelar</Button>
            <Button onClick={saveEvent}>Crear evento</Button>
          </div>
        </div>
      </Modal>
    </div>
  )
}
