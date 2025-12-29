"""
Página Dashboard principal.
"""
import reflex as rx
from ..constants import COLORS
from ..state.app_state import AppState
from ..components.sidebar import sidebar
from ..components.navbar import navbar
from ..components.stat_card import stat_card
from ..components.chart_card import chart_card, bar_chart_demo, pie_chart_demo, period_selector
from ..components.data_table import execution_table


def stats_section() -> rx.Component:
    """Sección de tarjetas de estadísticas."""
    return rx.grid(
        stat_card(
            title="Total Contratos",
            value=AppState.total_contratos,
            icon="file-text",
            change="+20%",
            change_type="positive",
        ),
        stat_card(
            title="Contratos Exitosos",
            value=AppState.contratos_exitosos,
            icon="check-circle",
            change="+15%",
            change_type="positive",
            color=COLORS["success"],
        ),
        stat_card(
            title="Alertas Pendientes",
            value=AppState.total_alertas,
            icon="alert-triangle",
            change="-8%",
            change_type="positive",
            color=COLORS["warning"],
        ),
        stat_card(
            title="Espacio GoAnywhere",
            value=f"{AppState.espacio_usado_gb} GB",
            icon="hard-drive",
            color=COLORS["info"],
        ),
        columns="4",
        spacing="4",
        width="100%",
    )


def charts_section() -> rx.Component:
    """Sección de gráficos principales."""
    return rx.grid(
        # Gráfico de barras - Servicios por mes
        chart_card(
            title="Estadísticas de Entregas",
            subtitle="Total de entregas: 70.5K",
            action=period_selector(),
            children=rx.vstack(
                rx.hstack(
                    rx.hstack(
                        rx.box(width="12px", height="12px", bg=COLORS["secondary_light"], border_radius="2px"),
                        rx.text("Envío", font_size="12px", color=COLORS["text_muted"]),
                        spacing="2",
                    ),
                    rx.hstack(
                        rx.box(width="12px", height="12px", bg=COLORS["primary"], border_radius="2px"),
                        rx.text("Entrega", font_size="12px", color=COLORS["text_muted"]),
                        spacing="2",
                    ),
                    spacing="4",
                ),
                bar_chart_demo(),
                width="100%",
            ),
            height="320px",
        ),
        # Panel derecho - Tracking
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text("Seguimiento de Entrega", font_weight="600", font_size="16px"),
                    rx.spacer(),
                    rx.icon_button(
                        rx.icon("more-vertical", size=16),
                        variant="ghost",
                        size="1",
                    ),
                    width="100%",
                ),
                rx.text(
                    "Último historial de entrega visto",
                    font_size="13px",
                    color=COLORS["text_muted"],
                ),
                # Mapa placeholder
                rx.box(
                    rx.center(
                        rx.vstack(
                            rx.icon("map", size=32, color=COLORS["text_muted"]),
                            rx.text("Mapa de seguimiento", font_size="12px", color=COLORS["text_muted"]),
                            spacing="2",
                        ),
                    ),
                    height="150px",
                    bg=COLORS["bg"],
                    border_radius="8px",
                    width="100%",
                ),
                # Tracking info
                rx.hstack(
                    rx.text("ID Seguimiento", font_size="12px", color=COLORS["text_muted"]),
                    rx.spacer(),
                    rx.badge("#28745-72809bjk", color_scheme="blue", variant="soft"),
                    rx.badge("En Tránsito", color_scheme="green", variant="soft"),
                    width="100%",
                ),
                # Timeline
                rx.vstack(
                    rx.hstack(
                        rx.box(
                            rx.icon("check", size=12, color=COLORS["white"]),
                            bg=COLORS["success"],
                            padding="4px",
                            border_radius="full",
                        ),
                        rx.vstack(
                            rx.text("12 Abr 2025", font_size="11px", color=COLORS["text_muted"]),
                            rx.text("Recogido", font_weight="500", font_size="13px"),
                            spacing="0",
                            align_items="start",
                        ),
                        rx.spacer(),
                        rx.text("12:54", font_size="11px", color=COLORS["text_muted"]),
                        width="100%",
                    ),
                    rx.hstack(
                        rx.box(
                            rx.icon("truck", size=12, color=COLORS["white"]),
                            bg=COLORS["primary"],
                            padding="4px",
                            border_radius="full",
                        ),
                        rx.vstack(
                            rx.text("12 Abr 2025", font_size="11px", color=COLORS["text_muted"]),
                            rx.text("En Tránsito", font_weight="500", font_size="13px"),
                            spacing="0",
                            align_items="start",
                        ),
                        rx.spacer(),
                        rx.text("12:58", font_size="11px", color=COLORS["text_muted"]),
                        width="100%",
                    ),
                    spacing="3",
                    width="100%",
                ),
                spacing="3",
                padding="20px",
                width="100%",
            ),
            bg=COLORS["white"],
            border_radius="12px",
            box_shadow="0 1px 3px rgba(0,0,0,0.1)",
            border=f"1px solid {COLORS['bg']}",
        ),
        columns="2",
        spacing="4",
        width="100%",
    )


def bottom_section() -> rx.Component:
    """Sección inferior con métricas y tabla."""
    return rx.grid(
        # Revenue y shipped
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text("Ingresos totales", font_size="13px", color=COLORS["text_muted"]),
                    rx.spacer(),
                    rx.icon_button(
                        rx.icon("more-vertical", size=16),
                        variant="ghost",
                        size="1",
                    ),
                    width="100%",
                ),
                rx.text(
                    "$23,445,700",
                    font_size="28px",
                    font_weight="700",
                    color=COLORS["text"],
                ),
                rx.divider(),
                rx.text("Cantidades enviadas", font_size="13px", color=COLORS["text_muted"]),
                rx.hstack(
                    rx.text("9,258", font_size="24px", font_weight="700"),
                    rx.spacer(),
                    # Mini sparkline placeholder
                    rx.box(
                        height="40px",
                        width="100px",
                        bg=f"linear-gradient(to top, {COLORS['primary']}30, transparent)",
                        border_radius="4px",
                    ),
                    width="100%",
                    align="center",
                ),
                spacing="3",
                padding="20px",
                width="100%",
            ),
            bg=COLORS["white"],
            border_radius="12px",
            box_shadow="0 1px 3px rgba(0,0,0,0.1)",
            border=f"1px solid {COLORS['bg']}",
        ),
        # Vehicles
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text("Vehículos de Entrega", font_weight="600", font_size="16px"),
                    rx.spacer(),
                    rx.icon_button(
                        rx.icon("more-vertical", size=16),
                        variant="ghost",
                        size="1",
                    ),
                    width="100%",
                ),
                rx.text(
                    "Vehículos en ruta",
                    font_size="13px",
                    color=COLORS["text_muted"],
                ),
                rx.hstack(
                    rx.vstack(
                        rx.text("29", font_size="36px", font_weight="700", color=COLORS["primary"]),
                        rx.hstack(
                            rx.badge("+3.85%", color_scheme="green", variant="soft", size="1"),
                            rx.text("que semana pasada", font_size="11px", color=COLORS["text_muted"]),
                            spacing="1",
                        ),
                        rx.hstack(
                            rx.box(width="8px", height="8px", bg=COLORS["success"], border_radius="full"),
                            rx.text("En ruta", font_size="12px", color=COLORS["text_muted"]),
                            spacing="2",
                        ),
                        spacing="2",
                        align_items="start",
                    ),
                    rx.spacer(),
                    # Truck image placeholder
                    rx.box(
                        rx.icon("truck", size=64, color=COLORS["text_muted"]),
                        padding="16px",
                    ),
                    width="100%",
                    align="center",
                ),
                spacing="3",
                padding="20px",
                width="100%",
            ),
            bg=COLORS["white"],
            border_radius="12px",
            box_shadow="0 1px 3px rgba(0,0,0,0.1)",
            border=f"1px solid {COLORS['bg']}",
        ),
        columns="2",
        spacing="4",
        width="100%",
    )


def recent_executions_section() -> rx.Component:
    """Sección de últimas ejecuciones."""
    executions_demo = [
        {"fecha": "28/12/2025 14:32", "estado": "COMPLETADO", "contratos": "150", "servicios": "45,230", "alertas": "12"},
        {"fecha": "27/12/2025 10:15", "estado": "COMPLETADO", "contratos": "148", "servicios": "44,891", "alertas": "8"},
        {"fecha": "26/12/2025 16:45", "estado": "ERROR", "contratos": "145", "servicios": "42,100", "alertas": "25"},
        {"fecha": "25/12/2025 09:30", "estado": "COMPLETADO", "contratos": "152", "servicios": "46,500", "alertas": "5"},
    ]

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text("Últimas Ejecuciones", font_weight="600", font_size="16px"),
                rx.spacer(),
                rx.button(
                    "Ver todas",
                    variant="ghost",
                    size="1",
                ),
                width="100%",
            ),
            execution_table(executions_demo),
            spacing="3",
            padding="20px",
            width="100%",
        ),
        bg=COLORS["white"],
        border_radius="12px",
        box_shadow="0 1px 3px rgba(0,0,0,0.1)",
        border=f"1px solid {COLORS['bg']}",
        width="100%",
    )


def dashboard_content() -> rx.Component:
    """Contenido principal del dashboard."""
    return rx.box(
        rx.vstack(
            stats_section(),
            charts_section(),
            bottom_section(),
            recent_executions_section(),
            spacing="6",
            width="100%",
            padding="24px",
        ),
        width="100%",
        min_height="100vh",
        bg=COLORS["bg"],
    )


def dashboard_page() -> rx.Component:
    """Página completa del dashboard."""
    return rx.hstack(
        sidebar(),
        rx.box(
            rx.vstack(
                navbar(title="Dashboard"),
                dashboard_content(),
                spacing="0",
                width="100%",
            ),
            margin_left="260px",
            width="calc(100% - 260px)",
            min_height="100vh",
        ),
        spacing="0",
        width="100%",
    )
