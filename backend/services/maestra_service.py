# -*- coding: utf-8 -*-
"""
Servicio Maestra - Manejo de archivo maestra de contratos
"""
import pandas as pd
import os
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

from config import PROCESSING_CONFIG

@dataclass
class ColumnasMaestra:
    """Columnas identificadas en la maestra."""
    tipo_proveedor: Optional[str] = None
    numero_contrato: Optional[str] = None
    ano_contrato: Optional[str] = None
    cto: Optional[str] = None
    nit: Optional[str] = None
    nombre_proveedor: Optional[str] = None

class MaestraService:
    """Servicio para manejo del archivo maestra de contratos."""
    
    def __init__(self):
        self.df_maestra: Optional[pd.DataFrame] = None
        self.df_prestadores: Optional[pd.DataFrame] = None
        self.columnas = ColumnasMaestra()
        self.archivo_cargado: str = ""
        self.anos_disponibles: List[int] = []
    
    def cargar_maestra(self, archivo: str) -> Tuple[bool, str, Dict]:
        """
        Carga el archivo maestra de contratos.
        
        Args:
            archivo: Ruta al archivo Excel
            
        Returns:
            Tuple[bool, str, Dict]: (éxito, mensaje, estadísticas)
        """
        stats = {
            'total_registros': 0,
            'registros_prestadores': 0,
            'anos_disponibles': [],
            'columnas_identificadas': {}
        }
        
        try:
            # Leer archivo
            self.df_maestra = pd.read_excel(archivo)
            stats['total_registros'] = len(self.df_maestra)
            
            # Identificar columnas
            self._identificar_columnas()
            
            stats['columnas_identificadas'] = {
                'tipo_proveedor': self.columnas.tipo_proveedor,
                'numero_contrato': self.columnas.numero_contrato,
                'ano_contrato': self.columnas.ano_contrato,
                'cto': self.columnas.cto,
                'nit': self.columnas.nit,
                'nombre_proveedor': self.columnas.nombre_proveedor
            }
            
            # Filtrar prestadores de salud
            if self.columnas.tipo_proveedor:
                self.df_prestadores = self.df_maestra[
                    self.df_maestra[self.columnas.tipo_proveedor] == 'PRESTADOR DE SERVICIOS DE SALUD'
                ].copy()
            else:
                self.df_prestadores = self.df_maestra.copy()
            
            stats['registros_prestadores'] = len(self.df_prestadores)
            
            # Obtener años disponibles
            if self.columnas.ano_contrato:
                self.anos_disponibles = sorted([
                    int(a) for a in self.df_prestadores[self.columnas.ano_contrato].dropna().unique()
                    if str(a).isdigit()
                ])
                stats['anos_disponibles'] = self.anos_disponibles
            
            self.archivo_cargado = archivo
            
            return True, f"Maestra cargada: {stats['registros_prestadores']} prestadores", stats
            
        except Exception as e:
            return False, f"Error cargando maestra: {str(e)}", stats
    
    def _identificar_columnas(self):
        """Identifica las columnas relevantes en la maestra."""
        if self.df_maestra is None:
            return
        
        for col in self.df_maestra.columns:
            col_upper = str(col).upper().strip()
            
            if 'TIPO' in col_upper and 'PROVEEDOR' in col_upper:
                self.columnas.tipo_proveedor = col
            elif col_upper == 'CTO':
                self.columnas.cto = col
            elif ('NUMERO' in col_upper or 'NÚMERO' in col_upper) and 'CONTRATO' in col_upper:
                self.columnas.numero_contrato = col
            elif ('AÑO' in col_upper or 'ANO' in col_upper) and 'CONTRATO' in col_upper:
                self.columnas.ano_contrato = col
            elif 'NIT' in col_upper:
                self.columnas.nit = col
            elif ('NOMBRE' in col_upper or 'RAZON' in col_upper) and 'PROVEEDOR' in col_upper:
                self.columnas.nombre_proveedor = col
    
    def obtener_contratos_por_ano(self, ano: int) -> List[Dict]:
        """
        Obtiene lista de contratos para un año específico.
        
        Args:
            ano: Año a filtrar
            
        Returns:
            Lista de contratos con su información
        """
        if self.df_prestadores is None or not self.columnas.ano_contrato:
            return []
        
        df_ano = self.df_prestadores[
            self.df_prestadores[self.columnas.ano_contrato] == ano
        ]
        
        contratos = []
        for _, row in df_ano.iterrows():
            contrato = {
                'ano': ano,
                'numero': '',
                'nit': '',
                'nombre_proveedor': '',
                'cto': ''
            }
            
            if self.columnas.numero_contrato:
                num = row[self.columnas.numero_contrato]
                if pd.notna(num):
                    contrato['numero'] = str(int(num) if isinstance(num, float) else num).zfill(4)
            
            if self.columnas.nit:
                nit = row[self.columnas.nit]
                if pd.notna(nit):
                    contrato['nit'] = str(nit).replace('.0', '')
            
            if self.columnas.nombre_proveedor:
                nombre = row[self.columnas.nombre_proveedor]
                if pd.notna(nombre):
                    contrato['nombre_proveedor'] = str(nombre)
            
            if self.columnas.cto:
                cto = row[self.columnas.cto]
                if pd.notna(cto):
                    contrato['cto'] = str(cto)
            
            if contrato['numero']:
                contratos.append(contrato)
        
        return contratos
    
    def obtener_estadisticas_por_ano(self) -> Dict[int, int]:
        """Obtiene cantidad de contratos por año."""
        if self.df_prestadores is None or not self.columnas.ano_contrato:
            return {}
        
        return self.df_prestadores.groupby(
            self.columnas.ano_contrato
        ).size().to_dict()
    
    def buscar_contrato(self, numero: str, ano: int) -> Optional[Dict]:
        """
        Busca un contrato específico en la maestra.
        
        Args:
            numero: Número de contrato
            ano: Año del contrato
            
        Returns:
            Dict con información del contrato o None
        """
        if self.df_prestadores is None:
            return None
        
        numero_str = str(numero).zfill(4)
        
        # Buscar por CTO
        if self.columnas.cto:
            cto_buscar = f"{numero_str}-{ano}"
            mask = self.df_prestadores[self.columnas.cto] == cto_buscar
            if mask.any():
                row = self.df_prestadores[mask].iloc[0]
                return self._row_to_dict(row, ano)
        
        # Buscar por número y año
        if self.columnas.numero_contrato and self.columnas.ano_contrato:
            mask = (
                self.df_prestadores[self.columnas.numero_contrato].astype(str).str.zfill(4) == numero_str
            ) & (
                self.df_prestadores[self.columnas.ano_contrato].astype(int) == ano
            )
            if mask.any():
                row = self.df_prestadores[mask].iloc[0]
                return self._row_to_dict(row, ano)
        
        return None
    
    def _row_to_dict(self, row, ano: int) -> Dict:
        """Convierte una fila de DataFrame a diccionario."""
        result = {'ano': ano}
        
        if self.columnas.numero_contrato:
            num = row[self.columnas.numero_contrato]
            result['numero'] = str(int(num) if isinstance(num, float) else num).zfill(4) if pd.notna(num) else ''
        
        if self.columnas.nit:
            nit = row[self.columnas.nit]
            result['nit'] = str(nit).replace('.0', '') if pd.notna(nit) else ''
        
        if self.columnas.nombre_proveedor:
            nombre = row[self.columnas.nombre_proveedor]
            result['nombre_proveedor'] = str(nombre) if pd.notna(nombre) else ''
        
        if self.columnas.cto:
            cto = row[self.columnas.cto]
            result['cto'] = str(cto) if pd.notna(cto) else ''
        
        # Obtener todas las columnas de fecha
        result['fechas'] = {}
        for col in row.index:
            col_lower = str(col).lower()
            if 'fecha' in col_lower:
                val = row[col]
                if pd.notna(val):
                    if isinstance(val, datetime):
                        result['fechas'][col] = val.strftime('%d/%m/%Y')
                    else:
                        result['fechas'][col] = str(val)
        
        return result
    
    def obtener_fecha_acuerdo(self, numero: str, ano: int, origen: str, 
                              fecha_archivo: float = None) -> Tuple[Optional[str], bool]:
        """
        Obtiene fecha de acuerdo de la maestra.
        
        Args:
            numero: Número de contrato
            ano: Año del contrato
            origen: Origen de tarifa (Inicial, Otrosí 1, etc.)
            fecha_archivo: Timestamp del archivo (fallback)
            
        Returns:
            Tuple[Optional[str], bool]: (fecha, encontrada_en_maestra)
        """
        contrato = self.buscar_contrato(numero, ano)
        
        if not contrato or 'fechas' not in contrato:
            if fecha_archivo:
                fecha_str = datetime.fromtimestamp(fecha_archivo).strftime('%d/%m/%Y')
                return fecha_str, False
            return None, False
        
        fechas = contrato['fechas']
        
        # Buscar fecha según origen
        if origen == 'Inicial':
            for col, val in fechas.items():
                col_lower = col.lower()
                if 'inicial' in col_lower and 'otrosi' not in col_lower:
                    return val, True
        elif 'Otrosí' in origen or 'Otrosi' in origen:
            import re
            m = re.search(r'\d+', origen)
            if m:
                num = m.group()
                for col, val in fechas.items():
                    col_lower = col.lower()
                    if f'otrosi' in col_lower and num in col_lower:
                        return val, True
        
        # Fallback a fecha de archivo
        if fecha_archivo:
            fecha_str = datetime.fromtimestamp(fecha_archivo).strftime('%d/%m/%Y')
            return fecha_str, False
        
        return None, False


# Instancia global
maestra_service = MaestraService()
