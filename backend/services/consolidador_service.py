# -*- coding: utf-8 -*-
"""
Servicio Consolidador T25 - Orquestador principal
"""
import os
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
import json

from config import PROCESSING_CONFIG
from services.sftp_service import SFTPService, BuscadorAnexos
from services.excel_processor import ProcesadorAnexo, ResultadoProcesamiento

@dataclass
class ContratoInfo:
    """Información de un contrato a procesar."""
    numero: str
    ano: str
    nit: str = ""
    nombre_proveedor: str = ""
    tipo_proveedor: str = ""

@dataclass
class ResultadoContrato:
    """Resultado del procesamiento de un contrato."""
    contrato: str
    ano: str
    estado: str = "pendiente"  # pendiente, procesado, error, sin_anexo
    mensaje: str = ""
    archivo_descargado: str = ""
    origen_tarifa: str = ""
    total_servicios: int = 0
    total_sedes: int = 0
    alertas: List[Dict] = field(default_factory=list)
    servicios: List[Dict] = field(default_factory=list)

@dataclass
class ResultadoConsolidacion:
    """Resultado completo de la consolidación."""
    exito: bool = False
    mensaje: str = ""
    
    # Estadísticas
    contratos_procesados: int = 0
    contratos_exitosos: int = 0
    contratos_fallidos: int = 0
    contratos_sin_anexo: int = 0
    total_servicios: int = 0
    total_alertas: int = 0
    
    # Resultados por contrato
    resultados: List[ResultadoContrato] = field(default_factory=list)
    
    # Datos consolidados
    servicios_consolidados: List[Dict] = field(default_factory=list)
    alertas_consolidadas: List[Dict] = field(default_factory=list)
    
    # Archivos generados
    archivo_consolidado: str = ""
    archivo_alertas: str = ""
    archivo_resumen: str = ""
    
    # Timestamps
    inicio: str = ""
    fin: str = ""
    duracion_segundos: float = 0

class ConsolidadorT25:
    """
    Orquestador principal del Consolidador T25.
    
    Coordina la conexión SFTP, navegación, descarga y procesamiento
    de archivos ANEXO 1 de contratos.
    """
    
    def __init__(self, sftp_service: SFTPService = None):
        self.sftp = sftp_service or SFTPService()
        self.buscador = None
        self.alertas = []
        self.logs = []
        self._progreso_callback = None
    
    def set_progreso_callback(self, callback):
        """Establece callback para reportar progreso."""
        self._progreso_callback = callback
    
    def _reportar_progreso(self, porcentaje: int, mensaje: str):
        """Reporta progreso al callback si está definido."""
        self.logs.append({
            'timestamp': datetime.now().isoformat(),
            'porcentaje': porcentaje,
            'mensaje': mensaje
        })
        if self._progreso_callback:
            self._progreso_callback(porcentaje, mensaje)
    
    def conectar(self, host: str = None, port: int = None,
                 username: str = None, password: str = None) -> Tuple[bool, str]:
        """Establece conexión SFTP."""
        self._reportar_progreso(5, "Conectando a GoAnywhere...")
        success, msg = self.sftp.conectar(host, port, username, password)
        
        if success:
            self.buscador = BuscadorAnexos(self.sftp)
            self._reportar_progreso(10, "Conexión establecida")
        else:
            self._reportar_progreso(0, f"Error de conexión: {msg}")
        
        return success, msg
    
    def desconectar(self):
        """Cierra la conexión SFTP."""
        self.sftp.desconectar()
    
    def procesar_contrato(self, contrato: ContratoInfo) -> ResultadoContrato:
        """
        Procesa un contrato individual.
        
        Args:
            contrato: Información del contrato
            
        Returns:
            ResultadoContrato
        """
        resultado = ResultadoContrato(
            contrato=contrato.numero,
            ano=contrato.ano
        )
        
        try:
            # Navegar al contrato
            success, msg, ruta = self.buscador.navegar_a_contrato(
                contrato.ano, 
                contrato.numero,
                contrato.nombre_proveedor
            )
            
            if not success:
                resultado.estado = "error" if "no encontrado" in msg.lower() else "sin_anexo"
                resultado.mensaje = msg
                resultado.alertas.append({
                    'tipo': 'CONTRATO_NO_ENCONTRADO',
                    'mensaje': msg,
                    'contrato': contrato.numero
                })
                return resultado
            
            # Crear directorio temporal
            temp_dir = os.path.join(PROCESSING_CONFIG.TEMP_DIR, f"{contrato.numero}_{contrato.ano}")
            os.makedirs(temp_dir, exist_ok=True)
            
            # Descargar anexos
            descarga = self.buscador.descargar_anexos(temp_dir)
            
            if not descarga['exito']:
                resultado.estado = "sin_anexo"
                resultado.mensaje = descarga['mensaje']
                resultado.alertas.append({
                    'tipo': 'SIN_ANEXO1',
                    'mensaje': descarga['mensaje'],
                    'contrato': contrato.numero
                })
                return resultado
            
            # Procesar archivo descargado
            archivo_info = descarga['archivos'][0]
            resultado.archivo_descargado = archivo_info['nombre']
            resultado.origen_tarifa = archivo_info['origen']
            
            procesador = ProcesadorAnexo(
                contrato_id=f"{contrato.numero}-{contrato.ano}",
                ano=contrato.ano,
                origen_tarifa=archivo_info['origen']
            )
            
            proc_resultado = procesador.procesar_con_timeout(
                archivo_info['ruta_local'],
                archivo_info['nombre']
            )
            
            if proc_resultado.exito:
                resultado.estado = "procesado"
                resultado.total_servicios = len(proc_resultado.servicios)
                resultado.total_sedes = len(proc_resultado.sedes)
                resultado.servicios = proc_resultado.servicios
                resultado.mensaje = f"Procesado: {resultado.total_servicios} servicios"
            else:
                resultado.estado = "error"
                resultado.mensaje = proc_resultado.mensaje
            
            resultado.alertas.extend(proc_resultado.alertas)
            
            # Limpiar archivos temporales
            try:
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)
            except:
                pass
            
            return resultado
            
        except Exception as e:
            resultado.estado = "error"
            resultado.mensaje = str(e)[:100]
            resultado.alertas.append({
                'tipo': 'ERROR_PROCESAMIENTO',
                'mensaje': str(e)[:100],
                'contrato': contrato.numero
            })
            return resultado
    
    def consolidar(self, contratos: List[ContratoInfo], 
                   generar_archivos: bool = True) -> ResultadoConsolidacion:
        """
        Consolida múltiples contratos.
        
        Args:
            contratos: Lista de contratos a procesar
            generar_archivos: Si debe generar archivos Excel
            
        Returns:
            ResultadoConsolidacion
        """
        resultado = ResultadoConsolidacion()
        resultado.inicio = datetime.now().isoformat()
        
        total = len(contratos)
        if total == 0:
            resultado.mensaje = "No hay contratos para procesar"
            return resultado
        
        self._reportar_progreso(15, f"Iniciando consolidación de {total} contratos...")
        
        todos_servicios = []
        todas_alertas = []
        
        for i, contrato in enumerate(contratos):
            porcentaje = 15 + int((i / total) * 70)
            self._reportar_progreso(
                porcentaje, 
                f"Procesando contrato {contrato.numero} ({i+1}/{total})..."
            )
            
            res_contrato = self.procesar_contrato(contrato)
            resultado.resultados.append(res_contrato)
            
            resultado.contratos_procesados += 1
            
            if res_contrato.estado == "procesado":
                resultado.contratos_exitosos += 1
                todos_servicios.extend(res_contrato.servicios)
            elif res_contrato.estado == "sin_anexo":
                resultado.contratos_sin_anexo += 1
            else:
                resultado.contratos_fallidos += 1
            
            todas_alertas.extend(res_contrato.alertas)
            
            # Reconectar periódicamente para evitar timeouts
            if (i + 1) % 10 == 0:
                self.sftp.reconectar()
        
        resultado.servicios_consolidados = todos_servicios
        resultado.alertas_consolidadas = todas_alertas
        resultado.total_servicios = len(todos_servicios)
        resultado.total_alertas = len(todas_alertas)
        
        # Generar archivos
        if generar_archivos and todos_servicios:
            self._reportar_progreso(90, "Generando archivos de salida...")
            resultado.archivo_consolidado = self._generar_excel_consolidado(todos_servicios)
            resultado.archivo_alertas = self._generar_excel_alertas(todas_alertas)
            resultado.archivo_resumen = self._generar_resumen(resultado)
        
        resultado.fin = datetime.now().isoformat()
        resultado.duracion_segundos = (
            datetime.fromisoformat(resultado.fin) - 
            datetime.fromisoformat(resultado.inicio)
        ).total_seconds()
        
        resultado.exito = resultado.contratos_exitosos > 0
        resultado.mensaje = (
            f"Consolidación completada: {resultado.contratos_exitosos}/{total} exitosos, "
            f"{resultado.total_servicios} servicios extraídos"
        )
        
        self._reportar_progreso(100, resultado.mensaje)
        
        return resultado
    
    def _generar_excel_consolidado(self, servicios: List[Dict]) -> str:
        """Genera archivo Excel con servicios consolidados."""
        if not servicios:
            return ""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        archivo = os.path.join(
            PROCESSING_CONFIG.OUTPUT_DIR, 
            f'CONSOLIDADO_T25_{timestamp}.xlsx'
        )
        
        df = pd.DataFrame(servicios)
        
        # Ordenar columnas
        columnas_orden = [
            'contrato', 'ano', 'codigo_cups', 'descripcion_cups',
            'codigo_homologo', 'tarifa_unitaria', 'manual_tarifario',
            'porcentaje_tarifario', 'codigo_habilitacion', 'numero_sede',
            'origen_tarifa', 'observaciones', 'archivo_origen', 'hoja_origen'
        ]
        columnas_disponibles = [c for c in columnas_orden if c in df.columns]
        df = df[columnas_disponibles]
        
        df.to_excel(archivo, index=False, sheet_name='CONSOLIDADO')
        
        return archivo
    
    def _generar_excel_alertas(self, alertas: List[Dict]) -> str:
        """Genera archivo Excel con alertas."""
        if not alertas:
            return ""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        archivo = os.path.join(
            PROCESSING_CONFIG.OUTPUT_DIR, 
            f'ALERTAS_T25_{timestamp}.xlsx'
        )
        
        df = pd.DataFrame(alertas)
        df.to_excel(archivo, index=False, sheet_name='ALERTAS')
        
        return archivo
    
    def _generar_resumen(self, resultado: ResultadoConsolidacion) -> str:
        """Genera archivo de resumen."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        archivo = os.path.join(
            PROCESSING_CONFIG.OUTPUT_DIR, 
            f'RESUMEN_T25_{timestamp}.xlsx'
        )
        
        # Crear resumen por contrato
        resumen_data = []
        for r in resultado.resultados:
            resumen_data.append({
                'Contrato': r.contrato,
                'Año': r.ano,
                'Estado': r.estado,
                'Mensaje': r.mensaje,
                'Archivo': r.archivo_descargado,
                'Origen': r.origen_tarifa,
                'Servicios': r.total_servicios,
                'Sedes': r.total_sedes,
                'Alertas': len(r.alertas)
            })
        
        df_resumen = pd.DataFrame(resumen_data)
        
        # Crear estadísticas
        stats_data = [{
            'Métrica': 'Total Contratos',
            'Valor': resultado.contratos_procesados
        }, {
            'Métrica': 'Contratos Exitosos',
            'Valor': resultado.contratos_exitosos
        }, {
            'Métrica': 'Contratos Sin Anexo',
            'Valor': resultado.contratos_sin_anexo
        }, {
            'Métrica': 'Contratos con Error',
            'Valor': resultado.contratos_fallidos
        }, {
            'Métrica': 'Total Servicios',
            'Valor': resultado.total_servicios
        }, {
            'Métrica': 'Total Alertas',
            'Valor': resultado.total_alertas
        }, {
            'Métrica': 'Duración (segundos)',
            'Valor': round(resultado.duracion_segundos, 2)
        }]
        
        df_stats = pd.DataFrame(stats_data)
        
        with pd.ExcelWriter(archivo, engine='openpyxl') as writer:
            df_stats.to_excel(writer, sheet_name='ESTADISTICAS', index=False)
            df_resumen.to_excel(writer, sheet_name='DETALLE', index=False)
        
        return archivo


# Instancia global del consolidador
consolidador_service = ConsolidadorT25()
