"""
Estado del explorador FTP GoAnywhere.
"""
import reflex as rx
from typing import Optional, List, Dict
from datetime import datetime


class FTPState(rx.State):
    """Estado del explorador FTP."""

    # Conexión
    conectado: bool = False
    conectando: bool = False
    error_conexion: str = ""

    # Navegación
    ruta_actual: str = "/R.A-ABASTECIMIENTO RED ASISTENCIAL"
    historial_rutas: List[str] = []

    # Árbol de carpetas
    carpetas: List[Dict] = []
    carpeta_expandida: Dict[str, bool] = {}

    # Archivos
    archivos: List[Dict] = []
    archivos_seleccionados: List[str] = []
    archivo_preview: Optional[Dict] = None

    # Búsqueda
    busqueda: str = ""
    resultados_busqueda: List[Dict] = []

    # Vista
    vista_tipo: str = "lista"  # lista, cuadricula
    ordenar_por: str = "nombre"  # nombre, tamano, fecha
    orden_ascendente: bool = True

    # Preview
    show_preview: bool = False
    preview_data: List[Dict] = []
    preview_hojas: List[str] = []
    preview_hoja_actual: str = ""
    preview_total_filas: int = 0

    # Loading
    cargando: bool = False

    async def conectar(self):
        """Conecta al servidor SFTP."""
        self.conectando = True
        self.error_conexion = ""

        try:
            # Simular conexión
            import asyncio
            await asyncio.sleep(1)

            # Cargar estructura inicial
            self._cargar_estructura_demo()

            self.conectado = True
        except Exception as e:
            self.error_conexion = str(e)
        finally:
            self.conectando = False

    def desconectar(self):
        """Desconecta del servidor SFTP."""
        self.conectado = False
        self.carpetas = []
        self.archivos = []

    def _cargar_estructura_demo(self):
        """Carga estructura de demostración."""
        # Simular estructura de carpetas
        self.carpetas = [
            {"nombre": "0123-2025", "tipo": "carpeta", "hijos": [
                {"nombre": "ACTAS", "tipo": "carpeta", "hijos": []},
                {"nombre": "TARIFAS", "tipo": "carpeta", "hijos": []},
                {"nombre": "DOCUMENTOS", "tipo": "carpeta", "hijos": []},
            ]},
            {"nombre": "0124-2025", "tipo": "carpeta", "hijos": [
                {"nombre": "ACTAS", "tipo": "carpeta", "hijos": []},
                {"nombre": "TARIFAS", "tipo": "carpeta", "hijos": []},
            ]},
            {"nombre": "0125-2025", "tipo": "carpeta", "hijos": [
                {"nombre": "ACTAS", "tipo": "carpeta", "hijos": []},
                {"nombre": "TARIFAS", "tipo": "carpeta", "hijos": []},
            ]},
            {"nombre": "0456-2024", "tipo": "carpeta", "hijos": [
                {"nombre": "TARIFAS", "tipo": "carpeta", "hijos": []},
            ]},
        ]

        # Simular archivos en la ruta actual
        self.archivos = [
            {
                "nombre": "ANEXO_1_HOSPITAL_SAN_JOSE.xlsx",
                "tamano": "2.3 MB",
                "tamano_bytes": 2411724,
                "fecha": "15/12/2025",
                "tipo": "xlsx"
            },
            {
                "nombre": "OTROSI_1_TARIFAS.xlsx",
                "tamano": "1.1 MB",
                "tamano_bytes": 1153434,
                "fecha": "20/12/2025",
                "tipo": "xlsx"
            },
            {
                "nombre": "TARIFAS_SERVICIOS.xlsb",
                "tamano": "890 KB",
                "tamano_bytes": 911360,
                "fecha": "10/12/2025",
                "tipo": "xlsb"
            },
            {
                "nombre": "CONTRATO_FIRMADO.pdf",
                "tamano": "3.5 MB",
                "tamano_bytes": 3670016,
                "fecha": "05/12/2025",
                "tipo": "pdf"
            },
        ]

    def navegar_a(self, ruta: str):
        """Navega a una ruta específica."""
        self.historial_rutas.append(self.ruta_actual)
        self.ruta_actual = ruta
        self._actualizar_archivos()

    def navegar_atras(self):
        """Navega a la ruta anterior."""
        if self.historial_rutas:
            self.ruta_actual = self.historial_rutas.pop()
            self._actualizar_archivos()

    def navegar_arriba(self):
        """Navega al directorio padre."""
        if "/" in self.ruta_actual and self.ruta_actual != "/":
            partes = self.ruta_actual.rsplit("/", 1)
            nueva_ruta = partes[0] if partes[0] else "/"
            self.navegar_a(nueva_ruta)

    def _actualizar_archivos(self):
        """Actualiza la lista de archivos según la ruta actual."""
        # En implementación real, esto haría una llamada SFTP
        pass

    def toggle_carpeta(self, nombre: str):
        """Expande o colapsa una carpeta."""
        if nombre in self.carpeta_expandida:
            self.carpeta_expandida[nombre] = not self.carpeta_expandida[nombre]
        else:
            self.carpeta_expandida[nombre] = True
        # Forzar actualización
        self.carpeta_expandida = self.carpeta_expandida.copy()

    def seleccionar_archivo(self, nombre: str):
        """Selecciona o deselecciona un archivo."""
        if nombre in self.archivos_seleccionados:
            self.archivos_seleccionados.remove(nombre)
        else:
            self.archivos_seleccionados.append(nombre)

    def seleccionar_todos(self):
        """Selecciona todos los archivos."""
        self.archivos_seleccionados = [a["nombre"] for a in self.archivos]

    def deseleccionar_todos(self):
        """Deselecciona todos los archivos."""
        self.archivos_seleccionados = []

    def set_busqueda(self, texto: str):
        """Establece el texto de búsqueda."""
        self.busqueda = texto
        if texto:
            self._buscar_archivos()
        else:
            self.resultados_busqueda = []

    def _buscar_archivos(self):
        """Busca archivos por nombre."""
        busqueda = self.busqueda.upper()
        self.resultados_busqueda = [
            a for a in self.archivos
            if busqueda in a["nombre"].upper()
        ]

    def cambiar_vista(self, tipo: str):
        """Cambia el tipo de vista."""
        self.vista_tipo = tipo

    def ordenar_archivos(self, campo: str):
        """Ordena los archivos por un campo."""
        if self.ordenar_por == campo:
            self.orden_ascendente = not self.orden_ascendente
        else:
            self.ordenar_por = campo
            self.orden_ascendente = True

        # Ordenar archivos
        reverse = not self.orden_ascendente
        if campo == "nombre":
            self.archivos = sorted(self.archivos, key=lambda x: x["nombre"], reverse=reverse)
        elif campo == "tamano":
            self.archivos = sorted(self.archivos, key=lambda x: x["tamano_bytes"], reverse=reverse)
        elif campo == "fecha":
            self.archivos = sorted(self.archivos, key=lambda x: x["fecha"], reverse=reverse)

    async def ver_preview(self, nombre: str):
        """Muestra la vista previa de un archivo."""
        self.cargando = True

        # Buscar el archivo
        archivo = next((a for a in self.archivos if a["nombre"] == nombre), None)
        if not archivo:
            self.cargando = False
            return

        self.archivo_preview = archivo

        # Simular datos de preview
        self.preview_hojas = ["TARIFAS DE SERVICIOS", "PAQUETES", "TRASLADOS"]
        self.preview_hoja_actual = self.preview_hojas[0]
        self.preview_total_filas = 1234

        # Simular datos de la hoja
        self.preview_data = [
            {"CUPS": "890201", "Descripción": "Consulta medicina general", "Tarifa": "$45,000", "Manual": "SOAT"},
            {"CUPS": "890301", "Descripción": "Consulta especialista", "Tarifa": "$65,000", "Manual": "SOAT"},
            {"CUPS": "890401", "Descripción": "Consulta subespecialista", "Tarifa": "$85,000", "Manual": "ISS"},
            {"CUPS": "890701", "Descripción": "Consulta nutrición", "Tarifa": "$35,000", "Manual": "SOAT"},
            {"CUPS": "890801", "Descripción": "Consulta psicología", "Tarifa": "$40,000", "Manual": "SOAT"},
        ]

        self.show_preview = True
        self.cargando = False

    def cerrar_preview(self):
        """Cierra la vista previa."""
        self.show_preview = False
        self.archivo_preview = None
        self.preview_data = []

    def cambiar_hoja_preview(self, hoja: str):
        """Cambia la hoja en la vista previa."""
        self.preview_hoja_actual = hoja
        # En implementación real, cargaría los datos de la hoja

    def descargar_seleccionados(self):
        """Descarga los archivos seleccionados."""
        # En implementación real, descargaría los archivos
        pass

    def copiar_ruta(self):
        """Copia la ruta actual al portapapeles."""
        # Esto se manejaría en el frontend con JavaScript
        pass
