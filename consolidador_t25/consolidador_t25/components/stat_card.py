"""
Componente StatCard para mostrar estadísticas.
"""
import reflex as rx
from ..constants import COLORS


def stat_card(
    title: str,
    value: str | int,
    icon: str,
    change: str = None,
    change_type: str = "positive",  # positive, negative, neutral
    color: str = None,
) -> rx.Component:
    """
    Tarjeta de estadística con icono, valor y cambio porcentual.

    Args:
        title: Título de la estadística
        value: Valor a mostrar
        icon: Nombre del icono de Lucide
        change: Texto de cambio (ej: "+20%")
        change_type: Tipo de cambio (positive, negative, neutral)
        color: Color del icono (opcional)
    """
    icon_color = color or COLORS["primary"]
    icon_bg = COLORS["primary_light"] if not color else f"{color}20"

    change_color = {
        "positive": COLORS["success"],
        "negative": COLORS["danger"],
        "neutral": COLORS["text_muted"],
    }.get(change_type, COLORS["text_muted"])

    return rx.box(
        rx.hstack(
            # Icono
            rx.box(
                rx.icon(
                    icon,
                    size=24,
                    color=icon_color,
                ),
                bg=icon_bg,
                padding="12px",
                border_radius="12px",
            ),
            # Contenido
            rx.vstack(
                rx.text(
                    title,
                    color=COLORS["text_muted"],
                    font_size="13px",
                    font_weight="500",
                ),
                rx.hstack(
                    rx.text(
                        value,
                        color=COLORS["text"],
                        font_size="24px",
                        font_weight="700",
                        line_height="1",
                    ),
                    rx.cond(
                        change is not None,
                        rx.badge(
                            change,
                            color_scheme="green" if change_type == "positive" else (
                                "red" if change_type == "negative" else "gray"
                            ),
                            variant="soft",
                            size="1",
                        ),
                    ),
                    spacing="2",
                    align="center",
                ),
                spacing="1",
                align_items="start",
            ),
            spacing="4",
            width="100%",
        ),
        bg=COLORS["white"],
        padding="20px",
        border_radius="12px",
        box_shadow="0 1px 3px rgba(0,0,0,0.1)",
        border=f"1px solid {COLORS['bg']}",
        _hover={
            "box_shadow": "0 4px 12px rgba(0,0,0,0.1)",
            "transform": "translateY(-2px)",
        },
        transition="all 0.2s ease",
        width="100%",
    )


def stat_card_mini(
    title: str,
    value: str | int,
    icon: str,
    color: str = None,
) -> rx.Component:
    """Versión mini de la tarjeta de estadística."""
    icon_color = color or COLORS["primary"]

    return rx.hstack(
        rx.box(
            rx.icon(icon, size=18, color=icon_color),
            bg=f"{icon_color}20",
            padding="8px",
            border_radius="8px",
        ),
        rx.vstack(
            rx.text(
                value,
                font_weight="700",
                font_size="18px",
                color=COLORS["text"],
                line_height="1",
            ),
            rx.text(
                title,
                font_size="11px",
                color=COLORS["text_muted"],
            ),
            spacing="0",
            align_items="start",
        ),
        spacing="3",
        bg=COLORS["white"],
        padding="12px 16px",
        border_radius="10px",
        border=f"1px solid {COLORS['bg']}",
    )


def stat_card_with_chart(
    title: str,
    value: str | int,
    subtitle: str,
    data: list,
    color: str = None,
) -> rx.Component:
    """Tarjeta de estadística con mini gráfico sparkline."""
    chart_color = color or COLORS["primary"]

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(
                    title,
                    color=COLORS["text_muted"],
                    font_size="13px",
                    font_weight="500",
                ),
                rx.spacer(),
                rx.icon("trending-up", size=16, color=COLORS["success"]),
                width="100%",
            ),
            rx.text(
                value,
                color=COLORS["text"],
                font_size="28px",
                font_weight="700",
                line_height="1",
            ),
            rx.text(
                subtitle,
                color=COLORS["text_muted"],
                font_size="12px",
            ),
            # Mini sparkline chart placeholder
            rx.box(
                height="40px",
                width="100%",
                bg=f"linear-gradient(to top, {chart_color}20, transparent)",
                border_radius="4px",
                margin_top="8px",
            ),
            spacing="2",
            align_items="start",
            width="100%",
        ),
        bg=COLORS["white"],
        padding="20px",
        border_radius="12px",
        box_shadow="0 1px 3px rgba(0,0,0,0.1)",
        border=f"1px solid {COLORS['bg']}",
        width="100%",
    )
