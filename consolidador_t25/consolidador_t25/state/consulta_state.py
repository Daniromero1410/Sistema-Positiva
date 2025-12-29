"""
Estado del módulo de consulta de datos.
"""
import reflex as rx
from typing import Optional, List, Dict
from datetime import datetime


class ConsultaState(rx.State):
    """Estado de consulta de datos."""

    # Búsqueda
    busqueda: str = ""
    sugerencias: List[str] = []
    show_sugerencias: bool = False

    # Filtros
    filtro_departamento: str = "Todos"
    filtro_ano: str = "Todos"
    filtro_manual: str = "Todos"
    filtro_categoria: str = "Todos"

    # Opciones de filtros
    departamentos_disponibles: List[str] = ["Todos", "BOGOTA", "ANTIOQUIA", "VALLE DEL CAUCA", "ATLANTICO", "SANTANDER"]
    anos_disponibles: List[str] = ["Todos", "2025", "2024", "2023"]
    manuales_disponibles: List[str] = ["Todos", "SOAT", "ISS 2001", "ISS 2004", "PROPIO"]
    categorias_disponibles: List[str] = ["Todos", "Cuentas médicas", "Ambulancias", "Hospitalización"]

    # Resultados
    resultados: List[Dict] = []
    total_resultados: int = 0
    pagina_actual: int = 1
    registros_por_pagina: int = 20
    total_paginas: int = 1

    # Ordenamiento
    ordenar_por: str = "contrato"
    orden_ascendente: bool = True

    # Detalle
    show_detalle: bool = False
    registro_detalle: Optional[Dict] = None

    # Loading
    buscando: bool = False

    # Exportación
    exportando: bool = False

    async def buscar(self):
        """Realiza la búsqueda de datos."""
        self.buscando = True
        self.pagina_actual = 1

        try:
            import asyncio
            await asyncio.sleep(0.5)  # Simular latencia

            # Simular resultados
            self._generar_resultados_demo()
        finally:
            self.buscando = False

    def _generar_resultados_demo(self):
        """Genera resultados de demostración."""
        # Datos de ejemplo
        base_resultados = [
            {
                "id": 1,
                "contrato": "0123-2025",
                "proveedor": "Hospital San José",
                "nit": "900.123.456-7",
                "cups": "890201",
                "descripcion": "CONSULTA DE PRIMERA VEZ POR MEDICINA GENERAL",
                "tarifa": 45000,
                "manual": "SOAT",
                "porcentaje": 25,
                "departamento": "ATLANTICO",
                "municipio": "BARRANQUILLA",
                "habilitacion": "08001234567-01",
                "origen": "Inicial",
                "otrosi": None,
                "fecha_procesamiento": "28/12/2025"
            },
            {
                "id": 2,
                "contrato": "0124-2025",
                "proveedor": "Clínica Santa María",
                "nit": "900.234.567-8",
                "cups": "890201",
                "descripcion": "CONSULTA DE PRIMERA VEZ POR MEDICINA GENERAL",
                "tarifa": 43500,
                "manual": "SOAT",
                "porcentaje": 20,
                "departamento": "BOGOTA",
                "municipio": "BOGOTA",
                "habilitacion": "11001234567-01",
                "origen": "Otrosí",
                "otrosi": 1,
                "fecha_procesamiento": "27/12/2025"
            },
            {
                "id": 3,
                "contrato": "0125-2025",
                "proveedor": "IPS Salud Total",
                "nit": "900.345.678-9",
                "cups": "890201",
                "descripcion": "CONSULTA DE PRIMERA VEZ POR MEDICINA GENERAL",
                "tarifa": 42000,
                "manual": "ISS 2004",
                "porcentaje": 30,
                "departamento": "ANTIOQUIA",
                "municipio": "MEDELLIN",
                "habilitacion": "05001234567-01",
                "origen": "Inicial",
                "otrosi": None,
                "fecha_procesamiento": "26/12/2025"
            },
        ]

        # Multiplicar para simular más resultados
        self.resultados = []
        for i in range(50):
            for base in base_resultados:
                nuevo = base.copy()
                nuevo["id"] = len(self.resultados) + 1
                self.resultados.append(nuevo)

        # Filtrar por búsqueda
        if self.busqueda:
            busqueda = self.busqueda.upper()
            self.resultados = [
                r for r in self.resultados
                if busqueda in r["cups"].upper()
                or busqueda in r["descripcion"].upper()
                or busqueda in r["contrato"].upper()
                or busqueda in r["proveedor"].upper()
            ]

        # Filtrar por departamento
        if self.filtro_departamento != "Todos":
            self.resultados = [
                r for r in self.resultados
                if r["departamento"] == self.filtro_departamento
            ]

        # Filtrar por año
        if self.filtro_ano != "Todos":
            self.resultados = [
                r for r in self.resultados
                if self.filtro_ano in r["contrato"]
            ]

        # Filtrar por manual
        if self.filtro_manual != "Todos":
            self.resultados = [
                r for r in self.resultados
                if r["manual"] == self.filtro_manual
            ]

        self.total_resultados = len(self.resultados)
        self.total_paginas = max(1, (self.total_resultados + self.registros_por_pagina - 1) // self.registros_por_pagina)

        # Paginar
        inicio = (self.pagina_actual - 1) * self.registros_por_pagina
        fin = inicio + self.registros_por_pagina
        self.resultados = self.resultados[inicio:fin]

    def set_busqueda(self, texto: str):
        """Establece el texto de búsqueda y genera sugerencias."""
        self.busqueda = texto
        if len(texto) >= 2:
            self._generar_sugerencias()
            self.show_sugerencias = True
        else:
            self.sugerencias = []
            self.show_sugerencias = False

    def _generar_sugerencias(self):
        """Genera sugerencias de búsqueda."""
        # Simular sugerencias basadas en la búsqueda
        busqueda = self.busqueda.upper()
        todas_sugerencias = [
            "890201 - Consulta medicina general",
            "890301 - Consulta especialista",
            "890401 - Consulta subespecialista",
            "890701 - Consulta nutrición",
            "Hospital San José",
            "Clínica Santa María",
            "0123-2025",
            "0124-2025",
        ]
        self.sugerencias = [s for s in todas_sugerencias if busqueda in s.upper()][:5]

    def seleccionar_sugerencia(self, sugerencia: str):
        """Selecciona una sugerencia de búsqueda."""
        self.busqueda = sugerencia.split(" - ")[0]
        self.show_sugerencias = False

    def ocultar_sugerencias(self):
        """Oculta las sugerencias."""
        self.show_sugerencias = False

    def set_filtro_departamento(self, valor: str):
        """Establece el filtro de departamento."""
        self.filtro_departamento = valor

    def set_filtro_ano(self, valor: str):
        """Establece el filtro de año."""
        self.filtro_ano = valor

    def set_filtro_manual(self, valor: str):
        """Establece el filtro de manual tarifario."""
        self.filtro_manual = valor

    def set_filtro_categoria(self, valor: str):
        """Establece el filtro de categoría."""
        self.filtro_categoria = valor

    def limpiar_filtros(self):
        """Limpia todos los filtros."""
        self.filtro_departamento = "Todos"
        self.filtro_ano = "Todos"
        self.filtro_manual = "Todos"
        self.filtro_categoria = "Todos"

    def cambiar_pagina(self, pagina: int):
        """Cambia a una página específica."""
        if 1 <= pagina <= self.total_paginas:
            self.pagina_actual = pagina
            self._generar_resultados_demo()

    def pagina_anterior(self):
        """Va a la página anterior."""
        if self.pagina_actual > 1:
            self.cambiar_pagina(self.pagina_actual - 1)

    def pagina_siguiente(self):
        """Va a la página siguiente."""
        if self.pagina_actual < self.total_paginas:
            self.cambiar_pagina(self.pagina_actual + 1)

    def ordenar(self, campo: str):
        """Ordena los resultados por un campo."""
        if self.ordenar_por == campo:
            self.orden_ascendente = not self.orden_ascendente
        else:
            self.ordenar_por = campo
            self.orden_ascendente = True

        # Ordenar resultados
        reverse = not self.orden_ascendente
        self.resultados = sorted(
            self.resultados,
            key=lambda x: x.get(campo, ""),
            reverse=reverse
        )

    def ver_detalle(self, registro_id: int):
        """Muestra el detalle de un registro."""
        registro = next((r for r in self.resultados if r["id"] == registro_id), None)
        if registro:
            self.registro_detalle = registro
            self.show_detalle = True

    def cerrar_detalle(self):
        """Cierra el modal de detalle."""
        self.show_detalle = False
        self.registro_detalle = None

    async def exportar_excel(self):
        """Exporta los resultados a Excel."""
        self.exportando = True

        try:
            import asyncio
            await asyncio.sleep(1)  # Simular generación

            # En implementación real, generaría el archivo Excel
            # y retornaría rx.download()
        finally:
            self.exportando = False
