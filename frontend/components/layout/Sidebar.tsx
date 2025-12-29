"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import {
  LayoutDashboard,
  Settings2,
  FolderOpen,
  Search,
  MapPin,
  Settings
} from "lucide-react"

const menuItems = [
  { name: "Dashboard", href: "/", icon: LayoutDashboard },
  { name: "Consolidador T25", href: "/consolidador", icon: Settings2 },
  { name: "Explorador FTP", href: "/explorador", icon: FolderOpen },
  { name: "Consulta de Datos", href: "/consulta", icon: Search },
  { name: "Mapa de Contratos", href: "/mapa", icon: MapPin },
  { name: "Configuración", href: "/configuracion", icon: Settings },
]

export function Sidebar() {
  const pathname = usePathname()

  return (
    <aside className="w-64 bg-sidebar h-screen fixed left-0 top-0 flex flex-col border-r border-sidebar-border">
      {/* Logo */}
      <div className="p-6 border-b border-sidebar-border">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-positiva-500 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-xl">P</span>
          </div>
          <div>
            <h1 className="text-white font-bold text-lg">POSITIVA</h1>
            <p className="text-sidebar-muted text-xs">Consolidador T25</p>
          </div>
        </div>
      </div>

      {/* Menú */}
      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          {menuItems.map((item) => {
            const Icon = item.icon
            const isActive = pathname === item.href

            return (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={cn(
                    "flex items-center gap-3 px-4 py-3 rounded-lg transition-colors",
                    isActive
                      ? "bg-positiva-500 text-white"
                      : "text-sidebar-foreground hover:bg-sidebar-border"
                  )}
                >
                  <Icon className="w-5 h-5" />
                  <span className="font-medium">{item.name}</span>
                </Link>
              </li>
            )
          })}
        </ul>
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-sidebar-border">
        <div className="text-center text-sidebar-muted text-xs">
          <p>Sistema Consolidador T25</p>
          <p>v1.0.0</p>
        </div>
      </div>
    </aside>
  )
}
