"use client"

import { useState, useCallback } from "react"
import { MainLayout } from "@/components/layout/MainLayout"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { consolidadorAPI } from "@/lib/api"
import { Upload, Play, Download } from "lucide-react"

export default function ConsolidadorPage() {
  const [maestraFile, setMaestraFile] = useState<File | null>(null)
  const [config, setConfig] = useState({
    modo: "completo",
    ano: 2025,
    guardar_en_bd: true,
    exportar_alertas: true
  })
  const [isProcessing, setIsProcessing] = useState(false)
  const [ejecucionId, setEjecucionId] = useState<number | null>(null)

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setMaestraFile(file)
    }
  }

  const handleIniciar = async () => {
    if (!maestraFile) {
      alert("Por favor sube la maestra de contratos primero")
      return
    }

    try {
      setIsProcessing(true)

      // Subir maestra
      await consolidadorAPI.uploadMaestra(maestraFile)

      // Iniciar consolidación
      const response = await consolidadorAPI.iniciar(config)
      setEjecucionId(response.data.ejecucion_id)

    } catch (error) {
      console.error("Error al iniciar consolidación:", error)
      alert("Error al iniciar la consolidación")
    } finally {
      setIsProcessing(false)
    }
  }

  return (
    <MainLayout>
      <div className="max-w-6xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">
          Consolidador T25
        </h1>

        {/* Upload Maestra */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>1. Cargar Maestra de Contratos</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-positiva-500 transition-colors">
              <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <input
                type="file"
                accept=".xlsx,.xls"
                onChange={handleFileUpload}
                className="hidden"
                id="file-upload"
              />
              <label htmlFor="file-upload" className="cursor-pointer">
                <span className="text-positiva-600 font-medium hover:text-positiva-700">
                  Selecciona un archivo
                </span>
                <span className="text-gray-600"> o arrastra y suelta</span>
              </label>
              <p className="text-sm text-gray-500 mt-2">
                Archivos Excel (.xlsx, .xls)
              </p>
              {maestraFile && (
                <p className="text-sm text-green-600 mt-4 font-medium">
                  ✓ {maestraFile.name}
                </p>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Configuración */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>2. Configurar Ejecución</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Modo de Ejecución
                </label>
                <select
                  value={config.modo}
                  onChange={(e) => setConfig({...config, modo: e.target.value})}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                >
                  <option value="completo">Completo</option>
                  <option value="por_ano">Por Año</option>
                  <option value="especifico">Específico</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Año
                </label>
                <input
                  type="number"
                  value={config.ano}
                  onChange={(e) => setConfig({...config, ano: parseInt(e.target.value)})}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                />
              </div>

              <div className="col-span-2 flex gap-4">
                <label className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={config.guardar_en_bd}
                    onChange={(e) => setConfig({...config, guardar_en_bd: e.target.checked})}
                    className="w-4 h-4"
                  />
                  <span className="text-sm text-gray-700">Guardar en Base de Datos</span>
                </label>

                <label className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={config.exportar_alertas}
                    onChange={(e) => setConfig({...config, exportar_alertas: e.target.checked})}
                    className="w-4 h-4"
                  />
                  <span className="text-sm text-gray-700">Exportar Alertas</span>
                </label>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Botón Iniciar */}
        <div className="flex justify-center mb-6">
          <Button
            onClick={handleIniciar}
            disabled={!maestraFile || isProcessing}
            size="lg"
            className="px-8"
          >
            <Play className="w-5 h-5 mr-2" />
            {isProcessing ? "Procesando..." : "Iniciar Consolidación"}
          </Button>
        </div>

        {/* Resultados (si hay ejecución) */}
        {ejecucionId && (
          <Card>
            <CardHeader>
              <CardTitle>3. Descargar Resultados</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <Button variant="outline" className="w-full justify-start">
                  <Download className="w-4 h-4 mr-2" />
                  CONSOLIDADO_ML_LIMPIO.xlsx (12.5 MB)
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <Download className="w-4 h-4 mr-2" />
                  CONSOLIDADO_2025.xlsx (8.2 MB)
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <Download className="w-4 h-4 mr-2" />
                  ALERTAS.xlsx (245 KB)
                </Button>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </MainLayout>
  )
}
