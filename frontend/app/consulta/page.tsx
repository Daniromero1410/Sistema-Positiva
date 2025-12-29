"use client"

import { useState } from "react"
import { MainLayout } from "@/components/layout/MainLayout"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Search } from "lucide-react"

export default function ConsultaPage() {
  const [searchTerm, setSearchTerm] = useState("")

  const servicios = [
    {
      id: 1,
      cups: "890201",
      descripcion: "Consulta medicina general",
      tarifa: 45000,
      manual: "SOAT",
      proveedor: "Clínica Ejemplo",
      departamento: "BOGOTA"
    },
    {
      id: 2,
      cups: "890301",
      descripcion: "Consulta especialista",
      tarifa: 65000,
      manual: "SOAT",
      proveedor: "Hospital Regional",
      departamento: "ANTIOQUIA"
    },
  ]

  return (
    <MainLayout>
      <div className="max-w-6xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">
          Consulta de Datos
        </h1>

        <Card className="mb-6">
          <CardContent className="pt-6">
            <div className="flex gap-4">
              <div className="flex-1">
                <input
                  type="text"
                  placeholder="Buscar por CUPS, descripción, contrato o proveedor..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full border border-gray-300 rounded-md px-4 py-2"
                />
              </div>
              <Button>
                <Search className="w-4 h-4 mr-2" />
                Buscar
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Resultados</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">CUPS</th>
                    <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">Descripción</th>
                    <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">Tarifa</th>
                    <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">Manual</th>
                    <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">Proveedor</th>
                    <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">Departamento</th>
                  </tr>
                </thead>
                <tbody>
                  {servicios.map((servicio) => (
                    <tr key={servicio.id} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="py-3 px-4 text-sm font-medium">{servicio.cups}</td>
                      <td className="py-3 px-4 text-sm">{servicio.descripcion}</td>
                      <td className="py-3 px-4 text-sm">
                        ${servicio.tarifa.toLocaleString()}
                      </td>
                      <td className="py-3 px-4 text-sm">
                        <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded-full text-xs">
                          {servicio.manual}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-sm">{servicio.proveedor}</td>
                      <td className="py-3 px-4 text-sm">{servicio.departamento}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  )
}
