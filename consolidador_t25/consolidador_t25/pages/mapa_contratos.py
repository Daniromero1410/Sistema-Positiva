"""
Página Mapa de Contratos.
Utiliza MapLibre GL JS + Deck.gl para visualización 3D.
"""
import reflex as rx
import json
from ..constants import COLORS, COORDENADAS_MUNICIPIOS
from ..components.sidebar import sidebar
from ..components.navbar import navbar


class MapaState(rx.State):
    """Estado del mapa de contratos."""

    # Filtros
    filtro_ano: str = "2025"
    filtro_departamento: str = "Todos"
    filtro_vista: str = "columnas"  # columnas, puntos, heatmap

    # Datos
    contratos_mapa: list = []
    contrato_seleccionado: dict = None
    show_detalle: bool = False

    # Estadísticas
    total_contratos_mapa: int = 925
    ciudades_unicas: int = 216
    departamentos_unicos: int = 33

    # Datos de ejemplo por ciudad
    datos_ciudades: list = [
        {"ciudad": "BOGOTA", "departamento": "BOGOTA", "lat": 4.7110, "lon": -74.0721, "contratos": 133, "alertas": 5},
        {"ciudad": "BARRANQUILLA", "departamento": "ATLANTICO", "lat": 10.9685, "lon": -74.7813, "contratos": 32, "alertas": 2},
        {"ciudad": "MEDELLIN", "departamento": "ANTIOQUIA", "lat": 6.2476, "lon": -75.5658, "contratos": 29, "alertas": 3},
        {"ciudad": "BUCARAMANGA", "departamento": "SANTANDER", "lat": 7.1193, "lon": -73.1227, "contratos": 24, "alertas": 1},
        {"ciudad": "CARTAGENA", "departamento": "BOLIVAR", "lat": 10.3997, "lon": -75.5144, "contratos": 23, "alertas": 2},
        {"ciudad": "PASTO", "departamento": "NARINO", "lat": 1.2136, "lon": -77.2811, "contratos": 20, "alertas": 0},
        {"ciudad": "VALLEDUPAR", "departamento": "CESAR", "lat": 10.4631, "lon": -73.2532, "contratos": 19, "alertas": 1},
        {"ciudad": "PEREIRA", "departamento": "RISARALDA", "lat": 4.8087, "lon": -75.6906, "contratos": 19, "alertas": 0},
        {"ciudad": "IBAGUE", "departamento": "TOLIMA", "lat": 4.4389, "lon": -75.2322, "contratos": 19, "alertas": 2},
        {"ciudad": "CUCUTA", "departamento": "NORTE DE SANTANDER", "lat": 7.8939, "lon": -72.5078, "contratos": 18, "alertas": 1},
        {"ciudad": "CALI", "departamento": "VALLE DEL CAUCA", "lat": 3.4516, "lon": -76.5320, "contratos": 17, "alertas": 0},
        {"ciudad": "VILLAVICENCIO", "departamento": "META", "lat": 4.1420, "lon": -73.6266, "contratos": 16, "alertas": 1},
        {"ciudad": "NEIVA", "departamento": "HUILA", "lat": 2.9273, "lon": -75.2819, "contratos": 15, "alertas": 0},
        {"ciudad": "MANIZALES", "departamento": "CALDAS", "lat": 5.0703, "lon": -75.5138, "contratos": 14, "alertas": 1},
        {"ciudad": "MONTERIA", "departamento": "CORDOBA", "lat": 8.7575, "lon": -75.8856, "contratos": 13, "alertas": 0},
    ]

    def set_filtro_ano(self, ano: str):
        """Establece el filtro de año."""
        self.filtro_ano = ano

    def set_filtro_departamento(self, depto: str):
        """Establece el filtro de departamento."""
        self.filtro_departamento = depto

    def set_filtro_vista(self, vista: str):
        """Establece el tipo de vista."""
        self.filtro_vista = vista

    def seleccionar_ciudad(self, ciudad: dict):
        """Selecciona una ciudad para ver detalles."""
        self.contrato_seleccionado = ciudad
        self.show_detalle = True

    def cerrar_detalle(self):
        """Cierra el panel de detalle."""
        self.show_detalle = False
        self.contrato_seleccionado = None


def mapa_component() -> rx.Component:
    """Componente del mapa con MapLibre GL + Deck.gl."""
    # Preparar datos para el mapa
    datos_json = json.dumps(MapaState.datos_ciudades)

    mapa_html = f'''
    <div id="map-container" style="width: 100%; height: 500px; border-radius: 12px; overflow: hidden; position: relative;">
        <div id="map" style="width: 100%; height: 100%;"></div>
        <div id="tooltip" style="position: absolute; z-index: 1; pointer-events: none; background: rgba(26, 54, 93, 0.95); color: white; padding: 12px 16px; border-radius: 8px; font-size: 13px; display: none; box-shadow: 0 4px 12px rgba(0,0,0,0.3);"></div>
        <div id="legend" style="position: absolute; bottom: 16px; left: 16px; background: rgba(255,255,255,0.95); padding: 12px 16px; border-radius: 8px; font-size: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <div style="font-weight: 600; margin-bottom: 8px;">Contratos por Ciudad</div>
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                <div style="width: 12px; height: 12px; background: #00A651; border-radius: 2px;"></div>
                <span>1-20</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                <div style="width: 16px; height: 16px; background: #00A651; border-radius: 2px;"></div>
                <span>21-50</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                <div style="width: 20px; height: 20px; background: #00A651; border-radius: 2px;"></div>
                <span>51-100</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 24px; height: 24px; background: #00A651; border-radius: 2px;"></div>
                <span>100+</span>
            </div>
        </div>
    </div>

    <link href="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.css" rel="stylesheet" />
    <script src="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.js"></script>
    <script src="https://unpkg.com/deck.gl@8.9.35/dist.min.js"></script>

    <script>
        (function() {{
            const datos = {datos_json};
            const tooltip = document.getElementById('tooltip');

            // Inicializar mapa
            const map = new maplibregl.Map({{
                container: 'map',
                style: 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
                center: [-74.0721, 4.7110],
                zoom: 5,
                pitch: 45,
                bearing: -17.6,
            }});

            // Agregar controles
            map.addControl(new maplibregl.NavigationControl());
            map.addControl(new maplibregl.FullscreenControl());

            // Función para actualizar tooltip
            function updateTooltip(info) {{
                if (info.object) {{
                    tooltip.style.display = 'block';
                    tooltip.style.left = info.x + 'px';
                    tooltip.style.top = info.y + 'px';
                    tooltip.innerHTML = `
                        <div style="font-weight: 600; font-size: 14px;">${{info.object.ciudad}}</div>
                        <div style="color: #00A651; margin: 4px 0;">${{info.object.departamento}}</div>
                        <div style="display: flex; justify-content: space-between; gap: 20px;">
                            <span>Contratos: <strong>${{info.object.contratos}}</strong></span>
                            <span>Alertas: <strong style="color: #F7941D;">${{info.object.alertas}}</strong></span>
                        </div>
                    `;
                }} else {{
                    tooltip.style.display = 'none';
                }}
            }}

            // Crear overlay de Deck.gl
            map.on('load', function() {{
                const deckOverlay = new deck.MapboxOverlay({{
                    interleaved: true,
                    layers: [
                        // Capa de columnas 3D
                        new deck.ColumnLayer({{
                            id: 'columnas',
                            data: datos,
                            getPosition: d => [d.lon, d.lat],
                            getElevation: d => d.contratos * 500,
                            getFillColor: d => d.alertas > 0 ? [247, 148, 29, 220] : [0, 166, 81, 220],
                            radius: 8000,
                            elevationScale: 1,
                            pickable: true,
                            autoHighlight: true,
                            highlightColor: [255, 255, 255, 100],
                            onHover: updateTooltip,
                        }}),
                        // Capa de puntos base
                        new deck.ScatterplotLayer({{
                            id: 'puntos-base',
                            data: datos,
                            getPosition: d => [d.lon, d.lat],
                            getRadius: d => Math.sqrt(d.contratos) * 2000,
                            getFillColor: [0, 166, 81, 100],
                            pickable: false,
                        }}),
                    ],
                }});

                map.addControl(deckOverlay);
            }});
        }})();
    </script>
    '''

    return rx.html(mapa_html)


def filters_bar() -> rx.Component:
    """Barra de filtros del mapa."""
    return rx.hstack(
        rx.text("Filtros:", font_weight="500", font_size="14px"),
        rx.select.root(
            rx.select.trigger(placeholder="Año"),
            rx.select.content(
                rx.select.item("2025", value="2025"),
                rx.select.item("2024", value="2024"),
                rx.select.item("Todos", value="Todos"),
            ),
            value=MapaState.filtro_ano,
            on_change=MapaState.set_filtro_ano,
            size="2",
        ),
        rx.select.root(
            rx.select.trigger(placeholder="Departamento"),
            rx.select.content(
                rx.select.item("Todos", value="Todos"),
                rx.select.item("Bogotá", value="BOGOTA"),
                rx.select.item("Antioquia", value="ANTIOQUIA"),
                rx.select.item("Valle del Cauca", value="VALLE DEL CAUCA"),
                rx.select.item("Atlántico", value="ATLANTICO"),
            ),
            value=MapaState.filtro_departamento,
            on_change=MapaState.set_filtro_departamento,
            size="2",
        ),
        rx.divider(orientation="vertical", height="24px"),
        rx.text("Vista:", font_size="14px", color=COLORS["text_muted"]),
        rx.segment.root(
            rx.segment.item(
                rx.hstack(rx.icon("bar-chart-3", size=14), "3D", spacing="1"),
                value="columnas",
            ),
            rx.segment.item(
                rx.hstack(rx.icon("map-pin", size=14), "Puntos", spacing="1"),
                value="puntos",
            ),
            rx.segment.item(
                rx.hstack(rx.icon("flame", size=14), "Heat", spacing="1"),
                value="heatmap",
            ),
            value=MapaState.filtro_vista,
            on_change=MapaState.set_filtro_vista,
            size="1",
        ),
        spacing="4",
        width="100%",
        flex_wrap="wrap",
    )


def stats_bar() -> rx.Component:
    """Barra de estadísticas del mapa."""
    return rx.hstack(
        rx.hstack(
            rx.icon("file-text", size=18, color=COLORS["primary"]),
            rx.text(
                f"Total: {MapaState.total_contratos_mapa} contratos",
                font_size="13px",
            ),
            spacing="2",
        ),
        rx.divider(orientation="vertical", height="20px"),
        rx.hstack(
            rx.icon("map-pin", size=18, color=COLORS["accent"]),
            rx.text(
                f"{MapaState.ciudades_unicas} ciudades",
                font_size="13px",
            ),
            spacing="2",
        ),
        rx.divider(orientation="vertical", height="20px"),
        rx.hstack(
            rx.icon("map", size=18, color=COLORS["info"]),
            rx.text(
                f"{MapaState.departamentos_unicos} departamentos",
                font_size="13px",
            ),
            spacing="2",
        ),
        spacing="4",
        padding="12px 16px",
        bg=COLORS["white"],
        border_radius="8px",
        box_shadow="0 1px 3px rgba(0,0,0,0.1)",
    )


def top_ciudades_panel() -> rx.Component:
    """Panel lateral con top ciudades."""
    return rx.box(
        rx.vstack(
            rx.text("TOP 10 CIUDADES", font_size="11px", font_weight="600", color=COLORS["text_muted"]),
            rx.divider(),
            rx.vstack(
                rx.foreach(
                    MapaState.datos_ciudades[:10],
                    lambda c, idx: rx.hstack(
                        rx.text(
                            f"{idx + 1}.",
                            font_size="12px",
                            color=COLORS["text_muted"],
                            width="20px",
                        ),
                        rx.vstack(
                            rx.text(c["ciudad"], font_size="13px", font_weight="500"),
                            rx.text(c["departamento"], font_size="11px", color=COLORS["text_muted"]),
                            spacing="0",
                            align_items="start",
                            flex="1",
                        ),
                        rx.badge(
                            str(c["contratos"]),
                            color_scheme="green",
                            variant="soft",
                        ),
                        spacing="2",
                        width="100%",
                        padding="8px",
                        border_radius="6px",
                        _hover={"bg": COLORS["bg"]},
                        cursor="pointer",
                    ),
                ),
                spacing="1",
                width="100%",
            ),
            spacing="3",
            padding="16px",
            width="100%",
        ),
        bg=COLORS["white"],
        border_radius="12px",
        box_shadow="0 1px 3px rgba(0,0,0,0.1)",
        min_width="280px",
    )


def mapa_content() -> rx.Component:
    """Contenido principal del mapa."""
    return rx.box(
        rx.vstack(
            filters_bar(),
            stats_bar(),
            rx.hstack(
                # Mapa principal
                rx.box(
                    mapa_component(),
                    bg=COLORS["white"],
                    border_radius="12px",
                    box_shadow="0 1px 3px rgba(0,0,0,0.1)",
                    overflow="hidden",
                    flex="1",
                ),
                # Panel lateral
                top_ciudades_panel(),
                spacing="4",
                width="100%",
                align_items="start",
            ),
            spacing="4",
            width="100%",
            padding="24px",
        ),
        width="100%",
        min_height="100vh",
        bg=COLORS["bg"],
    )


def mapa_page() -> rx.Component:
    """Página completa del mapa de contratos."""
    return rx.hstack(
        sidebar(),
        rx.box(
            rx.vstack(
                navbar(title="Mapa de Contratos"),
                mapa_content(),
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
