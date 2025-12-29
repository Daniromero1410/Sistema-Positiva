"use client"

import { useState } from "react"
import { MainLayout } from "@/components/layout/MainLayout"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Folder, FileText, Download, Eye } from "lucide-react"

export default function ExploradorPage() {
  const [currentPath, setCurrentPath] = useState("/R.A-ABASTECIMIENTO RED ASISTENCIAL")

  const carpetas = [
    { nombre: "0123-2025", tipo: "carpeta", fecha: "2025-12-20" },
    { nombre: "0124-2025", tipo: "carpeta", fecha: "2025-12-18" },
    { nombre: "0125-2025", tipo: "carpeta", fecha: "2025-12-15" },
  ]

  const archivos = [
    { nombre: "ANEXO_1.xlsx", tamano: "2.3 MB", fecha: "2025-12-15" },
    { nombre: "CONTRATO_INICIAL.pdf", tamano: "1.5 MB", fecha: "2025-01-10" },
  ]

  return (
    <MainLayout>
      <div className="max-w-6xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">
          Explorador FTP
        </h1>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg font-medium">
              {currentPath}
            </CardTitle>
          </CardHeader>
          <CardContent>
            {/* Carpetas */}
            <div className="mb-6">
              <h3 className="text-sm font-medium text-gray-700 mb-3">Carpetas</h3>
              <div className="space-y-2">
                {carpetas.map((carpeta, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between p-3 hover:bg-gray-50 rounded-lg border border-gray-200 cursor-pointer"
                  >
                    <div className="flex items-center gap-3">
                      <Folder className="w-5 h-5 text-blue-500" />
                      <div>
                        <p className="font-medium text-gray-900">{carpeta.nombre}</p>
                        <p className="text-sm text-gray-500">{carpeta.fecha}</p>
                      </div>
                    </div>
                    <Button variant="ghost" size="sm">
                      Abrir
                    </Button>
                  </div>
                ))}
              </div>
            </div>

            {/* Archivos */}
            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-3">Archivos</h3>
              <div className="space-y-2">
                {archivos.map((archivo, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between p-3 hover:bg-gray-50 rounded-lg border border-gray-200"
                  >
                    <div className="flex items-center gap-3">
                      <FileText className="w-5 h-5 text-green-500" />
                      <div>
                        <p className="font-medium text-gray-900">{archivo.nombre}</p>
                        <p className="text-sm text-gray-500">
                          {archivo.tamano} • {archivo.fecha}
                        </p>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <Button variant="ghost" size="sm">
                        <Eye className="w-4 h-4" />
                      </Button>
                      <Button variant="ghost" size="sm">
                        <Download className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  )
}
