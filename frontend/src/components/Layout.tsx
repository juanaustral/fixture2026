import { useState } from 'react'
import { Sidebar } from '@/components/Sidebar'
import { Outlet } from 'react-router'
import { PageTransition } from '@/components/ui/motion'
import { Menu } from 'lucide-react'

export function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <div className="flex h-screen bg-background text-foreground">
      <Sidebar mobileOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      <main className="flex-1 overflow-auto min-w-0">
        {/* Mobile header with hamburger */}
        <div className="sticky top-0 z-30 flex items-center h-14 px-4 border-b border-border bg-background/80 backdrop-blur-md md:hidden">
          <button
            onClick={() => setSidebarOpen(true)}
            className="p-2 -ml-2 rounded-lg hover:bg-muted transition-colors"
            aria-label="Abrir menu"
          >
            <Menu size={22} />
          </button>
          <span className="ml-2 font-bold text-base tracking-tight">akira.os</span>
        </div>

        <div className="p-4 md:p-8">
          <PageTransition>
            <Outlet />
          </PageTransition>
        </div>
      </main>
    </div>
  )
}
