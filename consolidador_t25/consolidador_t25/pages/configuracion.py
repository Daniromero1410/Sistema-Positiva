"""
Página de Configuración del sistema.
"""
import reflex as rx
from ..constants import COLORS, SFTP_CONFIG
from ..components.sidebar import sidebar
from ..components.navbar import navbar


class ConfigState(rx.State):
    """Estado de la configuración."""

    # SFTP
    sftp_host: str = SFTP_CONFIG["host"]
    sftp_port: int = SFTP_CONFIG["port"]
    sftp_username: str = SFTP_CONFIG["username"]
    sftp_password: str = ""  # No mostrar por seguridad
    sftp_timeout: int = SFTP_CONFIG["timeout"]
    sftp_carpeta: str = SFTP_CONFIG["carpeta_principal"]

    # Base de datos
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "consolidador_t25"
    db_user: str = "postgres"

    # Procesamiento
    max_reintentos: int = 3
    timeout_archivo: int = 60
    lote_size: int = 10

    # Notificaciones
    notif_email: bool = True
    notif_email_address: str = ""
    notif_webhook: bool = False
    notif_webhook_url: str = ""

    # Estado de prueba de conexión
    probando_sftp: bool = False
    probando_db: bool = False
    resultado_sftp: str = ""
    resultado_db: str = ""

    def set_sftp_host(self, value: str):
        self.sftp_host = value

    def set_sftp_port(self, value: str):
        self.sftp_port = int(value) if value.isdigit() else 2243

    def set_sftp_username(self, value: str):
        self.sftp_username = value

    def set_sftp_password(self, value: str):
        self.sftp_password = value

    async def probar_conexion_sftp(self):
        """Prueba la conexión SFTP."""
        self.probando_sftp = True
        self.resultado_sftp = ""

        try:
            import asyncio
            await asyncio.sleep(1)  # Simular prueba
            self.resultado_sftp = "success"
        except Exception as e:
            self.resultado_sftp = f"error: {str(e)}"
        finally:
            self.probando_sftp = False

    async def probar_conexion_db(self):
        """Prueba la conexión a la base de datos."""
        self.probando_db = True
        self.resultado_db = ""

        try:
            import asyncio
            await asyncio.sleep(1)  # Simular prueba
            self.resultado_db = "success"
        except Exception as e:
            self.resultado_db = f"error: {str(e)}"
        finally:
            self.probando_db = False

    def guardar_configuracion(self):
        """Guarda la configuración."""
        # TODO: Guardar en archivo .env o base de datos
        pass


def sftp_config_section() -> rx.Component:
    """Sección de configuración SFTP."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("server", size=20, color=COLORS["primary"]),
                rx.text("Configuración SFTP GoAnywhere", font_weight="600", font_size="16px"),
                spacing="3",
            ),
            rx.divider(),
            rx.grid(
                rx.vstack(
                    rx.text("Host", font_size="13px", font_weight="500"),
                    rx.input(
                        value=ConfigState.sftp_host,
                        on_change=ConfigState.set_sftp_host,
                        placeholder="mft.positiva.gov.co",
                        width="100%",
                    ),
                    spacing="1",
                    align_items="start",
                ),
                rx.vstack(
                    rx.text("Puerto", font_size="13px", font_weight="500"),
                    rx.input(
                        value=str(ConfigState.sftp_port),
                        on_change=ConfigState.set_sftp_port,
                        placeholder="2243",
                        width="100%",
                    ),
                    spacing="1",
                    align_items="start",
                ),
                rx.vstack(
                    rx.text("Usuario", font_size="13px", font_weight="500"),
                    rx.input(
                        value=ConfigState.sftp_username,
                        on_change=ConfigState.set_sftp_username,
                        placeholder="G_medica",
                        width="100%",
                    ),
                    spacing="1",
                    align_items="start",
                ),
                rx.vstack(
                    rx.text("Contraseña", font_size="13px", font_weight="500"),
                    rx.input(
                        value=ConfigState.sftp_password,
                        on_change=ConfigState.set_sftp_password,
                        type="password",
                        placeholder="••••••••",
                        width="100%",
                    ),
                    spacing="1",
                    align_items="start",
                ),
                columns="2",
                spacing="4",
                width="100%",
            ),
            rx.vstack(
                rx.text("Carpeta Principal", font_size="13px", font_weight="500"),
                rx.input(
                    value=ConfigState.sftp_carpeta,
                    placeholder="R.A-ABASTECIMIENTO RED ASISTENCIAL",
                    width="100%",
                ),
                spacing="1",
                align_items="start",
                width="100%",
            ),
            rx.hstack(
                rx.button(
                    rx.icon("plug", size=14),
                    "Probar Conexión",
                    variant="soft",
                    on_click=ConfigState.probar_conexion_sftp,
                    loading=ConfigState.probando_sftp,
                ),
                rx.cond(
                    ConfigState.resultado_sftp == "success",
                    rx.hstack(
                        rx.icon("check-circle", size=16, color=COLORS["success"]),
                        rx.text("Conexión exitosa", color=COLORS["success"], font_size="13px"),
                        spacing="2",
                    ),
                ),
                rx.cond(
                    ConfigState.resultado_sftp.startswith("error"),
                    rx.hstack(
                        rx.icon("x-circle", size=16, color=COLORS["danger"]),
                        rx.text("Error de conexión", color=COLORS["danger"], font_size="13px"),
                        spacing="2",
                    ),
                ),
                spacing="3",
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


def db_config_section() -> rx.Component:
    """Sección de configuración de base de datos."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("database", size=20, color=COLORS["info"]),
                rx.text("Configuración Base de Datos", font_weight="600", font_size="16px"),
                spacing="3",
            ),
            rx.divider(),
            rx.grid(
                rx.vstack(
                    rx.text("Host", font_size="13px", font_weight="500"),
                    rx.input(
                        value=ConfigState.db_host,
                        placeholder="localhost",
                        width="100%",
                    ),
                    spacing="1",
                    align_items="start",
                ),
                rx.vstack(
                    rx.text("Puerto", font_size="13px", font_weight="500"),
                    rx.input(
                        value=str(ConfigState.db_port),
                        placeholder="5432",
                        width="100%",
                    ),
                    spacing="1",
                    align_items="start",
                ),
                rx.vstack(
                    rx.text("Base de Datos", font_size="13px", font_weight="500"),
                    rx.input(
                        value=ConfigState.db_name,
                        placeholder="consolidador_t25",
                        width="100%",
                    ),
                    spacing="1",
                    align_items="start",
                ),
                rx.vstack(
                    rx.text("Usuario", font_size="13px", font_weight="500"),
                    rx.input(
                        value=ConfigState.db_user,
                        placeholder="postgres",
                        width="100%",
                    ),
                    spacing="1",
                    align_items="start",
                ),
                columns="2",
                spacing="4",
                width="100%",
            ),
            rx.hstack(
                rx.button(
                    rx.icon("plug", size=14),
                    "Probar Conexión",
                    variant="soft",
                    on_click=ConfigState.probar_conexion_db,
                    loading=ConfigState.probando_db,
                ),
                rx.cond(
                    ConfigState.resultado_db == "success",
                    rx.hstack(
                        rx.icon("check-circle", size=16, color=COLORS["success"]),
                        rx.text("Conexión exitosa", color=COLORS["success"], font_size="13px"),
                        spacing="2",
                    ),
                ),
                spacing="3",
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


def procesamiento_config_section() -> rx.Component:
    """Sección de configuración de procesamiento."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("settings-2", size=20, color=COLORS["accent"]),
                rx.text("Configuración de Procesamiento", font_weight="600", font_size="16px"),
                spacing="3",
            ),
            rx.divider(),
            rx.grid(
                rx.vstack(
                    rx.text("Máximo de reintentos", font_size="13px", font_weight="500"),
                    rx.input(
                        value=str(ConfigState.max_reintentos),
                        type="number",
                        width="100%",
                    ),
                    rx.text(
                        "Intentos antes de marcar como fallido",
                        font_size="11px",
                        color=COLORS["text_muted"],
                    ),
                    spacing="1",
                    align_items="start",
                ),
                rx.vstack(
                    rx.text("Timeout por archivo (seg)", font_size="13px", font_weight="500"),
                    rx.input(
                        value=str(ConfigState.timeout_archivo),
                        type="number",
                        width="100%",
                    ),
                    rx.text(
                        "Tiempo máximo de espera por archivo",
                        font_size="11px",
                        color=COLORS["text_muted"],
                    ),
                    spacing="1",
                    align_items="start",
                ),
                rx.vstack(
                    rx.text("Tamaño de lote", font_size="13px", font_weight="500"),
                    rx.input(
                        value=str(ConfigState.lote_size),
                        type="number",
                        width="100%",
                    ),
                    rx.text(
                        "Contratos a procesar antes de reconectar",
                        font_size="11px",
                        color=COLORS["text_muted"],
                    ),
                    spacing="1",
                    align_items="start",
                ),
                columns="3",
                spacing="4",
                width="100%",
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


def notificaciones_config_section() -> rx.Component:
    """Sección de configuración de notificaciones."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("bell", size=20, color=COLORS["warning"]),
                rx.text("Notificaciones", font_weight="600", font_size="16px"),
                spacing="3",
            ),
            rx.divider(),
            rx.vstack(
                rx.hstack(
                    rx.switch(
                        checked=ConfigState.notif_email,
                    ),
                    rx.vstack(
                        rx.text("Notificaciones por Email", font_weight="500"),
                        rx.text(
                            "Recibir alertas y resúmenes por correo",
                            font_size="12px",
                            color=COLORS["text_muted"],
                        ),
                        spacing="0",
                        align_items="start",
                    ),
                    spacing="3",
                    width="100%",
                ),
                rx.cond(
                    ConfigState.notif_email,
                    rx.input(
                        value=ConfigState.notif_email_address,
                        placeholder="correo@positiva.gov.co",
                        width="100%",
                    ),
                ),
                rx.divider(),
                rx.hstack(
                    rx.switch(
                        checked=ConfigState.notif_webhook,
                    ),
                    rx.vstack(
                        rx.text("Webhook (Teams/Slack)", font_weight="500"),
                        rx.text(
                            "Enviar notificaciones a canal de Teams o Slack",
                            font_size="12px",
                            color=COLORS["text_muted"],
                        ),
                        spacing="0",
                        align_items="start",
                    ),
                    spacing="3",
                    width="100%",
                ),
                rx.cond(
                    ConfigState.notif_webhook,
                    rx.input(
                        value=ConfigState.notif_webhook_url,
                        placeholder="https://hooks.teams.microsoft.com/...",
                        width="100%",
                    ),
                ),
                spacing="4",
                width="100%",
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


def configuracion_content() -> rx.Component:
    """Contenido principal de configuración."""
    return rx.box(
        rx.vstack(
            rx.grid(
                sftp_config_section(),
                db_config_section(),
                columns="2",
                spacing="4",
                width="100%",
            ),
            rx.grid(
                procesamiento_config_section(),
                notificaciones_config_section(),
                columns="2",
                spacing="4",
                width="100%",
            ),
            # Botón guardar
            rx.hstack(
                rx.spacer(),
                rx.button(
                    rx.icon("save", size=16),
                    "Guardar Configuración",
                    color_scheme="green",
                    size="3",
                    on_click=ConfigState.guardar_configuracion,
                ),
                width="100%",
            ),
            spacing="6",
            width="100%",
            padding="24px",
        ),
        width="100%",
        min_height="100vh",
        bg=COLORS["bg"],
    )


def configuracion_page() -> rx.Component:
    """Página completa de configuración."""
    return rx.hstack(
        sidebar(),
        rx.box(
            rx.vstack(
                navbar(title="Configuración"),
                configuracion_content(),
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
