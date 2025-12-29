"""
Constantes y configuración de la aplicación Consolidador T25.
Paleta de colores POSITIVA y configuraciones generales.
"""

# ══════════════════════════════════════════════════════════════════════════════
# PALETA DE COLORES - POSITIVA
# ══════════════════════════════════════════════════════════════════════════════

COLORES_POSITIVA = {
    # Colores principales
    "verde_principal": "#00A651",      # Verde POSITIVA (primario)
    "verde_oscuro": "#008C45",         # Verde hover/activo
    "verde_claro": "#E8F5E9",          # Verde para backgrounds suaves

    # Colores secundarios
    "azul_oscuro": "#1A365D",          # Para textos y sidebar
    "azul_medio": "#2D4A6F",           # Para headers
    "azul_claro": "#EBF4FF",           # Para backgrounds

    # Acentos
    "naranja": "#F7941D",              # Para alertas y highlights
    "amarillo": "#FFC107",             # Para warnings
    "rojo": "#DC3545",                 # Para errores

    # Neutros
    "blanco": "#FFFFFF",
    "gris_claro": "#F8F9FA",           # Background principal
    "gris_medio": "#6C757D",           # Textos secundarios
    "gris_oscuro": "#343A40",          # Textos principales

    # Estados
    "exito": "#28A745",
    "info": "#17A2B8",
    "warning": "#FFC107",
    "danger": "#DC3545",
}

# Alias para uso en componentes Reflex
COLORS = {
    "primary": COLORES_POSITIVA["verde_principal"],
    "primary_hover": COLORES_POSITIVA["verde_oscuro"],
    "primary_light": COLORES_POSITIVA["verde_claro"],
    "secondary": COLORES_POSITIVA["azul_oscuro"],
    "secondary_medium": COLORES_POSITIVA["azul_medio"],
    "secondary_light": COLORES_POSITIVA["azul_claro"],
    "accent": COLORES_POSITIVA["naranja"],
    "warning": COLORES_POSITIVA["amarillo"],
    "danger": COLORES_POSITIVA["rojo"],
    "success": COLORES_POSITIVA["exito"],
    "info": COLORES_POSITIVA["info"],
    "white": COLORES_POSITIVA["blanco"],
    "bg": COLORES_POSITIVA["gris_claro"],
    "text_muted": COLORES_POSITIVA["gris_medio"],
    "text": COLORES_POSITIVA["gris_oscuro"],
    "sidebar_bg": COLORES_POSITIVA["azul_oscuro"],
    "sidebar_text": COLORES_POSITIVA["blanco"],
}

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN SFTP GOANYWHERE
# ══════════════════════════════════════════════════════════════════════════════

SFTP_CONFIG = {
    "host": "mft.positiva.gov.co",
    "port": 2243,
    "username": "G_medica",
    "password": "Uhnbru0sgnpit]",
    "timeout": 30,
    "carpeta_principal": "R.A-ABASTECIMIENTO RED ASISTENCIAL"
}

# ══════════════════════════════════════════════════════════════════════════════
# MENÚ DE NAVEGACIÓN
# ══════════════════════════════════════════════════════════════════════════════

MENU_ITEMS = [
    {
        "name": "Dashboard",
        "icon": "layout-dashboard",
        "path": "/",
        "description": "Panel principal con estadísticas"
    },
    {
        "name": "Consolidador T25",
        "icon": "settings-2",
        "path": "/consolidador",
        "description": "Herramienta de consolidación de tarifas"
    },
    {
        "name": "Explorador FTP",
        "icon": "folder-open",
        "path": "/explorador",
        "description": "Navegador de archivos GoAnywhere"
    },
    {
        "name": "Consulta de Datos",
        "icon": "search",
        "path": "/consulta",
        "description": "Búsqueda en base de datos"
    },
    {
        "name": "Mapa de Contratos",
        "icon": "map-pin",
        "path": "/mapa",
        "description": "Visualización geográfica"
    },
    {
        "name": "Configuración",
        "icon": "settings",
        "path": "/configuracion",
        "description": "Ajustes del sistema"
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# TIPOS DE ALERTAS
# ══════════════════════════════════════════════════════════════════════════════

TIPOS_ALERTA = {
    "SIN_ANEXO1": {
        "nombre": "Sin Anexo 1",
        "prioridad": 1,
        "color": COLORES_POSITIVA["rojo"],
        "icono": "file-x",
        "descripcion": "No se encontró archivo de tarifas"
    },
    "TIMEOUT": {
        "nombre": "Timeout",
        "prioridad": 2,
        "color": COLORES_POSITIVA["naranja"],
        "icono": "clock",
        "descripcion": "Conexión agotada al servidor"
    },
    "FORMATO_NO_POSITIVA": {
        "nombre": "Formato No Estándar",
        "prioridad": 3,
        "color": COLORES_POSITIVA["amarillo"],
        "icono": "file-warning",
        "descripcion": "Archivo con formato no estándar POSITIVA"
    },
    "SIN_SERVICIOS": {
        "nombre": "Sin Servicios",
        "prioridad": 2,
        "color": COLORES_POSITIVA["naranja"],
        "icono": "list-x",
        "descripcion": "No se encontraron servicios válidos"
    },
    "ERROR_LECTURA": {
        "nombre": "Error de Lectura",
        "prioridad": 1,
        "color": COLORES_POSITIVA["rojo"],
        "icono": "file-x-2",
        "descripcion": "Error al leer el archivo"
    },
    "SOLO_PAQUETES": {
        "nombre": "Solo Paquetes",
        "prioridad": 3,
        "color": COLORES_POSITIVA["amarillo"],
        "icono": "package",
        "descripcion": "Solo contiene paquetes, no servicios individuales"
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# MANUALES TARIFARIOS
# ══════════════════════════════════════════════════════════════════════════════

MANUALES_TARIFARIOS = [
    "SOAT",
    "ISS 2001",
    "ISS 2004",
    "ISS + 25%",
    "ISS + 30%",
    "PROPIO",
    "TARIFA PLENA",
    "PACTADO",
]

# ══════════════════════════════════════════════════════════════════════════════
# CATEGORÍAS DE CONTRATOS
# ══════════════════════════════════════════════════════════════════════════════

CATEGORIAS_CONTRATO = [
    "Cuentas médicas",
    "Cuentas médicas Ambulancias",
    "Cuentas médicas Apoyo Diagnóstico",
    "Cuentas médicas Hospitalización",
    "Cuentas médicas Urgencias",
    "Rehabilitación",
    "Farmacia",
    "Otro",
]

# ══════════════════════════════════════════════════════════════════════════════
# ESTADOS DE EJECUCIÓN
# ══════════════════════════════════════════════════════════════════════════════

ESTADOS_EJECUCION = {
    "PENDIENTE": {"color": COLORES_POSITIVA["gris_medio"], "icono": "clock"},
    "EN_PROCESO": {"color": COLORES_POSITIVA["info"], "icono": "loader"},
    "COMPLETADO": {"color": COLORES_POSITIVA["exito"], "icono": "check-circle"},
    "ERROR": {"color": COLORES_POSITIVA["rojo"], "icono": "x-circle"},
    "CANCELADO": {"color": COLORES_POSITIVA["amarillo"], "icono": "ban"},
}

# ══════════════════════════════════════════════════════════════════════════════
# COORDENADAS DE MUNICIPIOS DE COLOMBIA
# ══════════════════════════════════════════════════════════════════════════════

COORDENADAS_MUNICIPIOS = {
    # === CAPITALES DE DEPARTAMENTO ===
    "LETICIA": (-4.2153, -69.9406),
    "MEDELLIN": (6.2476, -75.5658),
    "ARAUCA": (7.0847, -70.7617),
    "BARRANQUILLA": (10.9685, -74.7813),
    "BOGOTA": (4.7110, -74.0721),
    "BOGOTA, D.C.": (4.7110, -74.0721),
    "CARTAGENA": (10.3997, -75.5144),
    "TUNJA": (5.5353, -73.3678),
    "MANIZALES": (5.0703, -75.5138),
    "FLORENCIA": (1.6144, -75.6062),
    "YOPAL": (5.3378, -72.3959),
    "POPAYAN": (2.4419, -76.6061),
    "VALLEDUPAR": (10.4631, -73.2532),
    "QUIBDO": (5.6947, -76.6611),
    "MONTERIA": (8.7575, -75.8856),
    "INIRIDA": (3.8653, -67.9239),
    "SAN JOSE DEL GUAVIARE": (2.5669, -72.6406),
    "NEIVA": (2.9273, -75.2819),
    "RIOHACHA": (11.5444, -72.9072),
    "SANTA MARTA": (11.2408, -74.1990),
    "VILLAVICENCIO": (4.1420, -73.6266),
    "PASTO": (1.2136, -77.2811),
    "CUCUTA": (7.8939, -72.5078),
    "MOCOA": (1.1492, -76.6519),
    "ARMENIA": (4.5339, -75.6811),
    "PEREIRA": (4.8087, -75.6906),
    "SAN ANDRES": (12.5847, -81.7006),
    "BUCARAMANGA": (7.1193, -73.1227),
    "SINCELEJO": (9.3047, -75.3978),
    "IBAGUE": (4.4389, -75.2322),
    "CALI": (3.4516, -76.5320),
    "MITU": (1.2531, -70.2339),
    "PUERTO CARRENO": (6.1892, -67.4858),

    # === CIUDADES INTERMEDIAS ===
    "ENVIGADO": (6.1711, -75.5867),
    "ITAGUI": (6.1847, -75.5994),
    "BELLO": (6.3378, -75.5556),
    "RIONEGRO": (6.1553, -75.3744),
    "APARTADO": (7.8828, -76.6258),
    "CAUCASIA": (7.9847, -75.1989),
    "TURBO": (8.0936, -76.7286),
    "SOLEDAD": (10.9181, -74.7644),
    "MALAMBO": (10.8578, -74.7706),
    "SABANALARGA": (10.6342, -74.9247),
    "MAGANGUE": (9.2419, -74.7536),
    "TURBACO": (10.3286, -75.4267),
    "DUITAMA": (5.8267, -73.0331),
    "SOGAMOSO": (5.7142, -72.9336),
    "CHIQUINQUIRA": (5.6181, -73.8194),
    "LA DORADA": (5.4528, -74.6631),
    "CHINCHINA": (4.9833, -75.6058),
    "AGUAZUL": (5.1728, -72.5472),
    "VILLANUEVA": (4.9528, -73.0336),
    "SANTANDER DE QUILICHAO": (3.0092, -76.4833),
    "PUERTO TEJADA": (3.2317, -76.4192),
    "AGUACHICA": (8.3097, -73.6175),
    "CODAZZI": (10.0383, -73.2381),
    "ISTMINA": (5.1611, -76.6822),
    "CERETE": (8.8850, -75.7947),
    "LORICA": (9.2381, -75.8133),
    "SOACHA": (4.5867, -74.2167),
    "FACATATIVA": (4.8133, -74.3542),
    "ZIPAQUIRA": (5.0222, -74.0081),
    "CHIA": (4.8667, -74.0500),
    "FUSAGASUGA": (4.3433, -74.3642),
    "GIRARDOT": (4.3017, -74.8017),
    "PITALITO": (1.8525, -76.0472),
    "GARZON": (2.1961, -75.6261),
    "LA PLATA": (2.3917, -75.8917),
    "MAICAO": (11.3825, -72.2419),
    "CIENAGA": (11.0058, -74.2492),
    "FUNDACION": (10.5208, -74.1850),
    "ACACIAS": (3.9878, -73.7589),
    "GRANADA": (3.5447, -73.7050),
    "TUMACO": (1.7986, -78.7644),
    "IPIALES": (0.8275, -77.6447),
    "OCANA": (8.2378, -73.3522),
    "PAMPLONA": (7.3761, -72.6481),
    "VILLA DEL ROSARIO": (7.8333, -72.4711),
    "PUERTO ASIS": (0.5086, -76.5011),
    "CALARCA": (4.5247, -75.6394),
    "MONTENEGRO": (4.5667, -75.7500),
    "DOSQUEBRADAS": (4.8333, -75.6667),
    "LA VIRGINIA": (4.8972, -75.8822),
    "FLORIDABLANCA": (7.0647, -73.0897),
    "GIRON": (7.0681, -73.1697),
    "PIEDECUESTA": (6.9886, -73.0519),
    "BARRANCABERMEJA": (7.0653, -73.8547),
    "SAN GIL": (6.5556, -73.1361),
    "COROZAL": (9.3167, -75.2833),
    "SAN MARCOS": (8.6583, -75.1347),
    "ESPINAL": (4.1500, -74.8833),
    "MELGAR": (4.2056, -74.6461),
    "PALMIRA": (3.5394, -76.3036),
    "BUENAVENTURA": (3.8833, -77.0167),
    "TULUA": (4.0847, -76.2003),
    "CARTAGO": (4.7461, -75.9117),
    "BUGA": (3.9008, -76.3031),
    "YUMBO": (3.5847, -76.4947),
    "JAMUNDI": (3.2608, -76.5394),
}


def obtener_coordenadas(ciudad: str) -> tuple:
    """
    Busca las coordenadas de una ciudad, normalizando el nombre.
    Retorna (lat, lon) o None si no se encuentra.
    """
    import unicodedata

    def normalizar(texto):
        texto = unicodedata.normalize('NFD', texto)
        texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
        return texto.upper().strip()

    ciudad_norm = normalizar(ciudad)

    # Buscar directamente
    if ciudad_norm in COORDENADAS_MUNICIPIOS:
        return COORDENADAS_MUNICIPIOS[ciudad_norm]

    # Buscar sin sufijos comunes
    for nombre, coords in COORDENADAS_MUNICIPIOS.items():
        if normalizar(nombre) == ciudad_norm:
            return coords
        if ciudad_norm in normalizar(nombre) or normalizar(nombre) in ciudad_norm:
            return coords

    return None
