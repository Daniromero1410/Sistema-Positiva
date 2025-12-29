"use client"

import { Sidebar } from "./Sidebar"
import { Navbar } from "./Navbar"

export function MainLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar />
      <div className="ml-64">
        <Navbar />
        <main className="pt-16">
          <div className="p-6">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}
