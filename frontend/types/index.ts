export interface DashboardStats {
  total_contratos: number
  total_servicios: number
  alertas_pendientes: number
  ultima_ejecucion: {
    fecha: string | null
    estado: string | null
  }
}

export interface Ejecucion {
  id: number
  fecha: string
  estado: string
  contratos: number
  exitosos: number
  servicios: number
  alertas: number
}

export interface Contrato {
  numero: string
  ano: number
  nit: string
  razon_social: string
  departamento: string
  municipio: string
  categoria: string
}

export interface Servicio {
  id: number
  contrato: string
  proveedor: string
  cups: string
  descripcion: string
  tarifa: number
  manual: string
  departamento: string
}

export interface MapaDatos {
  ciudad: string
  departamento: string
  contratos: number
  alertas: number
  lat: number
  lon: number
}

export interface ConsolidadorConfig {
  modo: 'completo' | 'por_ano' | 'especifico'
  ano?: number
  contratos?: string[]
  guardar_en_bd: boolean
  exportar_alertas: boolean
}

export interface ProgresoEjecucion {
  ejecucion_id: number
  estado: string
  progreso: number
  contrato_actual: string
  contratos_procesados: number
  total_contratos: number
  servicios_extraidos: number
  alertas_generadas: number
}
