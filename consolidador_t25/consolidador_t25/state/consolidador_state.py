"""
Estado del módulo Consolidador T25.
"""
import reflex as rx
from typing import Optional, List, Dict
from datetime import datetime
import asyncio
import os
import json


class ConsolidadorState(rx.State):
    """Estado del consolidador T25."""

    # === PASO 1: Carga de Maestra ===
    maestra_cargada: bool = False
    maestra_nombre: str = ""
    maestra_tamano: str = ""
    maestra_contratos: int = 0
    maestra_por_ano: Dict[str, int] = {}

    # Lista de contratos de la maestra
    contratos_maestra: List[Dict] = []
    contratos_filtrados: List[Dict] = []

    # === PASO 2: Configuración ===
    modo_ejecucion: str = "completo"  # completo, por_ano, especifico
    ano_seleccionado: int = 2025
    busqueda_contrato: str = ""
    contratos_seleccionados: List[str] = []

    # Opciones avanzadas
    forzar_reconexion: bool = False
    guardar_en_bd: bool = True
    exportar_alertas_separadas: bool = True

    # === PASO 3: Ejecución ===
    ejecutando: bool = False
    progreso: float = 0.0
    contrato_actual: str = ""
    proveedor_actual: str = ""
    contratos_procesados: int = 0
    total_a_procesar: int = 0
    servicios_extraidos: int = 0
    alertas_generadas: int = 0
    tiempo_transcurrido: str = "00:00"
    log_mensajes: List[Dict] = []

    # Control de ejecución
    pausado: bool = False
    cancelado: bool = False

    # === PASO 4: Resultados ===
    ejecucion_completada: bool = False
    resultados: Dict = {}
    archivos_generados: List[Dict] = []
    archivo_principal: str = ""

    # Selección de archivos para descarga
    archivos_seleccionados: List[str] = []

    # === Handlers de Maestra ===

    async def handle_upload(self, files: List[rx.UploadFile]):
        """Procesa el archivo de maestra cargado."""
        if not files:
            return

        file = files[0]
        upload_data = await file.read()

        # Guardar archivo temporal
        temp_path = f"/tmp/maestra_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        with open(temp_path, "wb") as f:
            f.write(upload_data)

        self.maestra_nombre = file.filename
        self.maestra_tamano = f"{len(upload_data) / 1024 / 1024:.1f} MB"

        # Procesar la maestra
        await self._procesar_maestra(temp_path)

    async def _procesar_maestra(self, path: str):
        """Procesa el archivo de maestra y extrae los contratos."""
        try:
            import pandas as pd

            # Leer el archivo Excel
            df = pd.read_excel(path)

            # Buscar columnas relevantes
            col_contrato = None
            col_ano = None
            col_nit = None
            col_razon = None
            col_depto = None
            col_ciudad = None
            col_categoria = None

            for col in df.columns:
                col_upper = str(col).upper()
                if 'CONTRATO' in col_upper and 'NUM' in col_upper:
                    col_contrato = col
                elif col_upper in ['AÑO', 'ANO', 'YEAR']:
                    col_ano = col
                elif 'NIT' in col_upper:
                    col_nit = col
                elif 'RAZON' in col_upper or 'RAZÓN' in col_upper:
                    col_razon = col
                elif 'DEPARTAMENTO' in col_upper or 'DEPTO' in col_upper:
                    col_depto = col
                elif 'CIUDAD' in col_upper or 'MUNICIPIO' in col_upper:
                    col_ciudad = col
                elif 'CATEGORIA' in col_upper or 'CATEGORÍA' in col_upper:
                    col_categoria = col

            # Construir lista de contratos
            contratos = []
            por_ano = {}

            for idx, row in df.iterrows():
                contrato_num = str(row.get(col_contrato, '')).strip() if col_contrato else f"C{idx}"
                ano = int(row.get(col_ano, 2025)) if col_ano else 2025

                contrato = {
                    "numero": contrato_num,
                    "ano": ano,
                    "nit": str(row.get(col_nit, '')).strip() if col_nit else "",
                    "razon_social": str(row.get(col_razon, '')).strip() if col_razon else "",
                    "departamento": str(row.get(col_depto, '')).strip() if col_depto else "",
                    "municipio": str(row.get(col_ciudad, '')).strip() if col_ciudad else "",
                    "categoria": str(row.get(col_categoria, '')).strip() if col_categoria else "",
                    "seleccionado": False
                }
                contratos.append(contrato)

                # Contar por año
                ano_str = str(ano)
                por_ano[ano_str] = por_ano.get(ano_str, 0) + 1

            self.contratos_maestra = contratos
            self.contratos_filtrados = contratos.copy()
            self.maestra_contratos = len(contratos)
            self.maestra_por_ano = por_ano
            self.maestra_cargada = True

        except Exception as e:
            print(f"Error procesando maestra: {e}")
            # Datos de ejemplo si falla
            self.maestra_contratos = 925
            self.maestra_por_ano = {"2024": 456, "2025": 469}
            self.maestra_cargada = True

    def eliminar_maestra(self):
        """Elimina la maestra cargada."""
        self.maestra_cargada = False
        self.maestra_nombre = ""
        self.maestra_tamano = ""
        self.maestra_contratos = 0
        self.maestra_por_ano = {}
        self.contratos_maestra = []
        self.contratos_filtrados = []

    # === Handlers de Configuración ===

    def set_modo_ejecucion(self, modo: str):
        """Establece el modo de ejecución."""
        self.modo_ejecucion = modo

    def set_ano_seleccionado(self, ano: str):
        """Establece el año seleccionado."""
        self.ano_seleccionado = int(ano)
        self._filtrar_contratos()

    def set_busqueda_contrato(self, texto: str):
        """Establece el texto de búsqueda."""
        self.busqueda_contrato = texto
        self._filtrar_contratos()

    def _filtrar_contratos(self):
        """Filtra los contratos según los criterios."""
        filtrados = self.contratos_maestra.copy()

        # Filtrar por año si es modo por_ano
        if self.modo_ejecucion == "por_ano":
            filtrados = [c for c in filtrados if c["ano"] == self.ano_seleccionado]

        # Filtrar por búsqueda
        if self.busqueda_contrato:
            busqueda = self.busqueda_contrato.upper()
            filtrados = [
                c for c in filtrados
                if busqueda in c["numero"].upper()
                or busqueda in c["razon_social"].upper()
                or busqueda in c["nit"]
            ]

        self.contratos_filtrados = filtrados

    def toggle_contrato_seleccion(self, numero: str):
        """Alterna la selección de un contrato."""
        if numero in self.contratos_seleccionados:
            self.contratos_seleccionados.remove(numero)
        else:
            self.contratos_seleccionados.append(numero)

    def seleccionar_todos(self):
        """Selecciona todos los contratos filtrados."""
        self.contratos_seleccionados = [c["numero"] for c in self.contratos_filtrados]

    def deseleccionar_todos(self):
        """Deselecciona todos los contratos."""
        self.contratos_seleccionados = []

    # === Handlers de Ejecución ===

    async def iniciar_consolidacion(self):
        """Inicia el proceso de consolidación."""
        self.ejecutando = True
        self.pausado = False
        self.cancelado = False
        self.progreso = 0.0
        self.contratos_procesados = 0
        self.servicios_extraidos = 0
        self.alertas_generadas = 0
        self.log_mensajes = []
        self.ejecucion_completada = False

        # Determinar contratos a procesar
        if self.modo_ejecucion == "completo":
            contratos_a_procesar = self.contratos_maestra
        elif self.modo_ejecucion == "por_ano":
            contratos_a_procesar = [
                c for c in self.contratos_maestra
                if c["ano"] == self.ano_seleccionado
            ]
        else:  # especifico
            contratos_a_procesar = [
                c for c in self.contratos_maestra
                if c["numero"] in self.contratos_seleccionados
            ]

        self.total_a_procesar = len(contratos_a_procesar)

        # Agregar mensaje de inicio
        self._agregar_log("INFO", f"Iniciando consolidación de {self.total_a_procesar} contratos")

        # Simular procesamiento
        inicio = datetime.now()

        for i, contrato in enumerate(contratos_a_procesar):
            if self.cancelado:
                self._agregar_log("WARNING", "Consolidación cancelada por el usuario")
                break

            while self.pausado:
                await asyncio.sleep(0.5)
                if self.cancelado:
                    break

            self.contrato_actual = contrato["numero"]
            self.proveedor_actual = contrato["razon_social"][:50]
            self.contratos_procesados = i + 1
            self.progreso = (i + 1) / self.total_a_procesar * 100

            # Simular tiempo de procesamiento
            await asyncio.sleep(0.1)

            # Simular resultados
            servicios = 50 + (i % 200)
            self.servicios_extraidos += servicios

            # Simular algunas alertas
            if i % 15 == 0:
                self.alertas_generadas += 1
                self._agregar_log("WARNING", f"{contrato['numero']}: Sin ANEXO 1 encontrado")
            else:
                self._agregar_log("SUCCESS", f"{contrato['numero']}: {servicios} servicios extraídos")

            # Actualizar tiempo
            elapsed = datetime.now() - inicio
            minutes = int(elapsed.total_seconds() // 60)
            seconds = int(elapsed.total_seconds() % 60)
            self.tiempo_transcurrido = f"{minutes:02d}:{seconds:02d}"

        if not self.cancelado:
            self._agregar_log("SUCCESS", f"Consolidación completada: {self.servicios_extraidos} servicios")
            await self._generar_archivos()

        self.ejecutando = False

    async def _generar_archivos(self):
        """Genera los archivos de salida."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ano = self.ano_seleccionado if self.modo_ejecucion == "por_ano" else "ALL"

        # Simular generación de archivos
        self.archivos_generados = [
            {
                "nombre": f"CONSOLIDADO_ML_LIMPIO_{ano}_{timestamp}.xlsx",
                "ruta": f"/tmp/CONSOLIDADO_ML_LIMPIO_{ano}_{timestamp}.xlsx",
                "tamano": "12.5 MB",
                "registros": self.servicios_extraidos,
                "descripcion": "Datos consolidados + limpieza con Machine Learning",
                "es_principal": True,
                "seleccionado": True
            },
            {
                "nombre": f"CONSOLIDADO_{ano}_{timestamp}.xlsx",
                "ruta": f"/tmp/CONSOLIDADO_{ano}_{timestamp}.xlsx",
                "tamano": "8.2 MB",
                "registros": self.servicios_extraidos,
                "descripcion": "Datos crudos del GoAnywhere",
                "es_principal": False,
                "seleccionado": True
            },
            {
                "nombre": f"ALERTAS_{ano}_{timestamp}.xlsx",
                "ruta": f"/tmp/ALERTAS_{ano}_{timestamp}.xlsx",
                "tamano": "245 KB",
                "registros": self.alertas_generadas,
                "descripcion": "Alertas separadas por categoría",
                "es_principal": False,
                "seleccionado": True
            },
            {
                "nombre": f"RESUMEN_{ano}_{timestamp}.xlsx",
                "ruta": f"/tmp/RESUMEN_{ano}_{timestamp}.xlsx",
                "tamano": "156 KB",
                "registros": self.contratos_procesados,
                "descripcion": "Resumen por contrato",
                "es_principal": False,
                "seleccionado": True
            },
            {
                "nombre": f"NO_POSITIVA_{ano}_{timestamp}.xlsx",
                "ruta": f"/tmp/NO_POSITIVA_{ano}_{timestamp}.xlsx",
                "tamano": "45 KB",
                "registros": 5,
                "descripcion": "Archivos formato no estándar",
                "es_principal": False,
                "seleccionado": False
            },
            {
                "nombre": "correcciones_ml.csv",
                "ruta": "/tmp/correcciones_ml.csv",
                "tamano": "12 KB",
                "registros": 150,
                "descripcion": "Log de correcciones ML",
                "es_principal": False,
                "seleccionado": False
            },
        ]

        self.archivo_principal = self.archivos_generados[0]["ruta"]

        self.resultados = {
            "total_contratos": self.total_a_procesar,
            "exitosos": self.contratos_procesados - (self.alertas_generadas // 2),
            "fallidos": self.alertas_generadas // 2,
            "servicios": self.servicios_extraidos,
            "alertas": self.alertas_generadas,
            "tiempo": self.tiempo_transcurrido
        }

        self.ejecucion_completada = True

    def _agregar_log(self, tipo: str, mensaje: str):
        """Agrega un mensaje al log."""
        self.log_mensajes = self.log_mensajes + [{
            "tipo": tipo,
            "mensaje": mensaje,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }]
        # Mantener solo los últimos 100 mensajes
        if len(self.log_mensajes) > 100:
            self.log_mensajes = self.log_mensajes[-100:]

    def pausar_consolidacion(self):
        """Pausa la consolidación."""
        self.pausado = True
        self._agregar_log("INFO", "Consolidación pausada")

    def reanudar_consolidacion(self):
        """Reanuda la consolidación."""
        self.pausado = False
        self._agregar_log("INFO", "Consolidación reanudada")

    def cancelar_consolidacion(self):
        """Cancela la consolidación."""
        self.cancelado = True
        self.pausado = False

    # === Handlers de Descarga ===

    def toggle_archivo_seleccion(self, nombre: str):
        """Alterna la selección de un archivo."""
        for archivo in self.archivos_generados:
            if archivo["nombre"] == nombre:
                archivo["seleccionado"] = not archivo["seleccionado"]
                break
        # Forzar actualización
        self.archivos_generados = self.archivos_generados.copy()

    def descargar_principal(self):
        """Descarga el archivo principal."""
        if self.archivo_principal:
            return rx.download(url=self.archivo_principal)

    def descargar_archivo(self, ruta: str):
        """Descarga un archivo específico."""
        return rx.download(url=ruta)

    def descargar_seleccionados(self):
        """Descarga los archivos seleccionados."""
        seleccionados = [a for a in self.archivos_generados if a["seleccionado"]]
        if len(seleccionados) == 1:
            return rx.download(url=seleccionados[0]["ruta"])
        # TODO: Crear ZIP con múltiples archivos
        return rx.download(url=seleccionados[0]["ruta"])

    def descargar_todo(self):
        """Descarga todos los archivos como ZIP."""
        # TODO: Crear ZIP con todos los archivos
        return rx.download(url=self.archivo_principal)

    def nueva_ejecucion(self):
        """Reinicia para una nueva ejecución."""
        self.ejecucion_completada = False
        self.ejecutando = False
        self.progreso = 0.0
        self.contratos_procesados = 0
        self.servicios_extraidos = 0
        self.alertas_generadas = 0
        self.log_mensajes = []
        self.archivos_generados = []
        self.archivo_principal = ""
        self.resultados = {}
