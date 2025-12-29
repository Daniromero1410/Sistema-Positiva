import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Dashboard
export const dashboardAPI = {
  getStats: () => api.get('/api/dashboard/stats'),
  getEjecucionesRecientes: (limit = 5) => api.get(`/api/dashboard/ejecuciones-recientes?limit=${limit}`),
  getServiciosPorMes: () => api.get('/api/dashboard/servicios-por-mes'),
  getContratosPorDepartamento: () => api.get('/api/dashboard/contratos-por-departamento'),
}

// Consolidador
export const consolidadorAPI = {
  uploadMaestra: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/api/consolidador/upload-maestra', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  iniciar: (config: any) => api.post('/api/consolidador/iniciar', config),
  getProgreso: (ejecucionId: number) => api.get(`/api/consolidador/progreso/${ejecucionId}`),
  getResultados: (ejecucionId: number) => api.get(`/api/consolidador/resultados/${ejecucionId}`),
  cancelar: (ejecucionId: number) => api.post(`/api/consolidador/cancelar/${ejecucionId}`),
}

// FTP
export const ftpAPI = {
  getStatus: () => api.get('/api/ftp/status'),
  browse: (path = '/') => api.get(`/api/ftp/browse?path=${encodeURIComponent(path)}`),
  preview: (path: string, hoja?: string) => api.get(`/api/ftp/preview?path=${encodeURIComponent(path)}&hoja=${hoja || ''}`),
  download: (path: string) => api.post('/api/ftp/download', { path }),
}

// Consulta
export const consultaAPI = {
  search: (params: any) => api.get('/api/consulta/search', { params }),
  getSugerencias: (q: string, limit = 10) => api.get(`/api/consulta/sugerencias?q=${q}&limit=${limit}`),
  getDetalle: (servicioId: number) => api.get(`/api/consulta/detalle/${servicioId}`),
  getFiltros: () => api.get('/api/consulta/filtros'),
}

// Mapa
export const mapaAPI = {
  getDatos: (params?: any) => api.get('/api/mapa/datos', { params }),
  getTopCiudades: (limit = 10) => api.get(`/api/mapa/top-ciudades?limit=${limit}`),
  getDepartamentos: () => api.get('/api/mapa/departamentos'),
}

// Archivos
export const archivosAPI = {
  download: (ejecucionId: number, tipo: string) => {
    return `${API_URL}/api/archivos/download/${ejecucionId}/${tipo}`
  },
  list: () => api.get('/api/archivos/list'),
}
