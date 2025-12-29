"""
Páginas de la aplicación.
"""
from .dashboard import dashboard_page
from .consolidador import consolidador_page
from .explorador_ftp import explorador_page
from .consulta_datos import consulta_page
from .mapa_contratos import mapa_page
from .configuracion import configuracion_page

__all__ = [
    "dashboard_page",
    "consolidador_page",
    "explorador_page",
    "consulta_page",
    "mapa_page",
    "configuracion_page",
]
