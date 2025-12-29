"""
Página Explorador FTP GoAnywhere.
"""
import reflex as rx
from ..constants import COLORS
from ..state.ftp_state import FTPState
from ..components.sidebar import sidebar
from ..components.navbar import navbar


def connection_status() -> rx.Component:
    """Indicador de estado de conexión."""
    return rx.hstack(
        rx.cond(
            FTPState.conectado,
            rx.hstack(
                rx.box(
                    width="8px",
                    height="8px",
                    bg=COLORS["success"],
                    border_radius="full",
                ),
                rx.text("Conectado", font_size="13px", color=COLORS["success"]),
                spacing="2",
            ),
            rx.hstack(
                rx.box(
                    width="8px",
                    height="8px",
                    bg=COLORS["danger"],
                    border_radius="full",
                ),
                rx.text("Desconectado", font_size="13px", color=COLORS["danger"]),
                spacing="2",
            ),
        ),
        rx.cond(
            FTPState.conectado,
            rx.button(
                rx.icon("refresh-cw", size=14),
                "Reconectar",
                variant="ghost",
                size="1",
                on_click=FTPState.conectar,
            ),
            rx.button(
                rx.icon("plug", size=14),
                "Conectar",
                variant="soft",
                color_scheme="green",
                size="2",
                on_click=FTPState.conectar,
                loading=FTPState.conectando,
            ),
        ),
        spacing="4",
    )


def breadcrumb_path() -> rx.Component:
    """Barra de navegación de ruta."""
    return rx.hstack(
        rx.icon("folder", size=18, color=COLORS["primary"]),
        rx.text(
            f"Ruta: {FTPState.ruta_actual}",
            font_size="13px",
            color=COLORS["text"],
        ),
        rx.spacer(),
        rx.hstack(
            rx.icon_button(
                rx.icon("arrow-left", size=16),
                variant="ghost",
                size="1",
                on_click=FTPState.navegar_atras,
                disabled=~FTPState.historial_rutas,
            ),
            rx.icon_button(
                rx.icon("arrow-up", size=16),
                variant="ghost",
                size="1",
                on_click=FTPState.navegar_arriba,
            ),
            rx.icon_button(
                rx.icon("copy", size=16),
                variant="ghost",
                size="1",
                on_click=FTPState.copiar_ruta,
            ),
            spacing="1",
        ),
        width="100%",
        padding="12px 16px",
        bg=COLORS["bg"],
        border_radius="8px",
    )


def search_bar_ftp() -> rx.Component:
    """Barra de búsqueda de archivos."""
    return rx.hstack(
        rx.icon("search", size=18, color=COLORS["text_muted"]),
        rx.input(
            placeholder="Buscar archivo...",
            value=FTPState.busqueda,
            on_change=FTPState.set_busqueda,
            variant="soft",
            width="100%",
        ),
        rx.button("Buscar", variant="soft", size="2"),
        spacing="2",
        width="100%",
    )


def folder_tree_item(folder: dict, level: int = 0) -> rx.Component:
    """Item del árbol de carpetas."""
    is_expanded = FTPState.carpeta_expandida.get(folder["nombre"], False)
    has_children = len(folder.get("hijos", [])) > 0

    return rx.vstack(
        rx.hstack(
            rx.cond(
                has_children,
                rx.icon(
                    rx.cond(is_expanded, "chevron-down", "chevron-right"),
                    size=14,
                    color=COLORS["text_muted"],
                    cursor="pointer",
                    on_click=lambda: FTPState.toggle_carpeta(folder["nombre"]),
                ),
                rx.box(width="14px"),
            ),
            rx.icon("folder", size=16, color=COLORS["accent"]),
            rx.text(
                folder["nombre"],
                font_size="13px",
                cursor="pointer",
                _hover={"color": COLORS["primary"]},
            ),
            spacing="2",
            padding_left=f"{level * 16}px",
            padding_y="6px",
            width="100%",
            _hover={"bg": COLORS["bg"]},
            border_radius="4px",
            on_click=lambda: FTPState.navegar_a(f"{FTPState.ruta_actual}/{folder['nombre']}"),
        ),
        rx.cond(
            is_expanded & has_children,
            rx.vstack(
                rx.foreach(
                    folder["hijos"],
                    lambda child: folder_tree_item(child, level + 1),
                ),
                spacing="0",
                width="100%",
            ),
        ),
        spacing="0",
        width="100%",
    )


def folder_tree() -> rx.Component:
    """Árbol de carpetas."""
    return rx.box(
        rx.vstack(
            rx.text("ÁRBOL DE CARPETAS", font_size="11px", font_weight="600", color=COLORS["text_muted"]),
            rx.divider(),
            rx.box(
                rx.vstack(
                    rx.foreach(
                        FTPState.carpetas,
                        lambda f: folder_tree_item(f, 0),
                    ),
                    spacing="0",
                    width="100%",
                ),
                max_height="500px",
                overflow_y="auto",
                width="100%",
            ),
            spacing="3",
            padding="16px",
            width="100%",
        ),
        bg=COLORS["white"],
        border_radius="12px",
        box_shadow="0 1px 3px rgba(0,0,0,0.1)",
        border=f"1px solid {COLORS['bg']}",
        min_width="250px",
    )


def file_item(file: dict) -> rx.Component:
    """Item de archivo en la lista."""
    is_selected = file["nombre"] in FTPState.archivos_seleccionados

    icon_map = {
        "xlsx": "file-spreadsheet",
        "xls": "file-spreadsheet",
        "xlsb": "file-spreadsheet",
        "pdf": "file-text",
        "doc": "file-text",
        "docx": "file-text",
    }
    icon_name = icon_map.get(file.get("tipo", ""), "file")

    return rx.hstack(
        rx.checkbox(
            checked=is_selected,
            on_change=lambda: FTPState.seleccionar_archivo(file["nombre"]),
        ),
        rx.icon(icon_name, size=20, color=COLORS["primary"]),
        rx.vstack(
            rx.text(file["nombre"], font_size="13px", font_weight="500"),
            rx.text(file.get("fecha", ""), font_size="11px", color=COLORS["text_muted"]),
            spacing="0",
            align_items="start",
            flex="1",
        ),
        rx.text(file.get("tamano", ""), font_size="12px", color=COLORS["text_muted"]),
        rx.hstack(
            rx.icon_button(
                rx.icon("eye", size=14),
                variant="ghost",
                size="1",
                on_click=lambda: FTPState.ver_preview(file["nombre"]),
            ),
            rx.icon_button(
                rx.icon("download", size=14),
                variant="ghost",
                size="1",
            ),
            spacing="1",
        ),
        spacing="3",
        padding="12px",
        bg=COLORS["primary_light"] if is_selected else COLORS["white"],
        border_radius="8px",
        border=f"1px solid {COLORS['bg']}",
        _hover={"bg": COLORS["bg"]},
        width="100%",
    )


def file_list_section() -> rx.Component:
    """Lista de archivos."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text("ARCHIVOS", font_size="11px", font_weight="600", color=COLORS["text_muted"]),
                rx.spacer(),
                rx.hstack(
                    rx.text(
                        f"Vista: {FTPState.vista_tipo}",
                        font_size="11px",
                        color=COLORS["text_muted"],
                    ),
                    rx.icon_button(
                        rx.icon("list", size=14),
                        variant="ghost" if FTPState.vista_tipo != "lista" else "soft",
                        size="1",
                        on_click=lambda: FTPState.cambiar_vista("lista"),
                    ),
                    rx.icon_button(
                        rx.icon("grid", size=14),
                        variant="ghost" if FTPState.vista_tipo != "cuadricula" else "soft",
                        size="1",
                        on_click=lambda: FTPState.cambiar_vista("cuadricula"),
                    ),
                    spacing="1",
                ),
                width="100%",
            ),
            rx.divider(),
            # Header de la tabla
            rx.hstack(
                rx.checkbox(
                    on_change=lambda checked: FTPState.seleccionar_todos() if checked else FTPState.deseleccionar_todos(),
                ),
                rx.text(
                    "Nombre",
                    font_size="12px",
                    font_weight="600",
                    color=COLORS["text_muted"],
                    cursor="pointer",
                    on_click=lambda: FTPState.ordenar_archivos("nombre"),
                ),
                rx.spacer(),
                rx.text(
                    "Tamaño",
                    font_size="12px",
                    font_weight="600",
                    color=COLORS["text_muted"],
                    cursor="pointer",
                    on_click=lambda: FTPState.ordenar_archivos("tamano"),
                ),
                rx.text(
                    "Acciones",
                    font_size="12px",
                    font_weight="600",
                    color=COLORS["text_muted"],
                    width="80px",
                ),
                spacing="3",
                padding="8px 12px",
                bg=COLORS["bg"],
                border_radius="6px",
                width="100%",
            ),
            # Lista de archivos
            rx.cond(
                FTPState.cargando,
                rx.center(
                    rx.spinner(size="3"),
                    padding="40px",
                ),
                rx.cond(
                    len(FTPState.archivos) > 0,
                    rx.vstack(
                        rx.foreach(FTPState.archivos, file_item),
                        spacing="2",
                        width="100%",
                    ),
                    rx.center(
                        rx.vstack(
                            rx.icon("folder-open", size=48, color=COLORS["text_muted"]),
                            rx.text("No hay archivos", color=COLORS["text_muted"]),
                            spacing="2",
                        ),
                        padding="60px",
                    ),
                ),
            ),
            # Footer con selección
            rx.cond(
                len(FTPState.archivos_seleccionados) > 0,
                rx.hstack(
                    rx.text(
                        f"Seleccionados: {len(FTPState.archivos_seleccionados)} archivos",
                        font_size="13px",
                        color=COLORS["text_muted"],
                    ),
                    rx.spacer(),
                    rx.button(
                        rx.icon("download", size=14),
                        "Descargar selección",
                        variant="soft",
                        size="2",
                        on_click=FTPState.descargar_seleccionados,
                    ),
                    width="100%",
                    padding="12px",
                    bg=COLORS["bg"],
                    border_radius="8px",
                ),
            ),
            spacing="3",
            padding="16px",
            width="100%",
        ),
        bg=COLORS["white"],
        border_radius="12px",
        box_shadow="0 1px 3px rgba(0,0,0,0.1)",
        border=f"1px solid {COLORS['bg']}",
        flex="1",
    )


def preview_modal() -> rx.Component:
    """Modal de vista previa de archivo."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.hstack(
                    rx.icon("eye", size=20, color=COLORS["primary"]),
                    rx.text(
                        f"Vista Previa: {FTPState.archivo_preview['nombre'] if FTPState.archivo_preview else ''}",
                        font_weight="600",
                    ),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.icon_button(
                            rx.icon("x", size=18),
                            variant="ghost",
                        ),
                    ),
                    width="100%",
                ),
                rx.divider(),
                # Selector de hojas
                rx.hstack(
                    rx.text("Hojas disponibles:", font_size="13px"),
                    rx.select.root(
                        rx.select.trigger(placeholder="Seleccionar hoja"),
                        rx.select.content(
                            rx.foreach(
                                FTPState.preview_hojas,
                                lambda h: rx.select.item(h, value=h),
                            ),
                        ),
                        value=FTPState.preview_hoja_actual,
                        on_change=FTPState.cambiar_hoja_preview,
                    ),
                    spacing="3",
                ),
                # Tabla de preview
                rx.box(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.foreach(
                                    ["CUPS", "Descripción", "Tarifa", "Manual"],
                                    lambda col: rx.table.column_header_cell(col),
                                ),
                            ),
                        ),
                        rx.table.body(
                            rx.foreach(
                                FTPState.preview_data,
                                lambda row: rx.table.row(
                                    rx.table.cell(row.get("CUPS", "")),
                                    rx.table.cell(row.get("Descripción", "")),
                                    rx.table.cell(row.get("Tarifa", "")),
                                    rx.table.cell(row.get("Manual", "")),
                                ),
                            ),
                        ),
                        width="100%",
                    ),
                    max_height="400px",
                    overflow_y="auto",
                    width="100%",
                ),
                rx.text(
                    f"Mostrando 50 de {FTPState.preview_total_filas} filas",
                    font_size="12px",
                    color=COLORS["text_muted"],
                ),
                rx.button(
                    rx.icon("download", size=16),
                    "Descargar archivo completo",
                    width="100%",
                ),
                spacing="4",
                padding="20px",
                width="100%",
            ),
            max_width="800px",
        ),
        open=FTPState.show_preview,
        on_open_change=lambda open: FTPState.cerrar_preview() if not open else None,
    )


def explorador_content() -> rx.Component:
    """Contenido principal del explorador."""
    return rx.box(
        rx.vstack(
            # Header con conexión y búsqueda
            rx.hstack(
                connection_status(),
                rx.spacer(),
                search_bar_ftp(),
                width="100%",
            ),
            # Ruta actual
            breadcrumb_path(),
            # Contenido principal
            rx.hstack(
                folder_tree(),
                file_list_section(),
                spacing="4",
                width="100%",
                align_items="start",
            ),
            # Modal de preview
            preview_modal(),
            spacing="4",
            width="100%",
            padding="24px",
        ),
        width="100%",
        min_height="100vh",
        bg=COLORS["bg"],
    )


def explorador_page() -> rx.Component:
    """Página completa del explorador FTP."""
    return rx.hstack(
        sidebar(),
        rx.box(
            rx.vstack(
                navbar(title="Explorador GoAnywhere"),
                explorador_content(),
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
