"""
Componente ProgressModal para mostrar progreso de operaciones.
"""
import reflex as rx
from typing import List, Dict, Callable
from ..constants import COLORS


def progress_modal(
    is_open: bool,
    title: str = "Procesando",
    progress: float = 0,
    current_item: str = "",
    current_detail: str = "",
    stats: Dict = None,
    log_messages: List[Dict] = None,
    on_pause: Callable = None,
    on_cancel: Callable = None,
    is_paused: bool = False,
    on_resume: Callable = None,
) -> rx.Component:
    """
    Modal de progreso con barra, estadísticas y log.

    Args:
        is_open: Si el modal está abierto
        title: Título del modal
        progress: Porcentaje de progreso (0-100)
        current_item: Item actual siendo procesado
        current_detail: Detalle del item actual
        stats: Diccionario con estadísticas
        log_messages: Lista de mensajes de log
        on_pause: Callback para pausar
        on_cancel: Callback para cancelar
        is_paused: Si está pausado
        on_resume: Callback para reanudar
    """
    stats = stats or {}
    log_messages = log_messages or []

    def log_item(msg: Dict) -> rx.Component:
        """Renderiza un item del log."""
        icon_map = {
            "SUCCESS": ("check-circle", COLORS["success"]),
            "WARNING": ("alert-triangle", COLORS["warning"]),
            "ERROR": ("x-circle", COLORS["danger"]),
            "INFO": ("info", COLORS["info"]),
        }
        icon_name, icon_color = icon_map.get(msg.get("tipo", "INFO"), ("info", COLORS["info"]))

        return rx.hstack(
            rx.text(
                f"[{msg.get('timestamp', '')}]",
                font_size="11px",
                color=COLORS["text_muted"],
                font_family="monospace",
            ),
            rx.icon(icon_name, size=14, color=icon_color),
            rx.text(
                msg.get("mensaje", ""),
                font_size="12px",
                color=COLORS["text"],
            ),
            spacing="2",
            width="100%",
        )

    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                # Header
                rx.hstack(
                    rx.icon("loader", size=24, color=COLORS["primary"]),
                    rx.text(
                        title,
                        font_weight="600",
                        font_size="18px",
                    ),
                    spacing="3",
                ),
                # Barra de progreso
                rx.box(
                    rx.progress(
                        value=progress,
                        max=100,
                        color_scheme="green",
                        height="8px",
                        width="100%",
                    ),
                    rx.text(
                        f"{progress:.0f}%",
                        font_size="12px",
                        color=COLORS["text_muted"],
                        text_align="right",
                        margin_top="4px",
                    ),
                    width="100%",
                ),
                # Item actual
                rx.box(
                    rx.hstack(
                        rx.icon("file-text", size=16, color=COLORS["primary"]),
                        rx.text(
                            "Contrato actual:",
                            font_size="13px",
                            color=COLORS["text_muted"],
                        ),
                        rx.text(
                            current_item,
                            font_weight="500",
                            font_size="13px",
                        ),
                        spacing="2",
                    ),
                    rx.text(
                        current_detail,
                        font_size="12px",
                        color=COLORS["text_muted"],
                        margin_left="24px",
                    ),
                    width="100%",
                    padding="12px",
                    bg=COLORS["bg"],
                    border_radius="8px",
                ),
                # Estadísticas
                rx.divider(),
                rx.hstack(
                    rx.vstack(
                        rx.text(
                            stats.get("procesados", "0"),
                            font_weight="700",
                            font_size="20px",
                            color=COLORS["success"],
                        ),
                        rx.text(
                            f"de {stats.get('total', '0')}",
                            font_size="11px",
                            color=COLORS["text_muted"],
                        ),
                        rx.text(
                            "Contratos",
                            font_size="12px",
                            color=COLORS["text_muted"],
                        ),
                        spacing="0",
                        align="center",
                    ),
                    rx.vstack(
                        rx.text(
                            stats.get("servicios", "0"),
                            font_weight="700",
                            font_size="20px",
                            color=COLORS["primary"],
                        ),
                        rx.text(
                            "Servicios",
                            font_size="12px",
                            color=COLORS["text_muted"],
                        ),
                        spacing="0",
                        align="center",
                    ),
                    rx.vstack(
                        rx.text(
                            stats.get("alertas", "0"),
                            font_weight="700",
                            font_size="20px",
                            color=COLORS["warning"],
                        ),
                        rx.text(
                            "Alertas",
                            font_size="12px",
                            color=COLORS["text_muted"],
                        ),
                        spacing="0",
                        align="center",
                    ),
                    rx.vstack(
                        rx.text(
                            stats.get("tiempo", "00:00"),
                            font_weight="700",
                            font_size="20px",
                            color=COLORS["info"],
                        ),
                        rx.text(
                            "Tiempo",
                            font_size="12px",
                            color=COLORS["text_muted"],
                        ),
                        spacing="0",
                        align="center",
                    ),
                    justify="around",
                    width="100%",
                ),
                # Log
                rx.box(
                    rx.text(
                        "Log en tiempo real:",
                        font_size="12px",
                        font_weight="500",
                        color=COLORS["text_muted"],
                        margin_bottom="8px",
                    ),
                    rx.box(
                        rx.vstack(
                            rx.foreach(
                                log_messages[-10:],  # Últimos 10 mensajes
                                log_item,
                            ),
                            spacing="2",
                            width="100%",
                            align_items="start",
                        ),
                        max_height="150px",
                        overflow_y="auto",
                        padding="12px",
                        bg=COLORS["bg"],
                        border_radius="8px",
                        font_family="monospace",
                    ),
                    width="100%",
                ),
                # Botones
                rx.hstack(
                    rx.cond(
                        is_paused,
                        rx.button(
                            rx.icon("play", size=16),
                            "Reanudar",
                            variant="soft",
                            color_scheme="green",
                            on_click=on_resume,
                        ),
                        rx.button(
                            rx.icon("pause", size=16),
                            "Pausar",
                            variant="soft",
                            on_click=on_pause,
                        ),
                    ),
                    rx.button(
                        rx.icon("x", size=16),
                        "Cancelar",
                        variant="soft",
                        color_scheme="red",
                        on_click=on_cancel,
                    ),
                    spacing="3",
                    justify="center",
                    width="100%",
                ),
                spacing="4",
                padding="24px",
                width="100%",
            ),
            max_width="500px",
        ),
        open=is_open,
    )


def simple_progress_modal(
    is_open: bool,
    title: str,
    message: str,
    progress: float = None,
) -> rx.Component:
    """Modal de progreso simple."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.spinner(size="3"),
                rx.text(title, font_weight="600", font_size="16px"),
                rx.text(message, font_size="14px", color=COLORS["text_muted"]),
                rx.cond(
                    progress is not None,
                    rx.progress(
                        value=progress,
                        max=100,
                        width="100%",
                        height="6px",
                    ),
                ),
                spacing="3",
                align="center",
                padding="24px",
            ),
            max_width="300px",
        ),
        open=is_open,
    )
