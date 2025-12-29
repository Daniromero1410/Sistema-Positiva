"""
Componente AlertToast para notificaciones.
"""
import reflex as rx
from ..constants import COLORS


def alert_toast(
    message: str,
    type: str = "info",
    show: bool = False,
    on_close: callable = None,
    duration: int = 5000,
) -> rx.Component:
    """
    Notificación toast.

    Args:
        message: Mensaje a mostrar
        type: Tipo de alerta (success, error, warning, info)
        show: Si se muestra
        on_close: Callback al cerrar
        duration: Duración en ms
    """
    config = {
        "success": {
            "icon": "check-circle",
            "color": COLORS["success"],
            "bg": "#d4edda",
            "border": "#c3e6cb",
        },
        "error": {
            "icon": "x-circle",
            "color": COLORS["danger"],
            "bg": "#f8d7da",
            "border": "#f5c6cb",
        },
        "warning": {
            "icon": "alert-triangle",
            "color": COLORS["warning"],
            "bg": "#fff3cd",
            "border": "#ffeeba",
        },
        "info": {
            "icon": "info",
            "color": COLORS["info"],
            "bg": "#cce5ff",
            "border": "#b8daff",
        },
    }

    cfg = config.get(type, config["info"])

    return rx.cond(
        show,
        rx.box(
            rx.hstack(
                rx.icon(cfg["icon"], size=20, color=cfg["color"]),
                rx.text(message, font_size="14px", color=COLORS["text"]),
                rx.spacer(),
                rx.icon_button(
                    rx.icon("x", size=16),
                    variant="ghost",
                    size="1",
                    on_click=on_close,
                ),
                spacing="3",
                width="100%",
            ),
            position="fixed",
            bottom="24px",
            right="24px",
            padding="16px 20px",
            bg=cfg["bg"],
            border=f"1px solid {cfg['border']}",
            border_radius="8px",
            box_shadow="0 4px 12px rgba(0,0,0,0.15)",
            z_index="1000",
            min_width="300px",
            max_width="400px",
        ),
    )


def toast_container() -> rx.Component:
    """Contenedor para múltiples toasts usando el sistema de Reflex."""
    return rx.box(
        # El sistema de toasts de Reflex se maneja automáticamente
        id="toast-container",
    )


# Funciones helper para mostrar toasts usando el sistema nativo de Reflex
def show_success_toast(message: str):
    """Muestra un toast de éxito."""
    return rx.toast.success(message)


def show_error_toast(message: str):
    """Muestra un toast de error."""
    return rx.toast.error(message)


def show_warning_toast(message: str):
    """Muestra un toast de advertencia."""
    return rx.toast.warning(message)


def show_info_toast(message: str):
    """Muestra un toast informativo."""
    return rx.toast.info(message)


def confirmation_dialog(
    is_open: bool,
    title: str,
    message: str,
    on_confirm: callable,
    on_cancel: callable,
    confirm_text: str = "Confirmar",
    cancel_text: str = "Cancelar",
    danger: bool = False,
) -> rx.Component:
    """
    Diálogo de confirmación.

    Args:
        is_open: Si el diálogo está abierto
        title: Título del diálogo
        message: Mensaje del diálogo
        on_confirm: Callback al confirmar
        on_cancel: Callback al cancelar
        confirm_text: Texto del botón de confirmar
        cancel_text: Texto del botón de cancelar
        danger: Si es una acción peligrosa
    """
    return rx.alert_dialog.root(
        rx.alert_dialog.content(
            rx.alert_dialog.title(title),
            rx.alert_dialog.description(
                message,
                size="2",
            ),
            rx.hstack(
                rx.alert_dialog.cancel(
                    rx.button(
                        cancel_text,
                        variant="soft",
                        color="gray",
                    ),
                ),
                rx.alert_dialog.action(
                    rx.button(
                        confirm_text,
                        color_scheme="red" if danger else "green",
                        on_click=on_confirm,
                    ),
                ),
                spacing="3",
                justify="end",
                margin_top="16px",
            ),
        ),
        open=is_open,
    )


def info_modal(
    is_open: bool,
    title: str,
    content: rx.Component,
    on_close: callable,
) -> rx.Component:
    """Modal informativo genérico."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(title),
            rx.dialog.description(content),
            rx.dialog.close(
                rx.button(
                    "Cerrar",
                    variant="soft",
                    on_click=on_close,
                ),
            ),
        ),
        open=is_open,
    )
