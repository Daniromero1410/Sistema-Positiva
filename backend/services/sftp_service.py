# -*- coding: utf-8 -*-
"""
Servicio SFTP - Conexión a GoAnywhere
"""
import paramiko
import stat
import time
import re
from typing import List, Dict, Optional, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime
import os

from config import SFTP_CONFIG
from services.excel_processor import (
    es_archivo_tarifas_valido, 
    extraer_numero_otrosi,
    clasificar_tipo_archivo,
    contiene_anexo1
)

@dataclass
class SFTPItem:
    """Representa un archivo o directorio en el SFTP."""
    nombre: str
    tamano: int
    es_directorio: bool
    fecha_modificacion: float
    ruta_completa: str = ""
    
    @property
    def fecha_formateada(self) -> str:
        if self.fecha_modificacion:
            return datetime.fromtimestamp(self.fecha_modificacion).strftime('%d/%m/%Y %H:%M')
        return ""
    
    @property
    def tamano_formateado(self) -> str:
        if self.es_directorio:
            return "-"
        if self.tamano < 1024:
            return f"{self.tamano} B"
        elif self.tamano < 1024 * 1024:
            return f"{self.tamano / 1024:.1f} KB"
        else:
            return f"{self.tamano / (1024 * 1024):.1f} MB"

class SFTPService:
    """Cliente SFTP con manejo de reconexión automática."""
    
    def __init__(self, config: SFTP_CONFIG = None):
        self.config = config or SFTP_CONFIG
        self._client: Optional[paramiko.SSHClient] = None
        self._sftp: Optional[paramiko.SFTPClient] = None
        self._transport: Optional[paramiko.Transport] = None
        self._reconexiones = 0
        self._current_path = "/"
        self._connected = False
    
    def _cerrar(self):
        """Cierra todas las conexiones."""
        for c in [self._sftp, self._client]:
            try:
                if c:
                    c.close()
            except:
                pass
        try:
            if self._transport:
                self._transport.close()
        except:
            pass
        self._sftp = self._client = self._transport = None
        self._connected = False
    
    def conectar(self, host: str = None, port: int = None, 
                 username: str = None, password: str = None,
                 silencioso: bool = False) -> Tuple[bool, str]:
        """
        Establece conexión SFTP.
        
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        self._cerrar()
        
        # Usar parámetros o configuración por defecto
        host = host or self.config.HOST
        port = port or self.config.PORT
        username = username or self.config.USERNAME
        password = password or self.config.PASSWORD
        
        if not all([host, username, password]):
            return False, "Faltan credenciales de conexión"
        
        for intento in range(self.config.MAX_REINTENTOS_CONEXION):
            try:
                self._client = paramiko.SSHClient()
                self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self._client.connect(
                    hostname=host,
                    port=port,
                    username=username,
                    password=password,
                    timeout=self.config.TIMEOUT_CONEXION,
                    banner_timeout=self.config.TIMEOUT_CONEXION,
                    auth_timeout=self.config.TIMEOUT_CONEXION,
                    allow_agent=False,
                    look_for_keys=False
                )
                
                self._transport = self._client.get_transport()
                self._transport.set_keepalive(self.config.KEEPALIVE_INTERVAL)
                self._sftp = self._client.open_sftp()
                self._sftp.get_channel().settimeout(self.config.TIMEOUT_OPERACION)
                self._current_path = "/"
                self._connected = True
                
                return True, f"Conectado a {host}:{port}"
                
            except paramiko.AuthenticationException:
                self._cerrar()
                return False, "Error de autenticación: usuario o contraseña incorrectos"
            except paramiko.SSHException as e:
                self._cerrar()
                if intento < self.config.MAX_REINTENTOS_CONEXION - 1:
                    time.sleep(self.config.BACKOFF_BASE ** intento)
                    continue
                return False, f"Error SSH: {str(e)}"
            except Exception as e:
                self._cerrar()
                if intento < self.config.MAX_REINTENTOS_CONEXION - 1:
                    time.sleep(self.config.BACKOFF_BASE ** intento)
                    continue
                return False, f"Error de conexión: {str(e)}"
        
        return False, "No se pudo conectar después de varios intentos"
    
    def reconectar(self) -> Tuple[bool, str]:
        """Fuerza una reconexión."""
        self._reconexiones += 1
        self._cerrar()
        time.sleep(0.5)
        return self.conectar(silencioso=True)
    
    def esta_conectado(self) -> bool:
        """Verifica si la conexión está activa."""
        try:
            if not self._sftp or not self._transport:
                return False
            if not self._transport.is_active():
                return False
            self._sftp.getcwd()
            return True
        except:
            return False
    
    def _ejecutar(self, operacion: Callable, descripcion: str = "operación"):
        """Ejecuta una operación con manejo de reconexión."""
        for intento in range(self.config.MAX_REINTENTOS_OPERACION):
            try:
                if not self.esta_conectado():
                    self._reconexiones += 1
                    success, msg = self.conectar(silencioso=True)
                    if not success:
                        raise Exception(f"Reconexión fallida: {msg}")
                return operacion()
            except Exception as e:
                if intento == self.config.MAX_REINTENTOS_OPERACION - 1:
                    raise
                time.sleep(1)
    
    def listar(self, ruta: str = '.') -> List[SFTPItem]:
        """Lista contenido de un directorio."""
        def _op():
            items = []
            for attr in self._sftp.listdir_attr(ruta):
                item = SFTPItem(
                    nombre=attr.filename,
                    tamano=attr.st_size or 0,
                    es_directorio=stat.S_ISDIR(attr.st_mode),
                    fecha_modificacion=attr.st_mtime or 0,
                    ruta_completa=f"{ruta}/{attr.filename}" if ruta != '/' else f"/{attr.filename}"
                )
                items.append(item)
            return sorted(items, key=lambda x: (not x.es_directorio, x.nombre.lower()))
        
        return self._ejecutar(_op, f"listar {ruta}")
    
    def cambiar_directorio(self, ruta: str) -> Tuple[bool, str]:
        """Cambia al directorio especificado."""
        try:
            def _op():
                self._sftp.chdir(ruta)
                self._current_path = self._sftp.getcwd() or ruta
            self._ejecutar(_op)
            return True, self._current_path
        except Exception as e:
            return False, str(e)
    
    def descargar(self, remoto: str, local: str) -> Tuple[bool, str]:
        """Descarga un archivo."""
        try:
            self._ejecutar(lambda: self._sftp.get(remoto, local))
            return True, f"Descargado: {remoto}"
        except Exception as e:
            return False, str(e)
    
    def desconectar(self):
        """Cierra la conexión SFTP."""
        self._cerrar()
    
    @property
    def ruta_actual(self) -> str:
        return self._current_path
    
    @property
    def reconexiones(self) -> int:
        return self._reconexiones
    
    @property
    def conectado(self) -> bool:
        return self._connected and self.esta_conectado()


class BuscadorAnexos:
    """Buscador de archivos ANEXO 1 en GoAnywhere."""
    
    # Patrones para detectar archivos válidos
    EXTENSIONES_EXCEL = ('.xlsx', '.xls', '.xlsm', '.xlsb')
    
    # Palabras clave para EXCLUIR archivos
    PALABRAS_EXCLUIR = [
        'MEDICAMENT', 'MEDICAMENTO', 'MEDICAMENTOS',
        'FARMACO', 'FÁRMACO', 'FARMACOS', 'FÁRMACOS',
        'INSUMO', 'INSUMOS', 'ANALISIS DE TARIFA',
        'ANÁLISIS DE TARIFA', 'ANALISIS TARIFA'
    ]
    
    def __init__(self, sftp_service: SFTPService):
        self.sftp = sftp_service
        self.alertas = []
    
    def es_archivo_excel(self, nombre: str) -> bool:
        """Verifica si es un archivo Excel."""
        return nombre.lower().endswith(self.EXTENSIONES_EXCEL)
    
    def es_archivo_valido(self, nombre: str) -> Tuple[bool, str, str]:
        """
        Verifica si un archivo es válido para procesamiento.
        Uses v15.1 detection logic from excel_processor.
        
        Returns:
            Tuple[bool, str, str]: (es_valido, tipo, motivo)
        """
        if not nombre:
            return False, 'INVALIDO', 'Nombre vacío'
        
        # Use the improved file classification from excel_processor
        clasificacion = clasificar_tipo_archivo(nombre)
        
        if clasificacion['es_valido']:
            return True, clasificacion['tipo'], f"Detectado como {clasificacion['tipo']}"
        
        return False, 'INVALIDO', clasificacion['motivo_exclusion'] or 'No cumple patrones'
    
    def extraer_numero_otrosi(self, nombre: str) -> Optional[int]:
        """Extrae el número de otrosí del nombre del archivo. Uses v15.1 logic."""
        return extraer_numero_otrosi(nombre)
    
    def buscar_carpeta(self, carpetas: List[str], patron: str) -> Optional[str]:
        """Busca una carpeta que coincida con el patrón."""
        patron_upper = patron.upper()
        patron_sin_espacios = patron_upper.replace(' ', '')
        
        for carpeta in carpetas:
            carpeta_upper = carpeta.upper()
            carpeta_sin_espacios = carpeta_upper.replace(' ', '').replace('_', '').replace('-', '')
            
            if patron_upper in carpeta_upper:
                return carpeta
            if patron_sin_espacios in carpeta_sin_espacios:
                return carpeta
        
        return None
    
    def buscar_carpeta_contrato(self, carpetas: List[str], numero: str, 
                                 nombre_proveedor: str = None) -> Optional[str]:
        """Busca la carpeta de un contrato específico."""
        num = ''.join(filter(str.isdigit, str(numero)))
        
        variantes = [
            num,
            num.zfill(4),
            num.zfill(3),
            num.zfill(5),
            num.lstrip('0') or '0',
            '0' + num,
        ]
        
        variantes_unicas = list(dict.fromkeys(variantes))
        
        # Buscar por número de contrato
        for variante in variantes_unicas:
            for carpeta in carpetas:
                partes = re.split(r'[\s\-_]', carpeta)
                if partes and partes[0] == variante:
                    return carpeta
        
        # Buscar por prefijo
        for variante in variantes_unicas:
            for carpeta in carpetas:
                if (carpeta.startswith(variante + '-') or 
                    carpeta.startswith(variante + '_') or 
                    carpeta.startswith(variante + ' ')):
                    return carpeta
        
        # Buscar por nombre de proveedor
        if nombre_proveedor:
            nombre_limpio = nombre_proveedor.upper().strip()
            for carpeta in carpetas:
                if nombre_limpio in carpeta.upper():
                    return carpeta
        
        return None
    
    def navegar_a_contrato(self, ano: str, numero: str, 
                           nombre_proveedor: str = None) -> Tuple[bool, str, Optional[str]]:
        """
        Navega hasta la carpeta de un contrato.
        
        Returns:
            Tuple[bool, str, Optional[str]]: (éxito, mensaje, ruta_completa)
        """
        try:
            # Ir a raíz
            self.sftp.cambiar_directorio('/')
            items = self.sftp.listar('/')
            carpetas = [i.nombre for i in items if i.es_directorio]
            
            # Buscar carpeta principal
            carpeta_principal = self.buscar_carpeta(
                carpetas, 
                self.sftp.config.CARPETA_PRINCIPAL
            )
            if not carpeta_principal:
                return False, "Carpeta principal no encontrada", None
            
            self.sftp.cambiar_directorio(carpeta_principal)
            
            # Buscar carpeta del año
            items = self.sftp.listar('.')
            carpetas = [i.nombre for i in items if i.es_directorio]
            carpeta_ano = self.buscar_carpeta(carpetas, f'contratos {ano}')
            if not carpeta_ano:
                return False, f"Carpeta año {ano} no encontrada", None
            
            self.sftp.cambiar_directorio(carpeta_ano)
            
            # Buscar carpeta del contrato
            items = self.sftp.listar('.')
            carpetas = [i.nombre for i in items if i.es_directorio]
            carpeta_contrato = self.buscar_carpeta_contrato(carpetas, numero, nombre_proveedor)
            
            if not carpeta_contrato:
                return False, f"Contrato {numero} no encontrado en GoAnywhere", None
            
            self.sftp.cambiar_directorio(carpeta_contrato)
            ruta_completa = f"/{carpeta_principal}/{carpeta_ano}/{carpeta_contrato}"
            
            return True, "OK", ruta_completa
            
        except Exception as e:
            return False, str(e)[:100], None
    
    def descargar_anexos(self, carpeta_destino: str) -> Dict:
        """
        Descarga los archivos ANEXO 1 del contrato actual.
        
        Returns:
            Dict con información de los archivos descargados
        """
        resultado = {
            'exito': False,
            'archivos': [],
            'mensaje': '',
            'otrosis_encontrados': []
        }
        
        try:
            items = self.sftp.listar('.')
            carpetas = [i.nombre for i in items if i.es_directorio]
            
            # Buscar carpeta TARIFAS
            carpeta_tarifas = None
            for c in carpetas:
                if 'tarifa' in c.lower():
                    carpeta_tarifas = c
                    break
            
            if not carpeta_tarifas:
                resultado['mensaje'] = "Carpeta TARIFAS no encontrada"
                return resultado
            
            self.sftp.cambiar_directorio(carpeta_tarifas)
            items_tarifas = self.sftp.listar('.')
            
            # Filtrar archivos Excel
            archivos_excel = [i for i in items_tarifas 
                            if not i.es_directorio and self.es_archivo_excel(i.nombre)]
            
            anexos_iniciales = []
            anexos_otrosi = []
            
            for item in archivos_excel:
                es_valido, tipo, _ = self.es_archivo_valido(item.nombre)
                if not es_valido:
                    continue
                
                num_otrosi = self.extraer_numero_otrosi(item.nombre)
                if num_otrosi:
                    anexos_otrosi.append({
                        'item': item, 
                        'numero': num_otrosi, 
                        'tipo': tipo
                    })
                else:
                    anexos_iniciales.append({
                        'item': item, 
                        'tipo': tipo
                    })
            
            resultado['otrosis_encontrados'] = [a['numero'] for a in anexos_otrosi]
            
            # Seleccionar archivo principal (otrosí más reciente o inicial)
            archivo_principal = None
            origen = None
            numero_otrosi = None
            
            if anexos_otrosi:
                anexos_otrosi.sort(key=lambda x: x['numero'], reverse=True)
                archivo_principal = anexos_otrosi[0]['item']
                numero_otrosi = anexos_otrosi[0]['numero']
                origen = f"Otrosí {numero_otrosi}"
            elif anexos_iniciales:
                archivo_principal = anexos_iniciales[0]['item']
                origen = "Inicial"
            
            if archivo_principal:
                ruta_local = os.path.join(carpeta_destino, archivo_principal.nombre)
                success, msg = self.sftp.descargar(archivo_principal.nombre, ruta_local)
                
                if success:
                    resultado['archivos'].append({
                        'nombre': archivo_principal.nombre,
                        'ruta_local': ruta_local,
                        'origen': origen,
                        'numero_otrosi': numero_otrosi,
                        'fecha_modificacion': archivo_principal.fecha_modificacion
                    })
                    resultado['exito'] = True
                    resultado['mensaje'] = f"Descargado: {archivo_principal.nombre}"
                else:
                    resultado['mensaje'] = f"Error descargando: {msg}"
            else:
                resultado['mensaje'] = "No se encontró archivo ANEXO 1 válido"
            
            return resultado
            
        except Exception as e:
            resultado['mensaje'] = str(e)[:100]
            return resultado


# Instancia global del servicio SFTP
sftp_service = SFTPService()
