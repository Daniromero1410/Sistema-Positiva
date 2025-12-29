"""
Página Consulta de Datos.
"""
import reflex as rx
from ..constants import COLORS
from ..state.consulta_state import ConsultaState
from ..components.sidebar import sidebar
from ..components.navbar import navbar


def search_section() -> rx.Component:
    """Sección de búsqueda con autocompletado."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("search", size=20, color=COLORS["text_muted"]),
                rx.input(
                    placeholder="Buscar por CUPS, contrato, proveedor, NIT...",
                    value=ConsultaState.busqueda,
                    on_change=ConsultaState.set_busqueda,
                    on_blur=ConsultaState.ocultar_sugerencias,
                    width="100%",
                    size="3",
                ),
                rx.button(
                    "Buscar",
                    color_scheme="green",
                    size="3",
                    on_click=ConsultaState.buscar,
                    loading=ConsultaState.buscando,
                ),
                spacing="3",
                width="100%",
            ),
            # Sugerencias
            rx.cond(
                ConsultaState.show_sugerencias & (len(ConsultaState.sugerencias) > 0),
                rx.box(
                    rx.vstack(
                        rx.foreach(
                            ConsultaState.sugerencias,
                            lambda s: rx.box(
                                rx.text(s, font_size="13px"),
                                padding="8px 12px",
                                _hover={"bg": COLORS["bg"]},
                                cursor="pointer",
                                width="100%",
                                on_click=lambda: ConsultaState.seleccionar_sugerencia(s),
                            ),
                        ),
                        spacing="0",
                        width="100%",
                    ),
                    position="absolute",
                    top="100%",
                    left="0",
                    right="0",
                    bg=COLORS["white"],
                    border=f"1px solid {COLORS['bg']}",
                    border_radius="8px",
                    box_shadow="0 4px 12px rgba(0,0,0,0.1)",
                    z_index="10",
                ),
            ),
            spacing="2",
            width="100%",
            position="relative",
        ),
        bg=COLORS["white"],
        padding="20px",
        border_radius="12px",
        box_shadow="0 1px 3px rgba(0,0,0,0.1)",
        width="100%",
    )


def filters_section() -> rx.Component:
    """Sección de filtros avanzados."""
    return rx.box(
        rx.hstack(
            rx.text("Filtros:", font_weight="500", font_size="14px"),
            rx.select.root(
                rx.select.trigger(placeholder="Departamento"),
                rx.select.content(
                    rx.foreach(
                        ConsultaState.departamentos_disponibles,
                        lambda d: rx.select.item(d, value=d),
                    ),
                ),
                value=ConsultaState.filtro_departamento,
                on_change=ConsultaState.set_filtro_departamento,
                size="2",
            ),
            rx.select.root(
                rx.select.trigger(placeholder="Año"),
                rx.select.content(
                    rx.foreach(
                        ConsultaState.anos_disponibles,
                        lambda a: rx.select.item(a, value=a),
                    ),
                ),
                value=ConsultaState.filtro_ano,
                on_change=ConsultaState.set_filtro_ano,
                size="2",
            ),
            rx.select.root(
                rx.select.trigger(placeholder="Manual"),
                rx.select.content(
                    rx.foreach(
                        ConsultaState.manuales_disponibles,
                        lambda m: rx.select.item(m, value=m),
                    ),
                ),
                value=ConsultaState.filtro_manual,
                on_change=ConsultaState.set_filtro_manual,
                size="2",
            ),
            rx.button(
                rx.icon("x", size=14),
                "Limpiar",
                variant="ghost",
                size="2",
                on_click=ConsultaState.limpiar_filtros,
            ),
            spacing="3",
            width="100%",
            flex_wrap="wrap",
        ),
        bg=COLORS["white"],
        padding="16px 20px",
        border_radius="12px",
        box_shadow="0 1px 3px rgba(0,0,0,0.1)",
        width="100%",
    )


def result_row(resultado: dict) -> rx.Component:
    """Fila de resultado."""
    return rx.table.row(
        rx.table.cell(
            rx.text(resultado["contrato"], font_weight="500", font_size="13px"),
        ),
        rx.table.cell(
            rx.vstack(
                rx.text(resultado["proveedor"], font_size="13px"),
                rx.text(resultado["nit"], font_size="11px", color=COLORS["text_muted"]),
                spacing="0",
                align_items="start",
            ),
        ),
        rx.table.cell(
            rx.badge(resultado["cups"], color_scheme="blue", variant="soft"),
        ),
        rx.table.cell(
            rx.text(f"${resultado['tarifa']:,}", font_size="13px"),
        ),
        rx.table.cell(
            rx.badge(
                resultado["manual"],
                color_scheme="green" if resultado["manual"] == "SOAT" else "purple",
                variant="soft",
            ),
        ),
        rx.table.cell(
            rx.icon_button(
                rx.icon("eye", size=14),
                variant="ghost",
                size="1",
                on_click=lambda: ConsultaState.ver_detalle(resultado["id"]),
            ),
        ),
        _hover={"bg": COLORS["bg"]},
        cursor="pointer",
    )


def results_table() -> rx.Component:
    """Tabla de resultados."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(
                    f"Resultados: {ConsultaState.total_resultados} registros encontrados",
                    font_weight="500",
                    font_size="14px",
                ),
                rx.spacer(),
                rx.button(
                    rx.icon("download", size=14),
                    "Exportar Excel",
                    variant="soft",
                    size="2",
                    on_click=ConsultaState.exportar_excel,
                    loading=ConsultaState.exportando,
                ),
                width="100%",
            ),
            rx.cond(
                ConsultaState.buscando,
                rx.center(
                    rx.spinner(size="3"),
                    padding="60px",
                ),
                rx.cond(
                    len(ConsultaState.resultados) > 0,
                    rx.vstack(
                        rx.table.root(
                            rx.table.header(
                                rx.table.row(
                                    rx.table.column_header_cell("Contrato"),
                                    rx.table.column_header_cell("Proveedor"),
                                    rx.table.column_header_cell("CUPS"),
                                    rx.table.column_header_cell("Tarifa"),
                                    rx.table.column_header_cell("Manual"),
                                    rx.table.column_header_cell("", width="50px"),
                                    bg=COLORS["bg"],
                                ),
                            ),
                            rx.table.body(
                                rx.foreach(ConsultaState.resultados, result_row),
                            ),
                            width="100%",
                        ),
                        # Paginación
                        rx.hstack(
                            rx.icon_button(
                                rx.icon("chevron-left", size=16),
                                variant="ghost",
                                on_click=ConsultaState.pagina_anterior,
                                disabled=ConsultaState.pagina_actual <= 1,
                            ),
                            rx.text(
                                f"Página {ConsultaState.pagina_actual} de {ConsultaState.total_paginas}",
                                font_size="13px",
                            ),
                            rx.icon_button(
                                rx.icon("chevron-right", size=16),
                                variant="ghost",
                                on_click=ConsultaState.pagina_siguiente,
                                disabled=ConsultaState.pagina_actual >= ConsultaState.total_paginas,
                            ),
                            spacing="2",
                            justify="center",
                            width="100%",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    rx.center(
                        rx.vstack(
                            rx.icon("search", size=48, color=COLORS["text_muted"]),
                            rx.text(
                                "Realiza una búsqueda para ver resultados",
                                color=COLORS["text_muted"],
                            ),
                            spacing="3",
                        ),
                        padding="60px",
                    ),
                ),
            ),
            spacing="4",
            padding="20px",
            width="100%",
        ),
        bg=COLORS["white"],
        border_radius="12px",
        box_shadow="0 1px 3px rgba(0,0,0,0.1)",
        width="100%",
    )


def detail_modal() -> rx.Component:
    """Modal de detalle del registro."""
    r = ConsultaState.registro_detalle

    return rx.dialog.root(
        rx.dialog.content(
            rx.cond(
                r is not None,
                rx.vstack(
                    rx.hstack(
                        rx.icon("file-text", size=24, color=COLORS["primary"]),
                        rx.text("Detalle del Servicio", font_weight="600", font_size="18px"),
                        rx.spacer(),
                        rx.dialog.close(
                            rx.icon_button(rx.icon("x", size=18), variant="ghost"),
                        ),
                        width="100%",
                    ),
                    rx.divider(),
                    # Información del contrato
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "INFORMACIÓN DEL CONTRATO",
                                font_size="11px",
                                font_weight="600",
                                color=COLORS["text_muted"],
                            ),
                            rx.grid(
                                rx.vstack(
                                    rx.text("Número:", font_size="12px", color=COLORS["text_muted"]),
                                    rx.text(r["contrato"] if r else "", font_weight="500"),
                                    spacing="0",
                                    align_items="start",
                                ),
                                rx.vstack(
                                    rx.text("Proveedor:", font_size="12px", color=COLORS["text_muted"]),
                                    rx.text(r["proveedor"] if r else "", font_weight="500"),
                                    spacing="0",
                                    align_items="start",
                                ),
                                rx.vstack(
                                    rx.text("NIT:", font_size="12px", color=COLORS["text_muted"]),
                                    rx.text(r["nit"] if r else "", font_weight="500"),
                                    spacing="0",
                                    align_items="start",
                                ),
                                rx.vstack(
                                    rx.text("Departamento:", font_size="12px", color=COLORS["text_muted"]),
                                    rx.text(r["departamento"] if r else "", font_weight="500"),
                                    spacing="0",
                                    align_items="start",
                                ),
                                columns="2",
                                spacing="4",
                                width="100%",
                            ),
                            spacing="3",
                            width="100%",
                        ),
                        bg=COLORS["bg"],
                        padding="16px",
                        border_radius="8px",
                        width="100%",
                    ),
                    # Información del servicio
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "INFORMACIÓN DEL SERVICIO",
                                font_size="11px",
                                font_weight="600",
                                color=COLORS["text_muted"],
                            ),
                            rx.grid(
                                rx.vstack(
                                    rx.text("Código CUPS:", font_size="12px", color=COLORS["text_muted"]),
                                    rx.badge(r["cups"] if r else "", color_scheme="blue"),
                                    spacing="1",
                                    align_items="start",
                                ),
                                rx.vstack(
                                    rx.text("Tarifa:", font_size="12px", color=COLORS["text_muted"]),
                                    rx.text(
                                        f"${r['tarifa']:,}" if r else "",
                                        font_weight="700",
                                        font_size="18px",
                                        color=COLORS["primary"],
                                    ),
                                    spacing="1",
                                    align_items="start",
                                ),
                                rx.vstack(
                                    rx.text("Manual:", font_size="12px", color=COLORS["text_muted"]),
                                    rx.badge(r["manual"] if r else "", color_scheme="green"),
                                    spacing="1",
                                    align_items="start",
                                ),
                                rx.vstack(
                                    rx.text("Porcentaje:", font_size="12px", color=COLORS["text_muted"]),
                                    rx.text(f"+{r['porcentaje']}%" if r else "", font_weight="500"),
                                    spacing="1",
                                    align_items="start",
                                ),
                                columns="2",
                                spacing="4",
                                width="100%",
                            ),
                            rx.text("Descripción:", font_size="12px", color=COLORS["text_muted"]),
                            rx.text(r["descripcion"] if r else "", font_size="13px"),
                            spacing="3",
                            width="100%",
                        ),
                        bg=COLORS["bg"],
                        padding="16px",
                        border_radius="8px",
                        width="100%",
                    ),
                    # Acciones
                    rx.hstack(
                        rx.button(
                            rx.icon("map-pin", size=14),
                            "Ver en mapa",
                            variant="outline",
                            size="2",
                        ),
                        rx.button(
                            rx.icon("folder", size=14),
                            "Ver archivos",
                            variant="outline",
                            size="2",
                        ),
                        rx.button(
                            rx.icon("bar-chart", size=14),
                            "Comparar tarifas",
                            variant="outline",
                            size="2",
                        ),
                        spacing="2",
                        width="100%",
                        justify="center",
                    ),
                    spacing="4",
                    padding="20px",
                    width="100%",
                ),
            ),
            max_width="600px",
        ),
        open=ConsultaState.show_detalle,
        on_open_change=lambda open: ConsultaState.cerrar_detalle() if not open else None,
    )


def consulta_content() -> rx.Component:
    """Contenido principal de consulta."""
    return rx.box(
        rx.vstack(
            search_section(),
            filters_section(),
            results_table(),
            detail_modal(),
            spacing="4",
            width="100%",
            padding="24px",
        ),
        width="100%",
        min_height="100vh",
        bg=COLORS["bg"],
    )


def consulta_page() -> rx.Component:
    """Página completa de consulta de datos."""
    return rx.hstack(
        sidebar(),
        rx.box(
            rx.vstack(
                navbar(title="Consulta de Datos"),
                consulta_content(),
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
