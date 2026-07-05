import { useState, useEffect } from 'react'
import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Select } from '@/components/ui/select'
import { Modal } from '@/components/ui/modal'
import { Tabs } from '@/components/ui/tabs'
import { Spinner } from '@/components/ui/spinner'
import { Plus, Search, Star, Film, Tv, Music, MapPin, Utensils, LayoutGrid, List as ListIcon, Table, AlertCircle } from 'lucide-react'

interface ListItem {
  id?: string
  titulo: string
  tipo: string
  estado: string
  rating: number
  notas: string
  imagen_url: string
}

const TIPO_ICONS: Record<string, typeof Film> = {
  pelicula: Film,
  serie: Tv,
  musica: Music,
  lugar: MapPin,
  comida: Utensils,
}

const TIPO_LABELS: Record<string, string> = {
  pelicula: 'Peliculas',
  serie: 'Series',
  musica: 'Musica',
  lugar: 'Lugares',
  comida: 'Comida',
}

const TABS = [
  { id: 'todas', label: 'Todas' },
  { id: 'pelicula', label: 'Peliculas' },
  { id: 'serie', label: 'Series' },
  { id: 'musica', label: 'Musica' },
  { id: 'lugar', label: 'Lugares' },
  { id: 'comida', label: 'Comida' },
]

export function ListasPage() {
  const [items, setItems] = useState<ListItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState('todas')
  const [searchQuery, setSearchQuery] = useState('')
  const [viewMode, setViewMode] = useState<'grid' | 'table'>('grid')
  const [showModal, setShowModal] = useState(false)
  const [editing, setEditing] = useState<ListItem | null>(null)
  const [form, setForm] = useState<ListItem>({
    titulo: '', tipo: 'pelicula', estado: 'pendiente', rating: 0, notas: '', imagen_url: ''
  })

  useEffect(() => {
    loadItems()
  }, [])

  async function loadItems() {
    setLoading(true)
    setError(null)
    try {
      const res = await fetch('/api/listas')
      if (!res.ok) throw new Error(`Error ${res.status}`)
      const data = await res.json()
      setItems(Array.isArray(data) ? data : data.items ?? [])
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Error al cargar listas')
    } finally {
      setLoading(false)
    }
  }

  async function saveItem() {
    try {
      const res = await fetch('/api/listas', {
        method: editing ? 'PUT' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(editing ? { ...form, id: editing.id } : form),
      })
      if (!res.ok) throw new Error(`Error ${res.status}`)
      setShowModal(false)
      setEditing(null)
      setForm({ titulo: '', tipo: 'pelicula', estado: 'pendiente', rating: 0, notas: '', imagen_url: '' })
      await loadItems()
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Error al guardar')
    }
  }

  async function deleteItem(id: string) {
    try {
      const res = await fetch(`/api/listas?id=${id}`, { method: 'DELETE' })
      if (!res.ok) throw new Error(`Error ${res.status}`)
      await loadItems()
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Error al eliminar')
    }
  }

  async function searchTmdb() {
    const query = prompt('Buscar en TMDB:')
    if (!query) return
    try {
      const res = await fetch(`/api/listas/tmdb-search?q=${encodeURIComponent(query)}`)
      if (!res.ok) throw new Error(`Error ${res.status}`)
      const data = await res.json()
      if (Array.isArray(data.results) && data.results.length > 0) {
        const r = data.results[0]
        setForm(prev => ({
          ...prev,
          titulo: r.title || r.name || '',
          imagen_url: r.poster_path ? `https://image.tmdb.org/t/p/w500${r.poster_path}` : '',
          notas: r.overview || '',
        }))
        setShowModal(true)
      } else {
        alert('No se encontraron resultados')
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Error en busqueda TMDB')
    }
  }

  const filtered = items.filter(item => {
    const matchTab = activeTab === 'todas' || item.tipo === activeTab
    const matchSearch = !searchQuery || item.titulo.toLowerCase().includes(searchQuery.toLowerCase())
    return matchTab && matchSearch
  })

  const estadoBadge = (estado: string) => {
    switch (estado) {
      case 'completado': return <Badge variant="success">Completado</Badge>
      case 'en_progreso': return <Badge variant="info">En progreso</Badge>
      case 'pendiente': return <Badge variant="warning">Pendiente</Badge>
      case 'abandonado': return <Badge variant="danger">Abandonado</Badge>
      default: return <Badge>{estado}</Badge>
    }
  }

  const ratingStars = (r: number) => {
    return (
      <div className="flex items-center gap-0.5">
        {[1, 2, 3, 4, 5].map(i => (
          <Star key={i} size={14} className={i <= r ? 'text-yellow-500 fill-yellow-500' : 'text-muted'} />
        ))}
      </div>
    )
  }

  if (loading) return <Spinner size={32} className="py-12" />

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Listas</h1>
          <p className="text-muted-foreground mt-1">Peliculas, series, musica y mas</p>
        </div>
        <div className="flex items-center gap-2">
          <Button size="sm" variant="secondary" onClick={searchTmdb}>
            Buscar en TMDB
          </Button>
          <Button size="sm" onClick={() => { setEditing(null); setForm({ titulo: '', tipo: 'pelicula', estado: 'pendiente', rating: 0, notas: '', imagen_url: '' }); setShowModal(true) }}>
            <Plus size={16} /> Agregar
          </Button>
        </div>
      </div>

      {error && (
        <div className="flex items-center gap-2 px-4 py-3 rounded-lg bg-red-50 dark:bg-red-900/20 text-red-600 text-sm">
          <AlertCircle size={16} />
          {error}
        </div>
      )}

      {/* Filters */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4">
        <Tabs tabs={TABS} active={activeTab} onChange={setActiveTab} />
        <div className="flex items-center gap-2 ml-auto">
          <div className="relative">
            <Search size={14} className="absolute left-2.5 top-1/2 -translate-y-1/2 text-muted-foreground" />
            <Input
              placeholder="Buscar..."
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              className="pl-8 w-48"
            />
          </div>
          <div className="flex border border-border rounded-lg overflow-hidden">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-2 ${viewMode === 'grid' ? 'bg-primary text-white' : 'text-muted-foreground hover:bg-muted/50'}`}
            >
              <LayoutGrid size={16} />
            </button>
            <button
              onClick={() => setViewMode('table')}
              className={`p-2 ${viewMode === 'table' ? 'bg-primary text-white' : 'text-muted-foreground hover:bg-muted/50'}`}
            >
              <Table size={16} />
            </button>
          </div>
        </div>
      </div>

      {/* Content */}
      {filtered.length === 0 ? (
        <Card className="p-8 text-center">
          <p className="text-muted-foreground">No hay items en esta categoria</p>
        </Card>
      ) : viewMode === 'grid' ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filtered.map((item, i) => (
            <Card key={item.id ?? i} className="overflow-hidden p-0">
              {item.imagen_url && (
                <div className="aspect-[2/3] bg-muted overflow-hidden">
                  <img
                    src={item.imagen_url}
                    alt={item.titulo}
                    className="w-full h-full object-cover"
                    onError={e => { (e.target as HTMLImageElement).style.display = 'none' }}
                  />
                </div>
              )}
              <div className="p-4 space-y-2">
                <div className="flex items-center justify-between">
                  <h3 className="font-semibold truncate">{item.titulo}</h3>
                  {estadoBadge(item.estado)}
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-xs capitalize text-muted-foreground">{item.tipo}</span>
                  {ratingStars(item.rating)}
                </div>
                {item.notas && (
                  <p className="text-xs text-muted-foreground line-clamp-2">{item.notas}</p>
                )}
                <div className="flex gap-1 pt-1">
                  <Button size="sm" variant="ghost" onClick={() => { setEditing(item); setForm(item); setShowModal(true) }}>
                    Editar
                  </Button>
                  <Button size="sm" variant="ghost" onClick={() => item.id && deleteItem(item.id)}>
                    <AlertCircle size={14} className="text-red-500" />
                  </Button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      ) : (
        <Card className="overflow-hidden p-0">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left py-3 px-4 font-medium">Titulo</th>
                  <th className="text-left py-3 px-4 font-medium">Tipo</th>
                  <th className="text-left py-3 px-4 font-medium">Estado</th>
                  <th className="text-left py-3 px-4 font-medium">Rating</th>
                  <th className="text-left py-3 px-4 font-medium">Notas</th>
                  <th className="text-right py-3 px-4 font-medium">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((item, i) => (
                  <tr key={item.id ?? i} className="border-b border-border hover:bg-muted/30">
                    <td className="py-3 px-4 font-medium">{item.titulo}</td>
                    <td className="py-3 px-4 capitalize text-muted-foreground">{item.tipo}</td>
                    <td className="py-3 px-4">{estadoBadge(item.estado)}</td>
                    <td className="py-3 px-4">{ratingStars(item.rating)}</td>
                    <td className="py-3 px-4 text-muted-foreground max-w-[200px] truncate">{item.notas}</td>
                    <td className="py-3 px-4 text-right">
                      <Button size="sm" variant="ghost" onClick={() => { setEditing(item); setForm(item); setShowModal(true) }}>Editar</Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      )}

      {/* Modal */}
      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title={editing ? 'Editar item' : 'Agregar item'} size="lg">
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Titulo</label>
              <Input value={form.titulo} onChange={e => setForm({ ...form, titulo: e.target.value })} />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Tipo</label>
              <Select
                value={form.tipo}
                onChange={e => setForm({ ...form, tipo: e.target.value })}
                options={[
                  { value: 'pelicula', label: 'Pelicula' },
                  { value: 'serie', label: 'Serie' },
                  { value: 'musica', label: 'Musica' },
                  { value: 'lugar', label: 'Lugar' },
                  { value: 'comida', label: 'Comida' },
                ]}
              />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Estado</label>
              <Select
                value={form.estado}
                onChange={e => setForm({ ...form, estado: e.target.value })}
                options={[
                  { value: 'pendiente', label: 'Pendiente' },
                  { value: 'en_progreso', label: 'En progreso' },
                  { value: 'completado', label: 'Completado' },
                  { value: 'abandonado', label: 'Abandonado' },
                ]}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Rating (1-5)</label>
              <Input
                type="number"
                min={0}
                max={5}
                value={form.rating}
                onChange={e => setForm({ ...form, rating: parseInt(e.target.value) || 0 })}
              />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">URL de imagen</label>
            <Input value={form.imagen_url} onChange={e => setForm({ ...form, imagen_url: e.target.value })} placeholder="https://..." />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Notas</label>
            <Textarea value={form.notas} onChange={e => setForm({ ...form, notas: e.target.value })} />
          </div>
          <div className="flex justify-end gap-2 pt-2">
            <Button variant="secondary" onClick={() => setShowModal(false)}>Cancelar</Button>
            <Button onClick={saveItem}>{editing ? 'Actualizar' : 'Crear'}</Button>
          </div>
        </div>
      </Modal>
    </div>
  )
}
