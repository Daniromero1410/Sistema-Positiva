"""
Componente DataTable para mostrar tablas de datos.
"""
import reflex as rx
from typing import List, Dict, Callable
from ..constants import COLORS


def data_table(
    columns: List[Dict],
    data: List[Dict],
    on_row_click: Callable = None,
    selectable: bool = False,
    on_select: Callable = None,
    selected_rows: List = None,
    loading: bool = False,
    empty_message: str = "No hay datos disponibles",
) -> rx.Component:
    """
    Tabla de datos con soporte para selección, ordenamiento y acciones.

    Args:
        columns: Lista de columnas [{key, label, width, sortable}]
        data: Lista de datos a mostrar
        on_row_click: Callback al hacer clic en una fila
        selectable: Si las filas son seleccionables
        on_select: Callback al seleccionar una fila
        selected_rows: Lista de IDs de filas seleccionadas
        loading: Estado de carga
        empty_message: Mensaje cuando no hay datos
    """
    selected_rows = selected_rows or []

    def render_header():
        return rx.table.header(
            rx.table.row(
                rx.cond(
                    selectable,
                    rx.table.column_header_cell(
                        rx.checkbox(
                            size="1",
                        ),
                        width="40px",
                    ),
                ),
                *[
                    rx.table.column_header_cell(
                        rx.hstack(
                            rx.text(
                                col.get("label", col.get("key", "")),
                                font_weight="600",
                                font_size="13px",
                                color=COLORS["text_muted"],
                            ),
                            rx.cond(
                                col.get("sortable", False),
                                rx.icon("chevrons-up-down", size=14, color=COLORS["text_muted"]),
                            ),
                            spacing="1",
                            cursor="pointer" if col.get("sortable") else "default",
                        ),
                        width=col.get("width", "auto"),
                    )
                    for col in columns
                ],
                bg=COLORS["bg"],
            ),
        )

    def render_row(row: Dict, index: int):
        is_selected = row.get("id", index) in selected_rows

        return rx.table.row(
            rx.cond(
                selectable,
                rx.table.cell(
                    rx.checkbox(
                        checked=is_selected,
                        on_change=lambda: on_select(row.get("id", index)) if on_select else None,
                        size="1",
                    ),
                ),
            ),
            *[
                rx.table.cell(
                    rx.text(
                        str(row.get(col.get("key", ""), "")),
                        font_size="13px",
                        color=COLORS["text"],
                    ),
                )
                for col in columns
            ],
            bg=COLORS["primary_light"] if is_selected else COLORS["white"],
            _hover={"bg": COLORS["bg"]},
            cursor="pointer" if on_row_click else "default",
            on_click=lambda: on_row_click(row) if on_row_click else None,
        )

    return rx.box(
        rx.cond(
            loading,
            rx.center(
                rx.spinner(size="3"),
                padding="40px",
            ),
            rx.cond(
                len(data) > 0,
                rx.table.root(
                    render_header(),
                    rx.table.body(
                        rx.foreach(
                            data,
                            lambda row, idx: render_row(row, idx),
                        ),
                    ),
                    width="100%",
                    variant="surface",
                ),
                rx.center(
                    rx.vstack(
                        rx.icon("inbox", size=48, color=COLORS["text_muted"]),
                        rx.text(
                            empty_message,
                            color=COLORS["text_muted"],
                            font_size="14px",
                        ),
                        spacing="3",
                    ),
                    padding="60px",
                ),
            ),
        ),
        width="100%",
        overflow_x="auto",
    )


def simple_table(
    headers: List[str],
    rows: List[List[str]],
) -> rx.Component:
    """Tabla simple sin funcionalidades avanzadas."""
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                *[
                    rx.table.column_header_cell(
                        rx.text(
                            header,
                            font_weight="600",
                            font_size="13px",
                            color=COLORS["text_muted"],
                        ),
                    )
                    for header in headers
                ],
                bg=COLORS["bg"],
            ),
        ),
        rx.table.body(
            *[
                rx.table.row(
                    *[
                        rx.table.cell(
                            rx.text(
                                cell,
                                font_size="13px",
                            ),
                        )
                        for cell in row
                    ],
                    _hover={"bg": COLORS["bg"]},
                )
                for row in rows
            ],
        ),
        width="100%",
        variant="surface",
    )


def execution_table(executions: List[Dict]) -> rx.Component:
    """Tabla específica para historial de ejecuciones."""
    def status_badge(status: str):
        color_map = {
            "COMPLETADO": "green",
            "EN_PROCESO": "blue",
            "ERROR": "red",
            "CANCELADO": "yellow",
        }
        return rx.badge(
            status,
            color_scheme=color_map.get(status, "gray"),
            variant="soft",
            size="1",
        )

    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Fecha", width="150px"),
                rx.table.column_header_cell("Estado", width="120px"),
                rx.table.column_header_cell("Contratos", width="100px"),
                rx.table.column_header_cell("Servicios", width="100px"),
                rx.table.column_header_cell("Alertas", width="80px"),
                rx.table.column_header_cell("Acciones", width="100px"),
                bg=COLORS["bg"],
            ),
        ),
        rx.table.body(
            rx.foreach(
                executions,
                lambda e: rx.table.row(
                    rx.table.cell(
                        rx.text(e["fecha"], font_size="13px"),
                    ),
                    rx.table.cell(status_badge(e["estado"])),
                    rx.table.cell(
                        rx.text(e["contratos"], font_size="13px"),
                    ),
                    rx.table.cell(
                        rx.text(e["servicios"], font_size="13px"),
                    ),
                    rx.table.cell(
                        rx.text(e["alertas"], font_size="13px"),
                    ),
                    rx.table.cell(
                        rx.hstack(
                            rx.icon_button(
                                rx.icon("eye", size=14),
                                size="1",
                                variant="ghost",
                            ),
                            rx.icon_button(
                                rx.icon("download", size=14),
                                size="1",
                                variant="ghost",
                            ),
                            spacing="1",
                        ),
                    ),
                    _hover={"bg": COLORS["bg"]},
                ),
            ),
        ),
        width="100%",
        variant="surface",
    )
