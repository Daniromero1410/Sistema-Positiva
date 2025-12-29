"use client"

import { MainLayout } from "@/components/layout/MainLayout"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { MapPin } from "lucide-react"

export default function MapaPage() {
  const topCiudades = [
    { posicion: 1, ciudad: "BOGOTA", departamento: "BOGOTA", contratos: 135 },
    { posicion: 2, ciudad: "BARRANQUILLA", departamento: "ATLANTICO", contratos: 32 },
    { posicion: 3, ciudad: "MEDELLIN", departamento: "ANTIOQUIA", contratos: 29 },
    { posicion: 4, ciudad: "CALI", departamento: "VALLE DEL CAUCA", contratos: 28 },
    { posicion: 5, ciudad: "BUCARAMANGA", departamento: "SANTANDER", contratos: 24 },
  ]

  return (
    <MainLayout>
      <div className="max-w-6xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">
          Mapa de Contratos
        </h1>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Mapa */}
          <Card className="lg:col-span-2">
            <CardContent className="p-0">
              <div className="h-[600px] bg-gray-100 flex items-center justify-center rounded-lg">
                <div className="text-center text-gray-400">
                  <MapPin className="w-16 h-16 mx-auto mb-4" />
                  <p>Mapa interactivo - MapLibre GL JS</p>
                  <p className="text-sm mt-2">
                    Visualización de contratos por ubicación geográfica
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Top Ciudades */}
          <Card>
            <CardHeader>
              <CardTitle>Top Ciudades</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {topCiudades.map((ciudad) => (
                  <div key={ciudad.posicion} className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 bg-positiva-100 text-positiva-600 rounded-full flex items-center justify-center font-bold text-sm">
                        {ciudad.posicion}
                      </div>
                      <div>
                        <p className="font-medium text-gray-900">{ciudad.ciudad}</p>
                        <p className="text-sm text-gray-500">{ciudad.departamento}</p>
                      </div>
                    </div>
                    <span className="font-bold text-positiva-600">
                      {ciudad.contratos}
                    </span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </MainLayout>
  )
}
