import { useState, useEffect } from 'react'
import { NavLink } from 'react-router'
import { cn } from '@/lib/utils'
import { useTheme } from '@/providers/ThemeProvider'
import {
  LayoutDashboard,
  FileText,
  DollarSign,
  List,
  Calendar,
  Server,
  Bot,
  Sun,
  Moon,
  ChevronLeft,
  ChevronRight,
  X,
} from 'lucide-react'

const navItems = [
  { to: '/', icon: LayoutDashboard, label: 'Home' },
  { to: '/notas', icon: FileText, label: 'Notas' },
  { to: '/finanzas', icon: DollarSign, label: 'Finanzas' },
  { to: '/listas', icon: List, label: 'Listas' },
  { to: '/calendario', icon: Calendar, label: 'Calendario' },
  { to: '/servicios', icon: Server, label: 'Servicios' },
  { to: '/akira', icon: Bot, label: 'Akira' },
]

interface SidebarProps {
  mobileOpen: boolean
  onClose: () => void
}

export function Sidebar({ mobileOpen, onClose }: SidebarProps) {
  const [collapsed, setCollapsed] = useState(false)
  const { theme, toggle } = useTheme()

  // Close mobile sidebar on route change
  useEffect(() => {
    const handleRouteChange = () => {
      if (mobileOpen) onClose()
    }
    // Listen for popstate (back/forward)
    window.addEventListener('popstate', handleRouteChange)
    return () => window.removeEventListener('popstate', handleRouteChange)
  }, [mobileOpen, onClose])

  return (
    <>
      {/* Mobile overlay backdrop */}
      {mobileOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/50 backdrop-blur-sm md:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={cn(
          'h-screen bg-sidebar text-sidebar-foreground flex flex-col transition-all duration-300 border-r border-border',
          collapsed ? 'w-16' : 'w-64',
          // Mobile: fixed overlay
          'fixed md:relative z-50 top-0 left-0',
          mobileOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0',
        )}
      >
        {/* Logo */}
        <div className="flex items-center justify-between px-4 h-16 border-b border-sidebar-accent">
          {!collapsed && (
            <span className="font-bold text-lg tracking-tight">akira.os</span>
          )}
          <div className="flex items-center gap-1">
            {/* Mobile close button */}
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg hover:bg-sidebar-accent transition-colors md:hidden"
            >
              <X size={18} />
            </button>
            {/* Desktop collapse toggle */}
            <button
              onClick={() => setCollapsed(!collapsed)}
              className="p-1.5 rounded-lg hover:bg-sidebar-accent transition-colors hidden md:block"
            >
              {collapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
            </button>
          </div>
        </div>

        {/* Nav items */}
        <nav className="flex-1 py-4 space-y-1 px-2">
          {navItems.map(item => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/'}
              className={({ isActive }) =>
                cn(
                  'flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200',
                  isActive
                    ? 'bg-primary/20 text-primary font-medium'
                    : 'text-sidebar-foreground/70 hover:bg-sidebar-accent hover:text-sidebar-foreground'
                )
              }
              onClick={() => {
                if (mobileOpen) onClose()
              }}
            >
              <item.icon size={20} className="shrink-0" />
              {!collapsed && <span className="text-sm">{item.label}</span>}
            </NavLink>
          ))}
        </nav>

        {/* Theme toggle */}
        <div className="px-3 py-4 border-t border-sidebar-accent">
          <button
            onClick={toggle}
            className="flex items-center gap-3 px-3 py-2.5 w-full rounded-lg text-sidebar-foreground/70 hover:bg-sidebar-accent hover:text-sidebar-foreground transition-all duration-200"
          >
            {theme === 'dark' ? <Sun size={20} className="shrink-0" /> : <Moon size={20} className="shrink-0" />}
            {!collapsed && <span className="text-sm">{theme === 'dark' ? 'Modo claro' : 'Modo oscuro'}</span>}
          </button>
        </div>
      </aside>
    </>
  )
}
