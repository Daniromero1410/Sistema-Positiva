"""
Componente Sidebar de navegación.
"""
import reflex as rx
from ..constants import COLORS, MENU_ITEMS


def menu_item(item: dict, current_page: str) -> rx.Component:
    """Renderiza un item del menú."""
    is_active = current_page == item["path"]

    return rx.link(
        rx.hstack(
            rx.icon(
                item["icon"],
                size=20,
                color=COLORS["primary"] if is_active else COLORS["sidebar_text"],
            ),
            rx.text(
                item["name"],
                color=COLORS["primary"] if is_active else COLORS["sidebar_text"],
                font_weight="600" if is_active else "400",
                font_size="14px",
            ),
            spacing="3",
            padding="12px 16px",
            border_radius="8px",
            bg=COLORS["primary_light"] if is_active else "transparent",
            _hover={
                "bg": COLORS["primary_light"] if not is_active else None,
            },
            width="100%",
            cursor="pointer",
            transition="all 0.2s ease",
        ),
        href=item["path"],
        width="100%",
        text_decoration="none",
    )


def sidebar() -> rx.Component:
    """Componente sidebar de navegación."""
    return rx.box(
        rx.vstack(
            # Logo y título
            rx.hstack(
                rx.image(
                    src="/logo_positiva.svg",
                    height="40px",
                    fallback=rx.box(
                        rx.text(
                            "P",
                            color=COLORS["white"],
                            font_weight="bold",
                            font_size="20px",
                        ),
                        bg=COLORS["primary"],
                        width="40px",
                        height="40px",
                        border_radius="8px",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                    ),
                ),
                rx.vstack(
                    rx.text(
                        "POSITIVA",
                        color=COLORS["white"],
                        font_weight="bold",
                        font_size="16px",
                        line_height="1",
                    ),
                    rx.text(
                        "Consolidador T25",
                        color=COLORS["primary"],
                        font_size="11px",
                        line_height="1",
                    ),
                    spacing="1",
                    align_items="start",
                ),
                spacing="3",
                padding="20px 16px",
                width="100%",
                border_bottom=f"1px solid {COLORS['secondary_medium']}",
            ),
            # Menú
            rx.vstack(
                rx.text(
                    "MENÚ",
                    color=COLORS["text_muted"],
                    font_size="11px",
                    font_weight="600",
                    letter_spacing="0.5px",
                    padding="16px 16px 8px 16px",
                ),
                rx.foreach(
                    MENU_ITEMS,
                    lambda item: menu_item(item, rx.State.router.page.path),
                ),
                width="100%",
                spacing="1",
                padding="0 8px",
            ),
            # Spacer
            rx.spacer(),
            # Footer del sidebar
            rx.box(
                rx.vstack(
                    rx.divider(color=COLORS["secondary_medium"]),
                    rx.hstack(
                        rx.icon("help-circle", size=16, color=COLORS["text_muted"]),
                        rx.text(
                            "Soporte",
                            color=COLORS["text_muted"],
                            font_size="12px",
                        ),
                        spacing="2",
                        padding="12px 16px",
                        cursor="pointer",
                        _hover={"color": COLORS["white"]},
                    ),
                    rx.text(
                        "v1.0.0",
                        color=COLORS["text_muted"],
                        font_size="10px",
                        padding="0 16px 16px 16px",
                    ),
                    width="100%",
                    spacing="0",
                ),
                width="100%",
            ),
            height="100vh",
            width="260px",
            bg=COLORS["sidebar_bg"],
            spacing="0",
            position="fixed",
            left="0",
            top="0",
            z_index="100",
            box_shadow="2px 0 10px rgba(0,0,0,0.1)",
        ),
    )


def sidebar_collapsed() -> rx.Component:
    """Versión colapsada del sidebar para móvil."""
    return rx.drawer.root(
        rx.drawer.trigger(
            rx.icon_button(
                rx.icon("menu", size=24),
                variant="ghost",
            ),
        ),
        rx.drawer.overlay(z_index="99"),
        rx.drawer.portal(
            rx.drawer.content(
                sidebar(),
                width="260px",
                height="100vh",
                bg=COLORS["sidebar_bg"],
            ),
        ),
        direction="left",
    )
