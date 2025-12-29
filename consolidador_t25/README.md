# Consolidador T25 - POSITIVA

Sistema de gestión y consolidación de tarifas médicas para **POSITIVA Compañía de Seguros S.A.**

## Descripción

Esta aplicación web permite consolidar y gestionar las tarifas médicas de los contratos de POSITIVA, extrayendo información de archivos Excel almacenados en el servidor GoAnywhere (SFTP).

## Tecnologías

- **Framework:** [Reflex](https://reflex.dev/) (Python)
- **Base de Datos:** PostgreSQL
- **Mapas:** MapLibre GL JS + Deck.gl
- **Gráficos:** Recharts
- **Estilos:** Tailwind CSS

## Características

### Dashboard
- Estadísticas en tiempo real
- Gráficos de servicios por mes
- Distribución por departamento
- Historial de ejecuciones

### Consolidador T25
- Carga de maestra de contratos (Excel)
- Configuración de modos de ejecución
- Progreso en tiempo real
- Descarga de archivos generados

### Explorador FTP
- Navegación de archivos en GoAnywhere
- Vista previa de archivos Excel
- Descarga individual y múltiple

### Consulta de Datos
- Búsqueda inteligente (fuzzy search)
- Filtros avanzados
- Exportación a Excel

### Mapa de Contratos
- Visualización 3D con columnas
- Filtros por año y departamento
- Tooltip interactivo

### Configuración
- Conexión SFTP
- Base de datos
- Parámetros de procesamiento
- Notificaciones

## Instalación

### Requisitos previos

- Python 3.9+
- PostgreSQL 13+
- Node.js 18+ (para Reflex)

### Pasos

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-repo/consolidador-t25.git
cd consolidador-t25
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con las credenciales correctas
```

5. **Crear base de datos**
```bash
createdb consolidador_t25
```

6. **Inicializar Reflex**
```bash
reflex init
reflex db migrate
```

7. **Ejecutar en desarrollo**
```bash
reflex run
```

La aplicación estará disponible en `http://localhost:3000`

## Estructura del Proyecto

```
consolidador_t25/
├── consolidador_t25/
│   ├── __init__.py
│   ├── consolidador_t25.py     # Aplicación principal
│   ├── constants.py            # Constantes y configuración
│   │
│   ├── core/                   # Lógica de negocio
│   │   ├── consolidador_engine.py
│   │   ├── sftp_client.py
│   │   └── excel_exporter.py
│   │
│   ├── models/                 # Modelos de BD
│   │   ├── servicio.py
│   │   ├── contrato.py
│   │   ├── alerta.py
│   │   └── ejecucion.py
│   │
│   ├── pages/                  # Páginas de la app
│   │   ├── dashboard.py
│   │   ├── consolidador.py
│   │   ├── explorador_ftp.py
│   │   ├── consulta_datos.py
│   │   ├── mapa_contratos.py
│   │   └── configuracion.py
│   │
│   ├── components/             # Componentes UI
│   │   ├── sidebar.py
│   │   ├── navbar.py
│   │   ├── stat_card.py
│   │   └── ...
│   │
│   └── state/                  # Estados globales
│       ├── app_state.py
│       ├── consolidador_state.py
│       └── ...
│
├── assets/
│   ├── logo_positiva.svg
│   └── styles.css
│
├── rxconfig.py
├── requirements.txt
├── .env
└── README.md
```

## Paleta de Colores

| Color | Hex | Uso |
|-------|-----|-----|
| Verde Principal | `#00A651` | Botones primarios, acentos |
| Verde Oscuro | `#008C45` | Hover, estados activos |
| Verde Claro | `#E8F5E9` | Fondos suaves |
| Azul Oscuro | `#1A365D` | Sidebar, textos |
| Naranja | `#F7941D` | Alertas, highlights |

## API

### Modelos de Datos

#### Servicio
```python
class Servicio:
    contrato: str
    nit_proveedor: str
    codigo_cups: str
    descripcion_cups: str
    tarifa_unitaria: float
    manual_tarifario: str
```

#### Contrato
```python
class Contrato:
    numero_contrato: str
    ano: int
    nit: str
    razon_social: str
    departamento: str
    municipio: str
```

## Desarrollo

### Ejecutar tests
```bash
pytest
```

### Formatear código
```bash
black .
isort .
```

### Construir para producción
```bash
reflex export
```

## Licencia

Propiedad de POSITIVA Compañía de Seguros S.A. Todos los derechos reservados.

## Contacto

- **Área:** Gerencia Médica
- **Email:** gerencia.medica@positiva.gov.co
