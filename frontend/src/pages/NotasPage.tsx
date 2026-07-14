import { useState, useEffect, useCallback } from 'react'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Spinner } from '@/components/ui/spinner'
import { FileText, Folder, Plus, Search, Save, File, ChevronRight, ChevronDown, AlertCircle } from 'lucide-react'
import ReactMarkdown from 'react-markdown'

interface TreeNode {
  name: string
  path: string
  type: 'file' | 'folder' | 'directory'
  children?: TreeNode[]
}

export function NotasPage() {
  const [tree, setTree] = useState<TreeNode[]>([])
  const [selectedPath, setSelectedPath] = useState<string | null>(null)
  const [content, setContent] = useState('')
  const [originalContent, setOriginalContent] = useState('')
  const [loading, setLoading] = useState(true)
  const [loadingContent, setLoadingContent] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [expanded, setExpanded] = useState<Set<string>>(new Set())
  const [editMode, setEditMode] = useState(false)

  useEffect(() => {
    async function loadTree() {
      try {
        const res = await fetch('/api/notas/tree')
        if (!res.ok) throw new Error(`Error ${res.status}`)
        const data = await res.json()
        setTree(Array.isArray(data) ? data : data.tree ?? [])
      } catch (e) {
        setError(e instanceof Error ? e.message : 'Error al cargar arbol')
      } finally {
        setLoading(false)
      }
    }
    loadTree()
  }, [])

  const loadContent = useCallback(async (path: string) => {
    setLoadingContent(true)
    setError(null)
    try {
      // Ensure path has .md extension — backend expects it
      const safePath = path.endsWith('.md') ? path : `${path}.md`
      const res = await fetch(`/api/notas/read?path=${encodeURIComponent(safePath)}`)
      if (!res.ok) throw new Error(`Error ${res.status}`)
      const text = await res.text()
      setContent(text)
      setOriginalContent(text)
      setSelectedPath(path)
      setEditMode(false)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Error al cargar nota')
    } finally {
      setLoadingContent(false)
    }
  }, [])

  const saveContent = async () => {
    if (!selectedPath) return
    setSaving(true)
    setError(null)
    try {
      const res = await fetch('/api/notas/write', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: selectedPath, content }),
      })
      if (!res.ok) throw new Error(`Error ${res.status}`)
      setOriginalContent(content)
      setEditMode(false)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Error al guardar')
    } finally {
      setSaving(false)
    }
  }

  const createNewNote = async () => {
    const title = prompt('Nombre de la nota (sin .md):')
    if (!title) return
    const path = `${title.replace(/\s+/g, '_')}.md`
    setSaving(true)
    try {
      const res = await fetch('/api/notas/write', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path, content: `# ${title}\n\n` }),
      })
      if (!res.ok) throw new Error(`Error ${res.status}`)
      await loadContent(path)
      // Reload tree
      const treeRes = await fetch('/api/notas/tree')
      if (treeRes.ok) {
        const data = await treeRes.json()
        setTree(Array.isArray(data) ? data : data.tree ?? [])
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Error al crear nota')
    } finally {
      setSaving(false)
    }
  }

  const toggleExpand = (path: string) => {
    setExpanded(prev => {
      const next = new Set(prev)
      if (next.has(path)) next.delete(path)
      else next.add(path)
      return next
    })
  }

  function renderTree(nodes: TreeNode[], depth = 0) {
    const filtered = searchQuery
      ? nodes.filter(n => n.name.toLowerCase().includes(searchQuery.toLowerCase()))
      : nodes

    return filtered.map(node => (
      <div key={node.path}>
        <button
          className={`w-full flex items-center gap-2 px-2 py-1.5 rounded-md text-sm hover:bg-muted/50 transition-colors text-left ${
            selectedPath === node.path ? 'bg-primary/10 text-primary font-medium' : ''
          }`}
          style={{ paddingLeft: `${12 + depth * 16}px` }}
          onClick={() => {
            if (node.type === 'folder' || node.type === 'directory') {
              toggleExpand(node.path)
            } else {
              loadContent(node.path)
            }
          }}
        >
          {node.type === 'folder' || node.type === 'directory' ? (
            <>
              {expanded.has(node.path) ? <ChevronDown size={14} className="shrink-0" /> : <ChevronRight size={14} className="shrink-0" />}
              <Folder size={16} className="shrink-0 text-yellow-500" />
            </>
          ) : (
            <>
              <span className="w-4" />
              <File size={16} className="shrink-0 text-blue-400" />
            </>
          )}
          <span className="truncate">{node.name}</span>
        </button>
        {(node.type === 'folder' || node.type === 'directory') && expanded.has(node.path) && node.children && (
          <div>{renderTree(node.children, depth + 1)}</div>
        )}
      </div>
    ))
  }

  return (
    <div className="max-w-6xl mx-auto h-[calc(100vh-4rem)]">
      <div className="flex gap-6 h-full">
        {/* Sidebar */}
        <div className="w-72 shrink-0 flex flex-col border border-border rounded-xl bg-card overflow-hidden">
          <div className="p-3 border-b border-border space-y-2">
            <div className="flex items-center justify-between">
              <h2 className="font-semibold text-sm">Notas</h2>
              <Button size="sm" onClick={createNewNote} disabled={saving}>
                <Plus size={14} /> Nueva
              </Button>
            </div>
            <div className="relative">
              <Search size={14} className="absolute left-2.5 top-1/2 -translate-y-1/2 text-muted-foreground" />
              <Input
                placeholder="Buscar notas..."
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                className="pl-8 text-xs"
              />
            </div>
          </div>
          <div className="flex-1 overflow-y-auto p-2 space-y-0.5">
            {loading ? (
              <Spinner size={20} className="py-8" />
            ) : (
              renderTree(tree)
            )}
          </div>
        </div>

        {/* Content Panel */}
        <div className="flex-1 flex flex-col border border-border rounded-xl bg-card overflow-hidden">
          {!selectedPath ? (
            <div className="flex-1 flex items-center justify-center text-muted-foreground">
              <div className="text-center">
                <FileText size={48} className="mx-auto mb-3 opacity-30" />
                <p>Selecciona una nota del arbol</p>
              </div>
            </div>
          ) : loadingContent ? (
            <Spinner size={28} className="flex-1" />
          ) : (
            <>
              {/* Toolbar */}
              <div className="flex items-center justify-between px-4 py-3 border-b border-border">
                <span className="text-sm font-medium truncate">{selectedPath}</span>
                <div className="flex items-center gap-2">
                  {editMode ? (
                    <>
                      <Button size="sm" variant="ghost" onClick={() => { setContent(originalContent); setEditMode(false) }}>
                        Cancelar
                      </Button>
                      <Button size="sm" onClick={saveContent} disabled={saving}>
                        <Save size={14} /> {saving ? 'Guardando...' : 'Guardar'}
                      </Button>
                    </>
                  ) : (
                    <Button size="sm" variant="secondary" onClick={() => setEditMode(true)}>
                      Editar
                    </Button>
                  )}
                </div>
              </div>

              {/* Error */}
              {error && (
                <div className="flex items-center gap-2 px-4 py-2 bg-red-50 dark:bg-red-900/20 text-red-600 text-sm">
                  <AlertCircle size={14} />
                  {error}
                </div>
              )}

              {/* Content */}
              <div className="flex-1 overflow-y-auto p-6">
                {editMode ? (
                  <textarea
                    className="w-full h-full min-h-[400px] bg-background border border-border rounded-lg p-4 text-sm font-mono resize-none focus:outline-none focus:ring-2 focus:ring-primary/50"
                    value={content}
                    onChange={e => setContent(e.target.value)}
                  />
                ) : (
                  <div className="prose prose-sm dark:prose-invert max-w-none">
                    <ReactMarkdown>{content}</ReactMarkdown>
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
