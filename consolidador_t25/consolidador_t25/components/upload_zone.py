"""
Componente UploadZone para carga de archivos con drag & drop.
"""
import reflex as rx
from typing import Callable, List
from ..constants import COLORS


def upload_zone(
    on_upload: Callable,
    accepted_types: List[str] = None,
    max_size_mb: int = 100,
    uploaded_file: dict = None,
    on_remove: Callable = None,
) -> rx.Component:
    """
    Zona de carga de archivos con drag & drop.

    Args:
        on_upload: Callback al cargar archivo
        accepted_types: Tipos de archivo aceptados
        max_size_mb: Tamaño máximo en MB
        uploaded_file: Archivo ya cargado (para mostrar)
        on_remove: Callback para eliminar archivo
    """
    accepted_types = accepted_types or [".xlsx", ".xls", ".xlsb"]
    accept_str = ", ".join(accepted_types)

    return rx.cond(
        uploaded_file is not None,
        # Archivo cargado
        rx.box(
            rx.hstack(
                rx.hstack(
                    rx.icon("file-spreadsheet", size=32, color=COLORS["primary"]),
                    rx.vstack(
                        rx.text(
                            uploaded_file["name"] if uploaded_file else "",
                            font_weight="500",
                            font_size="14px",
                            color=COLORS["text"],
                        ),
                        rx.text(
                            uploaded_file["size"] if uploaded_file else "",
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
                    color=COLORS["danger"],
                    on_click=on_remove,
                    cursor="pointer",
                ),
                width="100%",
                padding="16px",
                bg=COLORS["primary_light"],
                border_radius="8px",
                border=f"1px solid {COLORS['primary']}",
            ),
        ),
        # Zona de upload
        rx.upload(
            rx.box(
                rx.vstack(
                    rx.icon(
                        "upload-cloud",
                        size=48,
                        color=COLORS["primary"],
                    ),
                    rx.vstack(
                        rx.text(
                            "Arrastra tu archivo Excel aquí",
                            font_weight="500",
                            font_size="16px",
                            color=COLORS["text"],
                        ),
                        rx.text(
                            "o haz clic para seleccionar",
                            font_size="14px",
                            color=COLORS["text_muted"],
                        ),
                        spacing="1",
                    ),
                    rx.text(
                        f"Formatos: {accept_str} (máx. {max_size_mb}MB)",
                        font_size="12px",
                        color=COLORS["text_muted"],
                    ),
                    spacing="3",
                    align="center",
                ),
                padding="40px",
                width="100%",
            ),
            id="upload_zone",
            accept={
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"],
                "application/vnd.ms-excel": [".xls"],
                "application/vnd.ms-excel.sheet.binary.macroEnabled.12": [".xlsb"],
            },
            max_files=1,
            max_size=max_size_mb * 1024 * 1024,
            on_drop=on_upload,
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
    )


def upload_zone_simple(
    id: str,
    on_upload: Callable,
    label: str = "Arrastra archivos aquí",
) -> rx.Component:
    """Versión simplificada de la zona de upload."""
    return rx.upload(
        rx.center(
            rx.vstack(
                rx.icon("upload", size=24, color=COLORS["text_muted"]),
                rx.text(label, font_size="14px", color=COLORS["text_muted"]),
                spacing="2",
            ),
            padding="24px",
        ),
        id=id,
        on_drop=on_upload,
        border=f"2px dashed {COLORS['text_muted']}",
        border_radius="8px",
        _hover={"border_color": COLORS["primary"]},
        cursor="pointer",
    )


def file_list(
    files: List[dict],
    on_remove: Callable = None,
    on_download: Callable = None,
    selectable: bool = False,
    on_select: Callable = None,
) -> rx.Component:
    """Lista de archivos cargados o generados."""
    return rx.vstack(
        rx.foreach(
            files,
            lambda f: rx.hstack(
                rx.cond(
                    selectable,
                    rx.checkbox(
                        checked=f.get("seleccionado", False),
                        on_change=lambda: on_select(f["nombre"]) if on_select else None,
                        size="2",
                    ),
                ),
                rx.hstack(
                    rx.icon(
                        rx.cond(
                            f.get("es_principal", False),
                            "star",
                            "file"
                        ),
                        size=20,
                        color=rx.cond(
                            f.get("es_principal", False),
                            COLORS["accent"],
                            COLORS["text_muted"],
                        ),
                    ),
                    rx.vstack(
                        rx.text(
                            f["nombre"],
                            font_weight="500",
                            font_size="14px",
                            color=COLORS["text"],
                        ),
                        rx.text(
                            f.get("descripcion", ""),
                            font_size="12px",
                            color=COLORS["text_muted"],
                        ),
                        spacing="0",
                        align_items="start",
                    ),
                    spacing="3",
                    flex="1",
                ),
                rx.spacer(),
                rx.text(
                    f.get("tamano", ""),
                    font_size="12px",
                    color=COLORS["text_muted"],
                ),
                rx.hstack(
                    rx.cond(
                        on_download is not None,
                        rx.icon_button(
                            rx.icon("download", size=16),
                            variant="ghost",
                            size="1",
                            on_click=lambda: on_download(f["ruta"]) if on_download else None,
                        ),
                    ),
                    rx.cond(
                        on_remove is not None,
                        rx.icon_button(
                            rx.icon("x", size=16),
                            variant="ghost",
                            color=COLORS["danger"],
                            size="1",
                            on_click=lambda: on_remove(f["nombre"]) if on_remove else None,
                        ),
                    ),
                    spacing="1",
                ),
                width="100%",
                padding="12px",
                border_radius="8px",
                border=f"1px solid {COLORS['bg']}",
                bg=rx.cond(
                    f.get("es_principal", False),
                    COLORS["primary_light"],
                    COLORS["white"],
                ),
                _hover={"bg": COLORS["bg"]},
            ),
        ),
        width="100%",
        spacing="2",
    )
