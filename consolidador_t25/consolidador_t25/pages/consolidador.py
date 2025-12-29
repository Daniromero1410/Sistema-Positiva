"""
Página Consolidador T25.
"""
import reflex as rx
from ..constants import COLORS
from ..state.consolidador_state import ConsolidadorState
from ..components.sidebar import sidebar
from ..components.navbar import navbar
from ..components.upload_zone import upload_zone, file_list
from ..components.progress_modal import progress_modal
from ..components.stat_card import stat_card_mini


def paso_1_maestra() -> rx.Component:
    """Paso 1: Carga de Maestra de Contratos."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.badge("PASO 1", color_scheme="green", variant="soft"),
                rx.text("Cargar Maestra de Contratos", font_weight="600", font_size="16px"),
                spacing="3",
            ),
            rx.divider(),
            # Zona de upload
            rx.cond(
                ConsolidadorState.maestra_cargada,
                # Archivo cargado
                rx.vstack(
                    rx.hstack(
                        rx.hstack(
                            rx.icon("file-spreadsheet", size=32, color=COLORS["primary"]),
                            rx.vstack(
                                rx.text(
                                    ConsolidadorState.maestra_nombre,
                                    font_weight="500",
                                    font_size="14px",
                                ),
                                rx.text(
                                    ConsolidadorState.maestra_tamano,
                                    font_size="12px",
                                    color=COLORS["text_muted"],
                                ),
                                spacing="0",
                                align_items="start",
                            ),
                            spacing="3",
                        ),
                        rx.spacer(),
                        rx.icon_button(
                            rx.icon("x", size=18),
                            variant="ghost",
                            color_scheme="red",
                            on_click=ConsolidadorState.eliminar_maestra,
                        ),
                        width="100%",
                        padding="16px",
                        bg=COLORS["primary_light"],
                        border_radius="8px",
                        border=f"1px solid {COLORS['primary']}",
                    ),
                    rx.hstack(
                        rx.vstack(
                            rx.text(
                                ConsolidadorState.maestra_contratos,
                                font_weight="700",
                                font_size="24px",
                                color=COLORS["primary"],
                            ),
                            rx.text("Contratos detectados", font_size="12px", color=COLORS["text_muted"]),
                            spacing="0",
                        ),
                        rx.divider(orientation="vertical", height="50px"),
                        rx.vstack(
                            rx.text("Por año:", font_weight="500", font_size="13px"),
                            rx.hstack(
                                rx.foreach(
                                    ConsolidadorState.maestra_por_ano,
                                    lambda item: rx.badge(
                                        f"{item[0]}: {item[1]}",
                                        variant="soft",
                                        size="1",
                                    ),
                                ),
                                spacing="2",
                            ),
                            spacing="1",
                            align_items="start",
                        ),
                        spacing="6",
                        padding="16px",
                        bg=COLORS["bg"],
                        border_radius="8px",
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                ),
                # Zona de upload
                rx.upload(
                    rx.box(
                        rx.vstack(
                            rx.icon("upload-cloud", size=48, color=COLORS["primary"]),
                            rx.vstack(
                                rx.text(
                                    "Arrastra tu archivo Excel aquí",
                                    font_weight="500",
                                    font_size="16px",
                                ),
                                rx.text(
                                    "o haz clic para seleccionar",
                                    font_size="14px",
                                    color=COLORS["text_muted"],
                                ),
                                spacing="1",
                            ),
                            rx.text(
                                "Formatos: .xlsx, .xls (máx. 100MB)",
                                font_size="12px",
                                color=COLORS["text_muted"],
                            ),
                            spacing="3",
                            align="center",
                        ),
                        padding="40px",
                        width="100%",
                    ),
                    id="maestra_upload",
                    accept={
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"],
                        "application/vnd.ms-excel": [".xls"],
                    },
                    max_files=1,
                    on_drop=ConsolidadorState.handle_upload(
                        rx.upload_files(upload_id="maestra_upload")
                    ),
                    border=f"2px dashed {COLORS['text_muted']}",
                    border_radius="12px",
                    bg=COLORS["bg"],
                    _hover={
                        "border_color": COLORS["primary"],
                        "bg": COLORS["primary_light"],
                    },
                    cursor="pointer",
                    transition="all 0.2s ease",
                ),
            ),
            spacing="4",
            padding="20px",
            width="100%",
        ),
        bg=COLORS["white"],
        border_radius="12px",
        box_shadow="0 1px 3px rgba(0,0,0,0.1)",
        border=f"1px solid {COLORS['bg']}",
        width="100%",
    )


def paso_2_configuracion() -> rx.Component:
    """Paso 2: Configuración de Ejecución."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.badge("PASO 2", color_scheme="blue", variant="soft"),
                rx.text("Configurar Ejecución", font_weight="600", font_size="16px"),
                spacing="3",
            ),
            rx.divider(),
            # Modo de procesamiento
            rx.text("Modo de procesamiento:", font_weight="500", font_size="14px"),
            rx.radio_group(
                rx.vstack(
                    rx.radio(
                        rx.hstack(
                            rx.text("Completo", font_weight="500"),
                            rx.text("(todos los contratos)", font_size="12px", color=COLORS["text_muted"]),
                            spacing="2",
                        ),
                        value="completo",
                    ),
                    rx.hstack(
                        rx.radio(
                            rx.text("Por año:", font_weight="500"),
                            value="por_ano",
                        ),
                        rx.select.root(
                            rx.select.trigger(placeholder="Seleccionar año"),
                            rx.select.content(
                                rx.select.item("2025", value="2025"),
                                rx.select.item("2024", value="2024"),
                                rx.select.item("2023", value="2023"),
                            ),
                            value=str(ConsolidadorState.ano_seleccionado),
                            on_change=ConsolidadorState.set_ano_seleccionado,
                            disabled=ConsolidadorState.modo_ejecucion != "por_ano",
                            size="2",
                        ),
                        spacing="2",
                    ),
                    rx.radio(
                        rx.text("Contratos específicos", font_weight="500"),
                        value="especifico",
                    ),
                    spacing="3",
                    align_items="start",
                ),
                value=ConsolidadorState.modo_ejecucion,
                on_change=ConsolidadorState.set_modo_ejecucion,
            ),
            # Búsqueda de contratos (si modo es específico)
            rx.cond(
                ConsolidadorState.modo_ejecucion == "especifico",
                rx.vstack(
                    rx.hstack(
                        rx.input(
                            placeholder="Buscar contrato...",
                            value=ConsolidadorState.busqueda_contrato,
                            on_change=ConsolidadorState.set_busqueda_contrato,
                            width="100%",
                        ),
                        rx.icon_button(
                            rx.icon("search", size=18),
                            variant="soft",
                        ),
                        width="100%",
                    ),
                    rx.box(
                        rx.vstack(
                            rx.foreach(
                                ConsolidadorState.contratos_filtrados[:10],
                                lambda c: rx.hstack(
                                    rx.checkbox(
                                        checked=c["numero"] in ConsolidadorState.contratos_seleccionados,
                                        on_change=lambda: ConsolidadorState.toggle_contrato_seleccion(c["numero"]),
                                    ),
                                    rx.text(c["numero"], font_weight="500", font_size="13px"),
                                    rx.text("-", color=COLORS["text_muted"]),
                                    rx.text(
                                        c["razon_social"][:40],
                                        font_size="13px",
                                        color=COLORS["text_muted"],
                                    ),
                                    spacing="2",
                                    padding="8px",
                                    border_radius="6px",
                                    _hover={"bg": COLORS["bg"]},
                                    width="100%",
                                ),
                            ),
                            spacing="1",
                            width="100%",
                            max_height="200px",
                            overflow_y="auto",
                        ),
                        border=f"1px solid {COLORS['bg']}",
                        border_radius="8px",
                        padding="8px",
                    ),
                    rx.text(
                        f"Seleccionados: {len(ConsolidadorState.contratos_seleccionados)} contratos",
                        font_size="12px",
                        color=COLORS["text_muted"],
                    ),
                    spacing="3",
                    width="100%",
                ),
            ),
            # Opciones avanzadas
            rx.accordion.root(
                rx.accordion.item(
                    header="Opciones avanzadas",
                    content=rx.vstack(
                        rx.checkbox(
                            "Forzar reconexión cada 10 contratos",
                            checked=ConsolidadorState.forzar_reconexion,
                            on_change=lambda v: setattr(ConsolidadorState, 'forzar_reconexion', v),
                        ),
                        rx.checkbox(
                            "Guardar en base de datos",
                            checked=ConsolidadorState.guardar_en_bd,
                            on_change=lambda v: setattr(ConsolidadorState, 'guardar_en_bd', v),
                        ),
                        rx.checkbox(
                            "Exportar alertas separadas",
                            checked=ConsolidadorState.exportar_alertas_separadas,
                            on_change=lambda v: setattr(ConsolidadorState, 'exportar_alertas_separadas', v),
                        ),
                        spacing="2",
                        align_items="start",
                    ),
                ),
                collapsible=True,
                width="100%",
            ),
            # Botón de inicio
            rx.button(
                rx.icon("rocket", size=18),
                "INICIAR CONSOLIDACIÓN",
                size="3",
                color_scheme="green",
                width="100%",
                on_click=ConsolidadorState.iniciar_consolidacion,
                disabled=~ConsolidadorState.maestra_cargada | ConsolidadorState.ejecutando,
            ),
            spacing="4",
            padding="20px",
            width="100%",
        ),
        bg=COLORS["white"],
        border_radius="12px",
        box_shadow="0 1px 3px rgba(0,0,0,0.1)",
        border=f"1px solid {COLORS['bg']}",
        width="100%",
    )


def paso_3_progreso() -> rx.Component:
    """Paso 3: Progreso de ejecución (modal)."""
    return progress_modal(
        is_open=ConsolidadorState.ejecutando,
        title="PROCESANDO",
        progress=ConsolidadorState.progreso,
        current_item=ConsolidadorState.contrato_actual,
        current_detail=ConsolidadorState.proveedor_actual,
        stats={
            "procesados": str(ConsolidadorState.contratos_procesados),
            "total": str(ConsolidadorState.total_a_procesar),
            "servicios": f"{ConsolidadorState.servicios_extraidos:,}",
            "alertas": str(ConsolidadorState.alertas_generadas),
            "tiempo": ConsolidadorState.tiempo_transcurrido,
        },
        log_messages=ConsolidadorState.log_mensajes,
        on_pause=ConsolidadorState.pausar_consolidacion,
        on_resume=ConsolidadorState.reanudar_consolidacion,
        on_cancel=ConsolidadorState.cancelar_consolidacion,
        is_paused=ConsolidadorState.pausado,
    )


def paso_4_resultados() -> rx.Component:
    """Paso 4: Resultados y descargas."""
    return rx.cond(
        ConsolidadorState.ejecucion_completada,
        rx.box(
            rx.vstack(
                # Header
                rx.hstack(
                    rx.icon("check-circle", size=32, color=COLORS["success"]),
                    rx.text("CONSOLIDACIÓN COMPLETADA", font_weight="700", font_size="18px", color=COLORS["success"]),
                    spacing="3",
                ),
                rx.divider(),
                # Stats
                rx.grid(
                    stat_card_mini(
                        title="Contratos",
                        value=ConsolidadorState.resultados.get("total_contratos", 0),
                        icon="file-text",
                    ),
                    stat_card_mini(
                        title="Exitosos",
                        value=ConsolidadorState.resultados.get("exitosos", 0),
                        icon="check",
                        color=COLORS["success"],
                    ),
                    stat_card_mini(
                        title="Fallidos",
                        value=ConsolidadorState.resultados.get("fallidos", 0),
                        icon="x",
                        color=COLORS["danger"],
                    ),
                    stat_card_mini(
                        title="Servicios",
                        value=f"{ConsolidadorState.resultados.get('servicios', 0):,}",
                        icon="list",
                        color=COLORS["primary"],
                    ),
                    columns="4",
                    spacing="3",
                    width="100%",
                ),
                rx.divider(),
                # Archivos para descarga
                rx.text("ARCHIVOS DISPONIBLES PARA DESCARGA", font_weight="600", font_size="14px"),
                # Archivo principal destacado
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("star", size=20, color=COLORS["accent"]),
                            rx.text("ARCHIVO PRINCIPAL (Recomendado)", font_weight="600", font_size="13px"),
                            spacing="2",
                        ),
                        rx.hstack(
                            rx.icon("brain", size=32, color=COLORS["primary"]),
                            rx.vstack(
                                rx.text("CONSOLIDADO_ML_LIMPIO.xlsx", font_weight="600"),
                                rx.text(
                                    "Datos consolidados + limpieza con Machine Learning",
                                    font_size="12px",
                                    color=COLORS["text_muted"],
                                ),
                                spacing="0",
                                align_items="start",
                            ),
                            spacing="3",
                            width="100%",
                        ),
                        rx.button(
                            rx.icon("download", size=18),
                            "DESCARGAR ARCHIVO PRINCIPAL",
                            color_scheme="green",
                            size="3",
                            width="100%",
                            on_click=ConsolidadorState.descargar_principal,
                        ),
                        spacing="3",
                        padding="16px",
                        width="100%",
                    ),
                    bg=COLORS["primary_light"],
                    border=f"2px solid {COLORS['primary']}",
                    border_radius="12px",
                    width="100%",
                ),
                # Lista de archivos adicionales
                rx.text("ARCHIVOS ADICIONALES", font_weight="500", font_size="13px", color=COLORS["text_muted"]),
                file_list(
                    files=ConsolidadorState.archivos_generados,
                    selectable=True,
                    on_select=ConsolidadorState.toggle_archivo_seleccion,
                    on_download=ConsolidadorState.descargar_archivo,
                ),
                # Botones de descarga
                rx.hstack(
                    rx.button(
                        rx.icon("download", size=16),
                        "DESCARGAR SELECCIONADOS",
                        variant="soft",
                        on_click=ConsolidadorState.descargar_seleccionados,
                    ),
                    rx.button(
                        rx.icon("archive", size=16),
                        "DESCARGAR TODO (.zip)",
                        variant="soft",
                        on_click=ConsolidadorState.descargar_todo,
                    ),
                    spacing="3",
                    width="100%",
                    justify="center",
                ),
                rx.divider(),
                # Acciones finales
                rx.hstack(
                    rx.button(
                        rx.icon("database", size=16),
                        "GUARDAR EN BD",
                        variant="outline",
                        color_scheme="blue",
                    ),
                    rx.button(
                        rx.icon("table", size=16),
                        "VER DATOS",
                        variant="outline",
                    ),
                    rx.button(
                        rx.icon("refresh-cw", size=16),
                        "NUEVA EJECUCIÓN",
                        variant="soft",
                        on_click=ConsolidadorState.nueva_ejecucion,
                    ),
                    spacing="3",
                    width="100%",
                    justify="center",
                ),
                spacing="4",
                padding="20px",
                width="100%",
            ),
            bg=COLORS["white"],
            border_radius="12px",
            box_shadow="0 1px 3px rgba(0,0,0,0.1)",
            border=f"1px solid {COLORS['bg']}",
            width="100%",
        ),
    )


def consolidador_content() -> rx.Component:
    """Contenido principal del consolidador."""
    return rx.box(
        rx.vstack(
            rx.cond(
                ~ConsolidadorState.ejecucion_completada,
                rx.grid(
                    paso_1_maestra(),
                    paso_2_configuracion(),
                    columns="2",
                    spacing="6",
                    width="100%",
                ),
                paso_4_resultados(),
            ),
            paso_3_progreso(),
            spacing="6",
            width="100%",
            padding="24px",
        ),
        width="100%",
        min_height="100vh",
        bg=COLORS["bg"],
    )


def consolidador_page() -> rx.Component:
    """Página completa del consolidador."""
    return rx.hstack(
        sidebar(),
        rx.box(
            rx.vstack(
                navbar(title="Consolidador T25"),
                consolidador_content(),
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
