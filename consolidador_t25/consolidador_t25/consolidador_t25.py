"""
Consolidador T25 - Aplicación Principal
Sistema de Gestión y Consolidación de Tarifas Médicas
POSITIVA Compañía de Seguros S.A.
"""

import reflex as rx

# Importar páginas
from .pages.dashboard import dashboard_page
from .pages.consolidador import consolidador_page
from .pages.explorador_ftp import explorador_page
from .pages.consulta_datos import consulta_page
from .pages.mapa_contratos import mapa_page
from .pages.configuracion import configuracion_page

# Importar estados
from .state.app_state import AppState
from .state.consolidador_state import ConsolidadorState
from .state.ftp_state import FTPState
from .state.consulta_state import ConsultaState

# Importar constantes
from .constants import COLORS


# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE ESTILOS GLOBALES
# ══════════════════════════════════════════════════════════════════════════════

# Estilos CSS globales
GLOBAL_STYLES = {
    "font_family": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    "background_color": COLORS["bg"],
}


# ══════════════════════════════════════════════════════════════════════════════
# DEFINICIÓN DE LA APLICACIÓN
# ══════════════════════════════════════════════════════════════════════════════

def index() -> rx.Component:
    """Página principal - Redirige al Dashboard."""
    return dashboard_page()


# Crear la aplicación
app = rx.App(
    style=GLOBAL_STYLES,
    stylesheets=[
        # Google Fonts - Inter
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
    ],
)

# ══════════════════════════════════════════════════════════════════════════════
# REGISTRO DE RUTAS
# ══════════════════════════════════════════════════════════════════════════════

# Ruta principal - Dashboard
app.add_page(
    index,
    route="/",
    title="Dashboard | Consolidador T25 - POSITIVA",
    description="Panel principal del sistema de consolidación de tarifas médicas",
)

# Consolidador T25
app.add_page(
    consolidador_page,
    route="/consolidador",
    title="Consolidador T25 | POSITIVA",
    description="Herramienta de consolidación de tarifas médicas",
)

# Explorador FTP
app.add_page(
    explorador_page,
    route="/explorador",
    title="Explorador GoAnywhere | POSITIVA",
    description="Navegador de archivos del servidor SFTP",
)

# Consulta de Datos
app.add_page(
    consulta_page,
    route="/consulta",
    title="Consulta de Datos | POSITIVA",
    description="Búsqueda y consulta de datos consolidados",
)

# Mapa de Contratos
app.add_page(
    mapa_page,
    route="/mapa",
    title="Mapa de Contratos | POSITIVA",
    description="Visualización geográfica de contratos",
)

# Configuración
app.add_page(
    configuracion_page,
    route="/configuracion",
    title="Configuración | POSITIVA",
    description="Configuración del sistema",
)
