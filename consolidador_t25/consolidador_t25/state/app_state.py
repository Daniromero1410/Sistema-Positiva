"""
Estado global de la aplicación.
"""
import reflex as rx
from typing import Optional, List, Dict
from datetime import datetime


class AppState(rx.State):
    """Estado global de la aplicación."""

    # Sidebar
    sidebar_collapsed: bool = False
    current_page: str = "/"

    # Usuario actual (simulado por ahora)
    current_user: str = "Usuario"
    user_role: str = "admin"

    # Notificaciones
    notifications: List[Dict] = []
    unread_notifications: int = 0

    # Toast messages
    show_toast: bool = False
    toast_message: str = ""
    toast_type: str = "info"  # success, error, warning, info

    # Loading states
    is_loading: bool = False
    loading_message: str = ""

    # Modal states
    show_modal: bool = False
    modal_title: str = ""
    modal_content: str = ""

    # Theme
    dark_mode: bool = False

    # Estadísticas del dashboard (cargadas de BD)
    total_contratos: int = 0
    contratos_exitosos: int = 0
    total_alertas: int = 0
    total_servicios: int = 0
    espacio_usado_gb: float = 0.0
    ultima_ejecucion: Optional[str] = None

    def toggle_sidebar(self):
        """Alterna el estado del sidebar."""
        self.sidebar_collapsed = not self.sidebar_collapsed

    def set_page(self, page: str):
        """Establece la página actual."""
        self.current_page = page

    def show_notification(self, message: str, type: str = "info"):
        """Muestra una notificación toast."""
        self.toast_message = message
        self.toast_type = type
        self.show_toast = True

    def hide_toast(self):
        """Oculta el toast."""
        self.show_toast = False

    def add_notification(self, title: str, message: str, type: str = "info"):
        """Agrega una notificación a la lista."""
        self.notifications.append({
            "id": len(self.notifications) + 1,
            "title": title,
            "message": message,
            "type": type,
            "timestamp": datetime.now().isoformat(),
            "read": False
        })
        self.unread_notifications += 1

    def mark_notification_read(self, notification_id: int):
        """Marca una notificación como leída."""
        for notif in self.notifications:
            if notif["id"] == notification_id and not notif["read"]:
                notif["read"] = True
                self.unread_notifications = max(0, self.unread_notifications - 1)
                break

    def clear_notifications(self):
        """Limpia todas las notificaciones."""
        self.notifications = []
        self.unread_notifications = 0

    def set_loading(self, loading: bool, message: str = ""):
        """Establece el estado de carga."""
        self.is_loading = loading
        self.loading_message = message

    def open_modal(self, title: str, content: str):
        """Abre un modal."""
        self.modal_title = title
        self.modal_content = content
        self.show_modal = True

    def close_modal(self):
        """Cierra el modal."""
        self.show_modal = False

    def toggle_dark_mode(self):
        """Alterna el modo oscuro."""
        self.dark_mode = not self.dark_mode

    async def load_dashboard_stats(self):
        """Carga las estadísticas del dashboard desde la BD."""
        # TODO: Implementar consulta a la BD
        # Por ahora, datos de ejemplo
        self.total_contratos = 925
        self.contratos_exitosos = 892
        self.total_alertas = 45
        self.total_servicios = 45230
        self.espacio_usado_gb = 2.3
        self.ultima_ejecucion = datetime.now().strftime("%d/%m/%Y %H:%M")
