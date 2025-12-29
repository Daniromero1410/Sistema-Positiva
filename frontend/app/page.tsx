"use client"

import { useEffect, useState } from "react"
import { MainLayout } from "@/components/layout/MainLayout"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { dashboardAPI } from "@/lib/api"
import { formatNumber, formatDate } from "@/lib/utils"
import {
  FileText,
  CheckCircle,
  AlertCircle,
  Package
} from "lucide-react"

interface Stats {
  total_contratos: number
  total_servicios: number
  alertas_pendientes: number
  ultima_ejecucion: {
    fecha: string | null
    estado: string | null
  }
}

export default function DashboardPage() {
  const [stats, setStats] = useState<Stats>({
    total_contratos: 925,
    total_servicios: 45230,
    alertas_pendientes: 45,
    ultima_ejecucion: { fecha: null, estado: null }
  })

  useEffect(() => {
    dashboardAPI.getStats()
      .then(response => setStats(response.data))
      .catch(error => console.error("Error al cargar estadísticas:", error))
  }, [])

  const statCards = [
    {
      title: "Total Contratos",
      value: formatNumber(stats.total_contratos),
      icon: FileText,
      color: "text-blue-600",
      bgColor: "bg-blue-50"
    },
    {
      title: "Contratos Exitosos",
      value: formatNumber(stats.total_contratos - stats.alertas_pendientes),
      icon: CheckCircle,
      color: "text-green-600",
      bgColor: "bg-green-50"
    },
    {
      title: "Alertas Pendientes",
      value: formatNumber(stats.alertas_pendientes),
      icon: AlertCircle,
      color: "text-orange-600",
      bgColor: "bg-orange-50"
    },
    {
      title: "Total Servicios",
      value: formatNumber(stats.total_servicios),
      icon: Package,
      color: "text-positiva-600",
      bgColor: "bg-positiva-50"
    }
  ]

  return (
    <MainLayout>
      {/* Estadísticas principales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        {statCards.map((stat, index) => {
          const Icon = stat.icon
          return (
            <Card key={index} className="hover:shadow-lg transition-shadow">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600 mb-1">
                      {stat.title}
                    </p>
                    <p className="text-3xl font-bold text-gray-900">
                      {stat.value}
                    </p>
                  </div>
                  <div className={`${stat.bgColor} p-3 rounded-lg`}>
                    <Icon className={`w-6 h-6 ${stat.color}`} />
                  </div>
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>

      {/* Gráficos y contenido adicional */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Servicios por mes */}
        <Card>
          <CardHeader>
            <CardTitle>Servicios Procesados por Mes</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-64 flex items-center justify-center text-gray-400">
              <p>Gráfico de barras - Recharts</p>
            </div>
          </CardContent>
        </Card>

        {/* Contratos por departamento */}
        <Card>
          <CardHeader>
            <CardTitle>Contratos por Departamento</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-64 flex items-center justify-center text-gray-400">
              <p>Gráfico de dona - Recharts</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Últimas ejecuciones */}
      <Card>
        <CardHeader>
          <CardTitle>Últimas Ejecuciones</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">Fecha</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">Estado</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">Contratos</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">Servicios</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">Alertas</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-3 px-4 text-sm">28/12/2025 10:30</td>
                  <td className="py-3 px-4">
                    <span className="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">
                      Completado
                    </span>
                  </td>
                  <td className="py-3 px-4 text-sm">150</td>
                  <td className="py-3 px-4 text-sm">45,230</td>
                  <td className="py-3 px-4 text-sm">12</td>
                </tr>
                <tr className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-3 px-4 text-sm">27/12/2025 14:15</td>
                  <td className="py-3 px-4">
                    <span className="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">
                      Completado
                    </span>
                  </td>
                  <td className="py-3 px-4 text-sm">148</td>
                  <td className="py-3 px-4 text-sm">44,891</td>
                  <td className="py-3 px-4 text-sm">8</td>
                </tr>
                <tr className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-3 px-4 text-sm">26/12/2025 09:45</td>
                  <td className="py-3 px-4">
                    <span className="px-2 py-1 bg-orange-100 text-orange-700 rounded-full text-xs font-medium">
                      Con alertas
                    </span>
                  </td>
                  <td className="py-3 px-4 text-sm">145</td>
                  <td className="py-3 px-4 text-sm">43,567</td>
                  <td className="py-3 px-4 text-sm">25</td>
                </tr>
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </MainLayout>
  )
}
