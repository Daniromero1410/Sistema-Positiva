# -*- coding: utf-8 -*-
"""
Servicio Procesador de Excel - Extracción de servicios de ANEXO 1
"""
import pandas as pd
import re
import os
import zipfile
import threading
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime

from config import PROCESSING_CONFIG

# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTES Y VALIDADORES
# ══════════════════════════════════════════════════════════════════════════════

CIUDADES_COLOMBIA = {
    'BOGOTÁ', 'BOGOTA', 'MEDELLÍN', 'MEDELLIN', 'CALI', 'BARRANQUILLA',
    'CARTAGENA', 'BUCARAMANGA', 'CÚCUTA', 'CUCUTA', 'PEREIRA', 'IBAGUÉ',
    'IBAGUE', 'SANTA MARTA', 'MANIZALES', 'VILLAVICENCIO', 'PASTO',
    'MONTERÍA', 'MONTERIA', 'NEIVA', 'ARMENIA', 'SINCELEJO', 'POPAYÁN',
    'POPAYAN', 'VALLEDUPAR', 'TUNJA', 'FLORENCIA', 'QUIBDÓ', 'QUIBDO',
    'RIOHACHA', 'YOPAL', 'MOCOA', 'LETICIA', 'ARAUCA', 'PALMIRA',
    'BUENAVENTURA', 'CARTAGO', 'TULUA', 'BUGA', 'SOGAMOSO', 'DUITAMA',
    'GIRARDOT', 'FUSAGASUGA', 'ZIPAQUIRA', 'CHIA', 'SOACHA', 'RIONEGRO',
    'ENVIGADO', 'ITAGUI', 'BELLO', 'TUMACO', 'IPIALES'
}

DEPARTAMENTOS_COLOMBIA = {
    'ANTIOQUIA', 'ATLÁNTICO', 'ATLANTICO', 'BOLÍVAR', 'BOLIVAR',
    'BOYACÁ', 'BOYACA', 'CALDAS', 'CAQUETÁ', 'CAQUETA', 'CASANARE',
    'CAUCA', 'CESAR', 'CHOCÓ', 'CHOCO', 'CÓRDOBA', 'CORDOBA',
    'CUNDINAMARCA', 'HUILA', 'LA GUAJIRA', 'MAGDALENA', 'META',
    'NARIÑO', 'NARINO', 'NORTE DE SANTANDER', 'PUTUMAYO', 'QUINDÍO',
    'QUINDIO', 'RISARALDA', 'SANTANDER', 'SUCRE', 'TOLIMA',
    'VALLE', 'VALLE DEL CAUCA'
}

MUNICIPIOS_COLOMBIA = CIUDADES_COLOMBIA | DEPARTAMENTOS_COLOMBIA

HOJAS_EXCLUIR = {
    'INSTRUCCIONES', 'INFO', 'DATOS', 'CONTENIDO', 'INDICE', 'ÍNDICE',
    'GUIA DE USO', 'GUÍA DE USO', 'CONTROL DE CAMBIOS', 'HOJA1', 'SHEET1',
    'INSTRUCTIVO', 'PARAMETROS', 'PARÁMETROS', 'CONFIGURACION', 'CONFIGURACIÓN',
    'LISTA', 'LISTAS', 'VALIDACION', 'VALIDACIÓN', 'CATALOGO', 'CATÁLOGO',
    'RESUMEN', 'PORTADA', 'CARATULA', 'CARÁTULA', 'INICIO', 'HOME',
    'MENU', 'MENÚ', 'ANEXO TECNICO', 'ANEXO TÉCNICO', 'GLOSARIO',
    'PAQUETE', 'PAQUETES', 'TARIFAS PAQUETE', 'TARIFAS PAQUETES',
    'COSTO VIAJE', 'COSTO DE VIAJE', 'COSTOS VIAJE'
}

PALABRAS_HOJA_SERVICIOS = [
    'TARIFA DE SERV', 'TARIFAS DE SERV', 'TARIFA SERV', 'TARIFAS SERV',
    'SERVICIOS INDIVIDUALES', 'SOLICITUD', 'ANEXO 1', 'ANEXO'
]

PATRONES_DIRECCION = [
    'CARRERA ', 'CRA ', 'CRA. ', 'CR ', 'CALLE ', 'CL ', 'CL. ',
    'AVENIDA ', 'AV ', 'AV. ', 'DIAGONAL ', 'DG ', 'DG. ',
    'TRANSVERSAL ', 'TV ', 'TV. ', 'KM ', 'KILOMETRO', 'KILÓMETRO',
    'LOCAL ', 'PISO ', 'OFICINA ', 'OF ', 'CONSULTORIO', 'TORRE ',
    'BLOQUE ', 'MANZANA', 'CASA ', 'APARTAMENTO', 'APTO', 'EDIFICIO',
    'CENTRO COMERCIAL', 'C.C.', 'BARRIO ', 'VEREDA ', 'SECTOR '
]

PALABRAS_INVALIDAS_CUPS = [
    'CODIGO', 'CUPS', 'ITEM', 'DESCRIPCION', 'TARIFA', 'TOTAL', 'SUBTOTAL',
    'DEPARTAMENTO', 'MUNICIPIO', 'HABILITACION', 'DIRECCION', 'TELEFONO',
    'EMAIL', 'SEDE', 'NOMBRE', 'NUMERO', 'ESPECIALIDAD', 'MANUAL', 'OBSERV',
    'PORCENTAJE', 'HOMOLOGO', 'N°', 'NO.', 'NOTA', 'NOTAS', 'ACLARATORIA'
]

# ══════════════════════════════════════════════════════════════════════════════
# FUNCIONES UTILITARIAS
# ══════════════════════════════════════════════════════════════════════════════

def normalizar_texto(texto: Any) -> str:
    """Normaliza texto para comparaciones."""
    if texto is None:
        return ''
    s = str(texto).upper().strip()
    s = re.sub(r'\s+', ' ', s)
    return s

def detectar_formato_real(filepath: str) -> str:
    """Detecta el formato REAL de un archivo Excel."""
    try:
        with open(filepath, 'rb') as f:
            header = f.read(8)
        
        if header[:4] == b'PK\x03\x04':
            try:
                with zipfile.ZipFile(filepath, 'r') as z:
                    names = z.namelist()
                    if any('workbook.bin' in n.lower() for n in names):
                        return 'xlsb'
                    elif any('.xml' in n.lower() for n in names):
                        return 'xlsx'
                return 'xlsx'
            except zipfile.BadZipFile:
                return 'zip_corrupt'
        
        if header[:8] == b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1':
            return 'xls_old'
        
        return 'unknown'
    except Exception:
        return 'error'

def leer_excel(ruta: str, sheet_name=0, header=0, engine=None):
    """Lee archivo Excel con manejo automático de motor."""
    if engine:
        return pd.read_excel(ruta, engine=engine, sheet_name=sheet_name, header=header)
    
    formato = detectar_formato_real(ruta)
    
    try:
        if formato == 'xlsb':
            return pd.read_excel(ruta, engine='pyxlsb', sheet_name=sheet_name, header=header)
        elif formato == 'xlsx':
            return pd.read_excel(ruta, engine='openpyxl', sheet_name=sheet_name, header=header)
        elif formato == 'xls_old':
            return pd.read_excel(ruta, engine='xlrd', sheet_name=sheet_name, header=header)
    except:
        pass
    
    for eng in ['openpyxl', 'pyxlsb', 'xlrd']:
        try:
            return pd.read_excel(ruta, engine=eng, sheet_name=sheet_name, header=header)
        except:
            continue
    
    raise Exception(f"No se pudo leer: {ruta}")

def obtener_hojas(ruta: str) -> List[str]:
    """Obtiene lista de hojas de un archivo Excel."""
    formato = detectar_formato_real(ruta)
    
    if formato == 'xlsb':
        try:
            from pyxlsb import open_workbook
            with open_workbook(ruta) as wb:
                return list(wb.sheets)
        except:
            pass
    elif formato == 'xlsx':
        try:
            from openpyxl import load_workbook
            wb = load_workbook(ruta, read_only=True, data_only=True)
            hojas = wb.sheetnames
            wb.close()
            return hojas
        except:
            pass
    elif formato == 'xls_old':
        try:
            import xlrd
            wb = xlrd.open_workbook(ruta, on_demand=True)
            return wb.sheet_names()
        except:
            pass
    
    # Fallback
    try:
        xl = pd.ExcelFile(ruta)
        return xl.sheet_names
    except:
        return []

def leer_hoja_raw(ruta: str, hoja: str, max_filas: int = 20000) -> List[List]:
    """Lee una hoja de Excel como lista de listas."""
    try:
        df = leer_excel(ruta, sheet_name=hoja, header=None)
        df = df.head(max_filas)
        return df.values.tolist()
    except Exception as e:
        return []

def es_municipio_o_departamento(texto: str) -> bool:
    """Verifica si el texto es un municipio o departamento."""
    if not texto:
        return False
    texto_upper = normalizar_texto(texto)
    return texto_upper in MUNICIPIOS_COLOMBIA

def es_direccion(texto: str) -> bool:
    """Verifica si el texto parece ser una dirección."""
    if not texto:
        return False
    texto_upper = normalizar_texto(texto)
    return any(p in texto_upper for p in PATRONES_DIRECCION)

def validar_cups(codigo: Any) -> Tuple[bool, str]:
    """
    Valida si un código CUPS es válido.
    
    Returns:
        Tuple[bool, str]: (es_valido, codigo_limpio)
    """
    if codigo is None:
        return False, ''
    
    codigo_str = str(codigo).strip()
    
    # Limpiar formato
    if codigo_str.endswith('.0'):
        codigo_str = codigo_str[:-2]
    
    codigo_limpio = re.sub(r'[^\dA-Za-z]', '', codigo_str)
    
    if not codigo_limpio:
        return False, ''
    
    # Validar longitud (CUPS colombiano: 6-8 caracteres)
    if len(codigo_limpio) < 4 or len(codigo_limpio) > 10:
        return False, ''
    
    # Rechazar si es un municipio
    if normalizar_texto(codigo_str) in MUNICIPIOS_COLOMBIA:
        return False, ''
    
    # Rechazar valores monetarios
    if re.match(r'^\d{6,}$', codigo_limpio) and int(codigo_limpio) > 999999:
        return False, ''
    
    # Rechazar palabras inválidas
    codigo_upper = normalizar_texto(codigo_str)
    for palabra in PALABRAS_INVALIDAS_CUPS:
        if palabra in codigo_upper:
            return False, ''
    
    return True, codigo_limpio

def limpiar_tarifa(valor: Any) -> Optional[float]:
    """Limpia y convierte un valor de tarifa a float."""
    if valor is None:
        return None
    
    try:
        if isinstance(valor, (int, float)):
            return float(valor) if valor > 0 else None
        
        s = str(valor).strip()
        s = re.sub(r'[$,\s]', '', s)
        s = s.replace('.', '').replace(',', '.')
        
        if s and s != '-':
            f = float(s)
            return f if f > 0 else None
    except:
        pass
    
    return None

def normalizar_codigo_habilitacion(codigo: Any, sede: Any = None) -> str:
    """Normaliza código de habilitación con sede."""
    if codigo is None:
        return ''
    
    c = str(codigo).strip()
    if c.endswith('.0'):
        c = c[:-2]
    c_limpio = re.sub(r'[^\d]', '', c)
    
    if not c_limpio:
        return ''
    
    try:
        if sede is None:
            s = 1
        else:
            sede_str = str(sede).strip()
            if sede_str.endswith('.0'):
                sede_str = sede_str[:-2]
            sede_limpia = re.sub(r'[^\d]', '', sede_str)
            if sede_limpia == c_limpio or len(sede_limpia) > 5:
                s = 1
            else:
                s = int(float(sede_str)) if sede_str else 1
    except:
        s = 1
    
    return f"{c_limpio}-{str(s).zfill(2)}"

# ══════════════════════════════════════════════════════════════════════════════
# DETECTORES DE SECCIONES
# ══════════════════════════════════════════════════════════════════════════════

def es_encabezado_seccion_sedes(fila: List) -> bool:
    """Detecta si una fila es encabezado de sección de sedes."""
    if not fila:
        return False
    
    texto = ' '.join([str(c).upper() for c in fila if c is not None])
    
    patrones = [
        'CODIGO DE HABILITACION', 'CÓDIGO DE HABILITACIÓN',
        'CODIGO HABILITACION', 'CÓDIGO HABILITACIÓN',
        'DEPARTAMENTO', 'MUNICIPIO'
    ]
    
    if any(p in texto for p in patrones):
        if 'CUPS' not in texto and 'TARIFA' not in texto:
            return True
    
    return False

def es_encabezado_seccion_servicios(fila: List) -> bool:
    """Detecta si una fila es encabezado de sección de servicios."""
    if not fila:
        return False
    
    texto = ' '.join([str(c).upper() for c in fila if c is not None])
    
    patrones = [
        'CODIGO CUPS', 'CÓDIGO CUPS', 'COD CUPS', 'COD. CUPS',
        'TARIFA UNITARIA', 'MANUAL TARIFARIO'
    ]
    
    return any(p in texto for p in patrones)

def es_dato_de_sede(fila: List) -> bool:
    """Verifica si una fila contiene datos de sede."""
    if not fila:
        return False
    
    for celda in fila:
        if celda is not None:
            s = str(celda).strip()
            if s.endswith('.0'):
                s = s[:-2]
            s_limpio = re.sub(r'[^\d]', '', s)
            if s_limpio and s_limpio.isdigit() and 5 <= len(s_limpio) <= 12:
                return True
    
    return False

# ══════════════════════════════════════════════════════════════════════════════
# PROCESADOR DE ANEXOS
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class ResultadoProcesamiento:
    """Resultado del procesamiento de un archivo."""
    exito: bool = False
    servicios: List[Dict] = field(default_factory=list)
    sedes: List[Dict] = field(default_factory=list)
    alertas: List[Dict] = field(default_factory=list)
    mensaje: str = ""
    hoja_procesada: str = ""
    total_filas: int = 0

class ProcesadorAnexo:
    """Procesa archivos ANEXO 1 para extraer servicios."""
    
    def __init__(self, contrato_id: str = "", ano: str = "", 
                 origen_tarifa: str = "Inicial"):
        self.contrato_id = contrato_id
        self.ano = ano
        self.origen_tarifa = origen_tarifa
        self.alertas = []
    
    def agregar_alerta(self, tipo: str, mensaje: str, archivo: str = ""):
        """Agrega una alerta al procesamiento."""
        self.alertas.append({
            'tipo': tipo,
            'mensaje': mensaje,
            'archivo': archivo,
            'contrato': self.contrato_id,
            'timestamp': datetime.now().isoformat()
        })
    
    def debe_excluir_hoja(self, nombre_hoja: str) -> bool:
        """Verifica si una hoja debe ser excluida."""
        if not nombre_hoja:
            return True
        
        nombre_upper = nombre_hoja.upper().strip()
        
        if nombre_upper in HOJAS_EXCLUIR:
            return True
        
        patrones_excluir = ['COSTO VIAJE', 'PAQUETE', 'AMBULANCIA', 'TRASLADO']
        for patron in patrones_excluir:
            if patron in nombre_upper:
                return True
        
        return False
    
    def buscar_hoja_servicios(self, archivo: str) -> Optional[str]:
        """Busca la hoja de servicios en el archivo."""
        try:
            hojas = obtener_hojas(archivo)
            if not hojas:
                return None
            
            # Prioridad alta
            for hoja in hojas:
                if self.debe_excluir_hoja(hoja):
                    continue
                hoja_upper = hoja.upper()
                for palabra in PALABRAS_HOJA_SERVICIOS:
                    if palabra in hoja_upper:
                        return hoja
            
            # Segunda pasada: cualquier hoja no excluida
            for hoja in hojas:
                if not self.debe_excluir_hoja(hoja):
                    return hoja
            
            return None
        except Exception as e:
            return None
    
    def detectar_columnas(self, fila: List) -> Dict[str, int]:
        """Detecta índices de columnas en el encabezado."""
        idx = {
            'cups': -1,
            'homologo': -1,
            'descripcion': -1,
            'tarifa': -1,
            'tarifario': -1,
            'porcentaje': -1,
            'observaciones': -1
        }
        
        PATRONES = {
            'cups': ['CODIGO CUPS', 'CÓDIGO CUPS', 'COD CUPS', 'COD. CUPS'],
            'homologo': ['CODIGO HOMOLOGO', 'CÓDIGO HOMÓLOGO', 'COD HOMOLOGO'],
            'descripcion': ['DESCRIPCION DEL CUPS', 'DESCRIPCIÓN DEL CUPS', 
                           'DESCRIPCION CUPS', 'DESCRIPCIÓN CUPS'],
            'tarifa': ['TARIFA UNITARIA EN PESOS', 'TARIFA UNITARIA PESOS',
                      'TARIFA EN PESOS', 'TARIFA UNITARIA', 'VALOR UNITARIO'],
            'tarifario': ['MANUAL TARIFARIO', 'TARIFARIO', 'MANUAL TAR'],
            'porcentaje': ['TARIFA SEGUN TARIFARIO', 'PORCENTAJE TARIFARIO', 
                          'PORCENTAJE', '% TARIFARIO'],
            'observaciones': ['OBSERVACIONES', 'OBSERVACION', 'OBS', 'NOTAS']
        }
        
        for i, celda in enumerate(fila):
            t = normalizar_texto(celda)
            if not t:
                continue
            
            for campo, patrones in PATRONES.items():
                if idx[campo] != -1:
                    continue
                
                for patron in patrones:
                    if patron in t or t == patron.replace(' ', ''):
                        # Validaciones adicionales
                        if campo == 'cups' and 'HOMOLOGO' in t:
                            continue
                        if campo == 'tarifa' and ('TARIFARIO' in t or 'SEGUN' in t):
                            continue
                        if campo == 'tarifario' and 'UNITARIA' in t:
                            continue
                        
                        idx[campo] = i
                        break
        
        return idx
    
    def extraer_sedes_de_bloque(self, datos: List[List], inicio: int, 
                                 idx_hab: int, idx_sede: int) -> List[Dict]:
        """Extrae las sedes de un bloque de datos."""
        sedes = []
        k = inicio
        
        while k < len(datos) and len(sedes) < PROCESSING_CONFIG.MAX_SEDES:
            fila = datos[k]
            if not fila:
                k += 1
                continue
            
            if es_encabezado_seccion_sedes(fila) or es_encabezado_seccion_servicios(fila):
                break
            
            if es_dato_de_sede(fila):
                if 0 <= idx_hab < len(fila):
                    codigo_hab = fila[idx_hab]
                    if codigo_hab:
                        codigo_str = str(codigo_hab).strip()
                        if codigo_str.endswith('.0'):
                            codigo_str = codigo_str[:-2]
                        codigo_clean = re.sub(r'[^\d]', '', codigo_str)
                        
                        if codigo_clean and codigo_clean.isdigit() and 5 <= len(codigo_clean) <= 12:
                            num_sede = fila[idx_sede] if 0 <= idx_sede < len(fila) else len(sedes) + 1
                            sedes.append({
                                'codigo': codigo_hab, 
                                'sede': num_sede
                            })
                            k += 1
                            continue
            
            if fila[0] is not None:
                primera = str(fila[0]).upper().strip()
                if not es_municipio_o_departamento(primera) and not es_direccion(primera):
                    if primera and not primera.isspace():
                        break
            
            k += 1
        
        return sedes
    
    def procesar(self, archivo: str, nombre_archivo: str = "") -> ResultadoProcesamiento:
        """
        Procesa un archivo ANEXO 1.
        
        Args:
            archivo: Ruta al archivo
            nombre_archivo: Nombre para mostrar
            
        Returns:
            ResultadoProcesamiento
        """
        resultado = ResultadoProcesamiento()
        nombre = nombre_archivo or os.path.basename(archivo)
        
        try:
            # Buscar hoja de servicios
            hoja = self.buscar_hoja_servicios(archivo)
            if not hoja:
                self.agregar_alerta('HOJA_NO_ENCONTRADA', 
                                   'No se encontró hoja de servicios válida', nombre)
                resultado.mensaje = "Hoja de servicios no encontrada"
                return resultado
            
            resultado.hoja_procesada = hoja
            
            # Leer datos
            datos = leer_hoja_raw(archivo, hoja)
            if not datos:
                self.agregar_alerta('HOJA_VACIA', 'Hoja vacía o no legible', nombre)
                resultado.mensaje = "Hoja vacía"
                return resultado
            
            resultado.total_filas = len(datos)
            
            servicios = []
            sedes_activas = []
            idx_columnas = None
            
            i = 0
            while i < len(datos):
                fila = datos[i]
                
                if not fila or all(c is None for c in fila):
                    i += 1
                    continue
                
                # Detectar sección de sedes
                if es_encabezado_seccion_sedes(fila):
                    idx_hab = -1
                    idx_sede = -1
                    for j, c in enumerate(fila):
                        t = normalizar_texto(c) if c else ''
                        if 'HABILITACION' in t or 'HABIITACION' in t:
                            idx_hab = j
                        if 'NUMERO DE SEDE' in t or 'N SEDE' in t or 'N° SEDE' in t:
                            idx_sede = j
                    
                    if idx_sede == -1 and idx_hab >= 0:
                        idx_sede = idx_hab + 1
                    
                    nuevas_sedes = self.extraer_sedes_de_bloque(datos, i + 1, idx_hab, idx_sede)
                    if nuevas_sedes:
                        sedes_activas = nuevas_sedes
                        resultado.sedes.extend(nuevas_sedes)
                    
                    i += 1
                    continue
                
                # Detectar sección de servicios
                if es_encabezado_seccion_servicios(fila):
                    idx_columnas = self.detectar_columnas(fila)
                    i += 1
                    continue
                
                # Procesar fila de servicio
                if idx_columnas and idx_columnas['cups'] >= 0:
                    if idx_columnas['cups'] < len(fila):
                        cups_raw = fila[idx_columnas['cups']]
                        es_valido, cups_limpio = validar_cups(cups_raw)
                        
                        if es_valido:
                            servicio = {
                                'codigo_cups': cups_limpio,
                                'descripcion_cups': '',
                                'codigo_homologo': '',
                                'tarifa_unitaria': None,
                                'manual_tarifario': '',
                                'porcentaje_tarifario': '',
                                'observaciones': '',
                                'origen_tarifa': self.origen_tarifa,
                                'contrato': self.contrato_id,
                                'ano': self.ano,
                                'archivo_origen': nombre,
                                'hoja_origen': hoja
                            }
                            
                            # Extraer descripción
                            if idx_columnas['descripcion'] >= 0 and idx_columnas['descripcion'] < len(fila):
                                desc = fila[idx_columnas['descripcion']]
                                if desc:
                                    servicio['descripcion_cups'] = str(desc).strip()[:500]
                            
                            # Extraer código homólogo
                            if idx_columnas['homologo'] >= 0 and idx_columnas['homologo'] < len(fila):
                                hom = fila[idx_columnas['homologo']]
                                if hom:
                                    servicio['codigo_homologo'] = str(hom).strip()[:20]
                            
                            # Extraer tarifa
                            if idx_columnas['tarifa'] >= 0 and idx_columnas['tarifa'] < len(fila):
                                tarifa = limpiar_tarifa(fila[idx_columnas['tarifa']])
                                servicio['tarifa_unitaria'] = tarifa
                            
                            # Extraer manual tarifario
                            if idx_columnas['tarifario'] >= 0 and idx_columnas['tarifario'] < len(fila):
                                man = fila[idx_columnas['tarifario']]
                                if man:
                                    servicio['manual_tarifario'] = str(man).strip()[:50]
                            
                            # Extraer porcentaje
                            if idx_columnas['porcentaje'] >= 0 and idx_columnas['porcentaje'] < len(fila):
                                pct = fila[idx_columnas['porcentaje']]
                                if pct:
                                    servicio['porcentaje_tarifario'] = str(pct).strip()[:20]
                            
                            # Extraer observaciones
                            if idx_columnas['observaciones'] >= 0 and idx_columnas['observaciones'] < len(fila):
                                obs = fila[idx_columnas['observaciones']]
                                if obs:
                                    servicio['observaciones'] = str(obs).strip()[:500]
                            
                            # Agregar sedes
                            if sedes_activas:
                                for sede in sedes_activas:
                                    servicio_con_sede = servicio.copy()
                                    servicio_con_sede['codigo_habilitacion'] = normalizar_codigo_habilitacion(
                                        sede['codigo'], sede['sede']
                                    )
                                    servicio_con_sede['numero_sede'] = sede['sede']
                                    servicios.append(servicio_con_sede)
                            else:
                                servicios.append(servicio)
                
                i += 1
            
            resultado.servicios = servicios
            resultado.alertas = self.alertas
            resultado.exito = len(servicios) > 0
            resultado.mensaje = f"Extraídos {len(servicios)} servicios" if servicios else "Sin servicios"
            
            return resultado
            
        except Exception as e:
            self.agregar_alerta('ERROR_PROCESAMIENTO', str(e)[:100], nombre)
            resultado.mensaje = str(e)[:100]
            resultado.alertas = self.alertas
            return resultado
    
    def procesar_con_timeout(self, archivo: str, nombre_archivo: str = "", 
                              timeout: int = None) -> ResultadoProcesamiento:
        """Procesa con timeout."""
        timeout = timeout or PROCESSING_CONFIG.TIMEOUT_ARCHIVO
        resultado = [ResultadoProcesamiento()]
        
        def worker():
            resultado[0] = self.procesar(archivo, nombre_archivo)
        
        thread = threading.Thread(target=worker)
        thread.start()
        thread.join(timeout)
        
        if thread.is_alive():
            self.agregar_alerta('TIMEOUT', f'Archivo tardó más de {timeout}s', nombre_archivo)
            resultado[0].mensaje = f"Timeout ({timeout}s)"
        
        return resultado[0]
