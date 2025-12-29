"""
Componente ChartCard para mostrar gráficos.
"""
import reflex as rx
from ..constants import COLORS


def chart_card(
    title: str,
    subtitle: str = None,
    children: rx.Component = None,
    action: rx.Component = None,
    height: str = "300px",
) -> rx.Component:
    """
    Tarjeta contenedora para gráficos.

    Args:
        title: Título del gráfico
        subtitle: Subtítulo opcional
        children: Contenido del gráfico
        action: Componente de acción (dropdown, botón, etc.)
        height: Altura del contenedor
    """
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.vstack(
                    rx.text(
                        title,
                        font_weight="600",
                        font_size="16px",
                        color=COLORS["text"],
                    ),
                    rx.cond(
                        subtitle is not None,
                        rx.text(
                            subtitle,
                            font_size="13px",
                            color=COLORS["text_muted"],
                        ),
                    ),
                    spacing="1",
                    align_items="start",
                ),
                rx.spacer(),
                rx.cond(
                    action is not None,
                    action,
                ),
                width="100%",
                padding="20px 20px 0 20px",
            ),
            # Content
            rx.box(
                children,
                width="100%",
                height=height,
                padding="16px 20px 20px 20px",
            ),
            spacing="0",
            width="100%",
        ),
        bg=COLORS["white"],
        border_radius="12px",
        box_shadow="0 1px 3px rgba(0,0,0,0.1)",
        border=f"1px solid {COLORS['bg']}",
        width="100%",
    )


def period_selector() -> rx.Component:
    """Selector de período para gráficos."""
    return rx.select.root(
        rx.select.trigger(
            placeholder="Monthly",
            variant="soft",
        ),
        rx.select.content(
            rx.select.item("Diario", value="daily"),
            rx.select.item("Semanal", value="weekly"),
            rx.select.item("Mensual", value="monthly"),
            rx.select.item("Anual", value="yearly"),
        ),
        default_value="monthly",
        size="2",
    )


def bar_chart_demo() -> rx.Component:
    """Gráfico de barras de demostración usando Recharts."""
    data = [
        {"month": "Ene", "shipment": 65, "delivery": 80},
        {"month": "Feb", "shipment": 75, "delivery": 70},
        {"month": "Mar", "shipment": 55, "delivery": 60},
        {"month": "Abr", "shipment": 70, "delivery": 75},
        {"month": "May", "shipment": 60, "delivery": 65},
        {"month": "Jun", "shipment": 50, "delivery": 55},
        {"month": "Jul", "shipment": 45, "delivery": 50},
        {"month": "Ago", "shipment": 55, "delivery": 60},
        {"month": "Sep", "shipment": 70, "delivery": 75},
        {"month": "Oct", "shipment": 85, "delivery": 90},
        {"month": "Nov", "shipment": 95, "delivery": 100},
        {"month": "Dic", "shipment": 80, "delivery": 85},
    ]

    return rx.recharts.bar_chart(
        rx.recharts.bar(
            data_key="shipment",
            fill=COLORS["secondary_light"],
            radius=[4, 4, 0, 0],
        ),
        rx.recharts.bar(
            data_key="delivery",
            fill=COLORS["primary"],
            radius=[4, 4, 0, 0],
        ),
        rx.recharts.x_axis(data_key="month"),
        rx.recharts.y_axis(),
        rx.recharts.legend(),
        rx.recharts.graphing_tooltip(),
        data=data,
        width="100%",
        height=250,
    )


def pie_chart_demo() -> rx.Component:
    """Gráfico de dona de demostración."""
    data = [
        {"name": "Bogotá", "value": 135, "fill": COLORS["primary"]},
        {"name": "Antioquia", "value": 61, "fill": COLORS["secondary"]},
        {"name": "Santander", "value": 46, "fill": COLORS["accent"]},
        {"name": "Atlántico", "value": 40, "fill": COLORS["info"]},
        {"name": "Otros", "value": 643, "fill": COLORS["text_muted"]},
    ]

    return rx.recharts.pie_chart(
        rx.recharts.pie(
            data=data,
            data_key="value",
            name_key="name",
            cx="50%",
            cy="50%",
            inner_radius=60,
            outer_radius=80,
            padding_angle=2,
            label=True,
        ),
        rx.recharts.legend(),
        rx.recharts.graphing_tooltip(),
        width="100%",
        height=250,
    )


def line_chart_demo() -> rx.Component:
    """Gráfico de líneas de demostración."""
    data = [
        {"date": "01/12", "alertas": 12},
        {"date": "08/12", "alertas": 8},
        {"date": "15/12", "alertas": 15},
        {"date": "22/12", "alertas": 10},
        {"date": "29/12", "alertas": 5},
    ]

    return rx.recharts.line_chart(
        rx.recharts.line(
            data_key="alertas",
            stroke=COLORS["accent"],
            stroke_width=2,
        ),
        rx.recharts.x_axis(data_key="date"),
        rx.recharts.y_axis(),
        rx.recharts.graphing_tooltip(),
        rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
        data=data,
        width="100%",
        height=200,
    )


def area_chart_demo() -> rx.Component:
    """Gráfico de área de demostración."""
    data = [
        {"month": "Ene", "servicios": 35000},
        {"month": "Feb", "servicios": 38000},
        {"month": "Mar", "servicios": 42000},
        {"month": "Abr", "servicios": 40000},
        {"month": "May", "servicios": 45000},
        {"month": "Jun", "servicios": 48000},
    ]

    return rx.recharts.area_chart(
        rx.recharts.area(
            data_key="servicios",
            fill=COLORS["primary"],
            stroke=COLORS["primary"],
            fill_opacity=0.3,
        ),
        rx.recharts.x_axis(data_key="month"),
        rx.recharts.y_axis(),
        rx.recharts.graphing_tooltip(),
        rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
        data=data,
        width="100%",
        height=200,
    )
