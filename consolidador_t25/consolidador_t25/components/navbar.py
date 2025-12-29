"""
Componente Navbar superior.
"""
import reflex as rx
from ..constants import COLORS
from ..state.app_state import AppState


def notification_dropdown() -> rx.Component:
    """Dropdown de notificaciones."""
    return rx.popover.root(
        rx.popover.trigger(
            rx.box(
                rx.icon_button(
                    rx.icon("bell", size=20),
                    variant="ghost",
                    color=COLORS["text_muted"],
                    cursor="pointer",
                ),
                rx.cond(
                    AppState.unread_notifications > 0,
                    rx.badge(
                        AppState.unread_notifications,
                        color_scheme="red",
                        variant="solid",
                        size="1",
                        position="absolute",
                        top="-2px",
                        right="-2px",
                    ),
                ),
                position="relative",
            ),
        ),
        rx.popover.content(
            rx.vstack(
                rx.hstack(
                    rx.text("Notificaciones", font_weight="600"),
                    rx.spacer(),
                    rx.button(
                        "Limpiar",
                        size="1",
                        variant="ghost",
                        on_click=AppState.clear_notifications,
                    ),
                    width="100%",
                ),
                rx.divider(),
                rx.cond(
                    AppState.notifications.length() > 0,
                    rx.foreach(
                        AppState.notifications,
                        lambda n: rx.box(
                            rx.vstack(
                                rx.text(n["title"], font_weight="500", font_size="13px"),
                                rx.text(n["message"], color=COLORS["text_muted"], font_size="12px"),
                                spacing="1",
                                align_items="start",
                            ),
                            padding="8px",
                            border_radius="6px",
                            _hover={"bg": COLORS["bg"]},
                            cursor="pointer",
                            width="100%",
                        ),
                    ),
                    rx.text(
                        "No hay notificaciones",
                        color=COLORS["text_muted"],
                        font_size="13px",
                        padding="16px",
                    ),
                ),
                width="300px",
                max_height="400px",
                overflow_y="auto",
                spacing="2",
            ),
            side="bottom",
            align="end",
        ),
    )


def user_dropdown() -> rx.Component:
    """Dropdown del usuario."""
    return rx.popover.root(
        rx.popover.trigger(
            rx.hstack(
                rx.avatar(
                    fallback="U",
                    size="2",
                    radius="full",
                    color=COLORS["white"],
                    bg=COLORS["primary"],
                ),
                rx.vstack(
                    rx.text(
                        AppState.current_user,
                        font_weight="500",
                        font_size="14px",
                        color=COLORS["text"],
                    ),
                    rx.text(
                        AppState.user_role,
                        font_size="11px",
                        color=COLORS["text_muted"],
                    ),
                    spacing="0",
                    align_items="start",
                ),
                rx.icon("chevron-down", size=16, color=COLORS["text_muted"]),
                spacing="2",
                cursor="pointer",
                padding="8px",
                border_radius="8px",
                _hover={"bg": COLORS["bg"]},
            ),
        ),
        rx.popover.content(
            rx.vstack(
                rx.hstack(
                    rx.icon("user", size=16),
                    rx.text("Mi Perfil", font_size="13px"),
                    spacing="2",
                    padding="8px 12px",
                    border_radius="6px",
                    _hover={"bg": COLORS["bg"]},
                    cursor="pointer",
                    width="100%",
                ),
                rx.hstack(
                    rx.icon("settings", size=16),
                    rx.text("Configuración", font_size="13px"),
                    spacing="2",
                    padding="8px 12px",
                    border_radius="6px",
                    _hover={"bg": COLORS["bg"]},
                    cursor="pointer",
                    width="100%",
                ),
                rx.divider(),
                rx.hstack(
                    rx.icon("log-out", size=16, color=COLORS["danger"]),
                    rx.text("Cerrar Sesión", font_size="13px", color=COLORS["danger"]),
                    spacing="2",
                    padding="8px 12px",
                    border_radius="6px",
                    _hover={"bg": COLORS["bg"]},
                    cursor="pointer",
                    width="100%",
                ),
                width="180px",
                spacing="1",
            ),
            side="bottom",
            align="end",
        ),
    )


def search_bar() -> rx.Component:
    """Barra de búsqueda global."""
    return rx.hstack(
        rx.icon("search", size=18, color=COLORS["text_muted"]),
        rx.input(
            placeholder="Buscar o escribir comando...",
            variant="soft",
            size="2",
            width="300px",
            bg=COLORS["bg"],
            border="none",
        ),
        rx.kbd("⌘K", size="1"),
        bg=COLORS["bg"],
        padding="8px 16px",
        border_radius="8px",
        spacing="2",
        cursor="text",
    )


def navbar(title: str = "Dashboard") -> rx.Component:
    """Componente navbar superior."""
    return rx.box(
        rx.hstack(
            # Título de la página
            rx.hstack(
                rx.heading(
                    title,
                    size="5",
                    color=COLORS["text"],
                    font_weight="600",
                ),
                spacing="3",
            ),
            # Spacer
            rx.spacer(),
            # Barra de búsqueda
            search_bar(),
            # Spacer
            rx.spacer(),
            # Acciones
            rx.hstack(
                # Botón de tema
                rx.icon_button(
                    rx.cond(
                        AppState.dark_mode,
                        rx.icon("sun", size=20),
                        rx.icon("moon", size=20),
                    ),
                    variant="ghost",
                    color=COLORS["text_muted"],
                    on_click=AppState.toggle_dark_mode,
                ),
                # Notificaciones
                notification_dropdown(),
                # Usuario
                user_dropdown(),
                spacing="2",
            ),
            width="100%",
            padding="16px 24px",
            bg=COLORS["white"],
            border_bottom=f"1px solid {COLORS['bg']}",
            align="center",
        ),
        width="100%",
        position="sticky",
        top="0",
        z_index="50",
    )
