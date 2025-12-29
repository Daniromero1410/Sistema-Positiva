"""
Estados globales de la aplicación.
"""
from .app_state import AppState
from .consolidador_state import ConsolidadorState
from .ftp_state import FTPState
from .consulta_state import ConsultaState

__all__ = [
    "AppState",
    "ConsolidadorState",
    "FTPState",
    "ConsultaState",
]
