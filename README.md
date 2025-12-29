# 🚀 Sistema Consolidador T25 - POSITIVA

Sistema completo de consolidación de tarifas médicas para POSITIVA Compañía de Seguros S.A.

## 📋 Stack Tecnológico

- **Frontend:** Next.js 14 (App Router) + TypeScript + Tailwind CSS
- **Backend:** FastAPI (Python 3.11+) + SQLAlchemy
- **Base de Datos:** SQLite (desarrollo) / PostgreSQL (producción)
- **Entorno:** Firebase Studio (Google IDX)

## 🎨 Colores POSITIVA

El color principal es **NARANJA** (#F58220):

```typescript
primary: "#F58220"        // Naranja POSITIVA
primaryHover: "#E5721A"   // Naranja oscuro (hover)
secondary: "#1E293B"      // Slate oscuro (sidebar)
```

## 📁 Estructura del Proyecto

```
consolidador-t25/
├── .idx/
│   └── dev.nix                 # Configuración Firebase Studio
│
├── frontend/                    # Next.js 14 App
│   ├── app/                    # Páginas (App Router)
│   │   ├── page.tsx            # Dashboard
│   │   ├── consolidador/       # Consolidador T25
│   │   ├── explorador/         # Explorador FTP
│   │   ├── consulta/           # Consulta de datos
│   │   ├── mapa/               # Mapa de contratos
│   │   └── configuracion/      # Configuración
│   │
│   ├── components/
│   │   ├── ui/                 # Componentes UI (Button, Card, etc.)
│   │   └── layout/             # Sidebar, Navbar, MainLayout
│   │
│   ├── lib/
│   │   ├── api.ts              # Cliente API
│   │   ├── utils.ts            # Utilidades
│   │   └── constants.ts        # Colores, menú, config
│   │
│   └── types/
│       └── index.ts            # TypeScript types
│
├── backend/                     # FastAPI App
│   ├── main.py                 # Entry point
│   ├── config.py               # Configuración
│   │
│   ├── api/routes/             # Rutas de la API
│   │   ├── dashboard.py
│   │   ├── consolidador.py
│   │   ├── ftp.py
│   │   ├── consulta.py
│   │   ├── mapa.py
│   │   └── archivos.py
│   │
│   ├── core/
│   │   └── consolidador_engine.py  # Motor de consolidación
│   │
│   ├── models/                 # Modelos SQLAlchemy
│   │   ├── database.py
│   │   ├── servicio.py
│   │   ├── contrato.py
│   │   ├── ejecucion.py
│   │   └── alerta.py
│   │
│   └── schemas/                # Schemas Pydantic
│
├── uploads/                     # Archivos subidos
├── outputs/                     # Archivos generados
│
└── README.md
```

## 🚀 Instalación y Ejecución

### Opción 1: Firebase Studio (Recomendado)

1. **Abrir en Firebase Studio:**
   - El archivo `.idx/dev.nix` configura automáticamente el entorno
   - Las dependencias se instalan automáticamente al crear el workspace

2. **Ejecutar el proyecto:**

   ```bash
   # Terminal 1 - Backend
   cd backend
   source venv/bin/activate
   uvicorn main:app --reload --host 0.0.0.0 --port 8000

   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

3. **Acceder:**
   - Frontend: `http://localhost:3000`
   - API: `http://localhost:8000/api/docs`

### Opción 2: Instalación Manual

#### Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# Inicializar base de datos
python -c "from models.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Ejecutar servidor
uvicorn main:app --reload
```

#### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.local.example .env.local
# Editar .env.local

# Ejecutar en desarrollo
npm run dev

# Build para producción
npm run build
npm start
```

## 📡 API Endpoints

### Dashboard
- `GET /api/dashboard/stats` - Estadísticas principales
- `GET /api/dashboard/ejecuciones-recientes` - Últimas ejecuciones
- `GET /api/dashboard/servicios-por-mes` - Datos para gráficos
- `GET /api/dashboard/contratos-por-departamento` - Datos para gráficos

### Consolidador
- `POST /api/consolidador/upload-maestra` - Subir maestra de contratos
- `POST /api/consolidador/iniciar` - Iniciar consolidación
- `GET /api/consolidador/progreso/{id}` - Obtener progreso
- `GET /api/consolidador/resultados/{id}` - Obtener resultados
- `POST /api/consolidador/cancelar/{id}` - Cancelar ejecución

### FTP
- `GET /api/ftp/status` - Estado de conexión SFTP
- `GET /api/ftp/browse?path=/` - Navegar carpetas
- `GET /api/ftp/preview?path=...` - Vista previa de archivo
- `POST /api/ftp/download` - Descargar archivo

### Consulta
- `GET /api/consulta/search?q=...` - Buscar servicios
- `GET /api/consulta/sugerencias?q=...` - Autocompletado
- `GET /api/consulta/detalle/{id}` - Detalle de servicio
- `GET /api/consulta/filtros` - Filtros disponibles

### Mapa
- `GET /api/mapa/datos` - Datos para mapa
- `GET /api/mapa/top-ciudades` - Top ciudades
- `GET /api/mapa/departamentos` - Contratos por departamento

### Archivos
- `GET /api/archivos/download/{ejecucion_id}/{tipo}` - Descargar archivo
- `GET /api/archivos/list` - Listar archivos disponibles

## 🗄️ Modelos de Base de Datos

### Servicio
Almacena información de tarifas médicas por servicio:
- Contrato y proveedor
- Código CUPS y descripción
- Tarifa y manual tarifario
- Ubicación geográfica
- Origen de la tarifa (inicial, otrosí, acta)

### Contrato
Información de contratos con proveedores:
- Número de contrato y año
- NIT y razón social
- Ubicación y categoría
- Coordenadas para mapa
- Estadísticas de servicios y alertas

### Ejecucion
Registro de cada ejecución del consolidador:
- Configuración (modo, año, filtros)
- Progreso y estado
- Resultados (contratos procesados, servicios extraídos)
- Archivos generados
- Log detallado

### Alerta
Alertas generadas durante el procesamiento:
- Tipo y prioridad
- Contrato y archivo afectado
- Mensaje y sugerencia
- Estado de resolución

## 🎨 Páginas de la Aplicación

### 1. Dashboard (/)
- Estadísticas principales (contratos, servicios, alertas)
- Gráfico de servicios por mes (Recharts)
- Gráfico de contratos por departamento
- Tabla de últimas ejecuciones

### 2. Consolidador T25 (/consolidador)
- Upload de maestra de contratos (drag & drop)
- Configuración de ejecución (modo, año, filtros)
- Modal de progreso en tiempo real
- Descarga de archivos generados

### 3. Explorador FTP (/explorador)
- Navegación por carpetas del servidor SFTP
- Vista previa de archivos Excel
- Descarga de archivos
- Información de metadata

### 4. Consulta de Datos (/consulta)
- Búsqueda por CUPS, descripción, contrato, proveedor
- Filtros avanzados (departamento, manual, año)
- Tabla paginada de resultados
- Modal de detalle de servicio

### 5. Mapa de Contratos (/mapa)
- Visualización geográfica con MapLibre GL
- Filtros por departamento y año
- Panel de top ciudades
- Estadísticas por región

### 6. Configuración (/configuracion)
- Configuración de conexión SFTP
- Configuración de base de datos
- Parámetros del sistema

## 🔐 Variables de Entorno

### Backend (.env)
```env
DATABASE_URL=sqlite:///./consolidador.db
SFTP_HOST=mft.positiva.gov.co
SFTP_PORT=2243
SFTP_USER=G_medica
SFTP_PASSWORD=your_password_here
SECRET_KEY=your-secret-key-change-in-production
DEBUG=true
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📝 Notas Importantes

1. **Firebase Studio:** El entorno se configura automáticamente con `.idx/dev.nix`
2. **SQLite:** Se usa en desarrollo. Para producción, cambiar a PostgreSQL
3. **SFTP:** Configurar credenciales reales en `.env`
4. **Colores:** El color principal de POSITIVA es NARANJA (#F58220), no verde
5. **Archivos grandes:** El consolidador usa background tasks para procesar grandes volúmenes

## 🛠️ Desarrollo

### Agregar nueva página
1. Crear archivo en `frontend/app/nombre/page.tsx`
2. Usar `MainLayout` como wrapper
3. Actualizar `MENU_ITEMS` en `lib/constants.ts` si es necesario

### Agregar nuevo endpoint
1. Crear ruta en `backend/api/routes/`
2. Registrar en `backend/main.py`
3. Actualizar cliente API en `frontend/lib/api.ts`

### Agregar nuevo modelo
1. Crear modelo en `backend/models/`
2. Crear schema en `backend/schemas/`
3. Crear migración con Alembic (opcional)

## 📊 Tecnologías Adicionales

- **React Query:** Gestión de estado del servidor
- **Zustand:** Gestión de estado local
- **Recharts:** Gráficos y visualizaciones
- **MapLibre GL:** Mapas interactivos
- **Deck.gl:** Capas de datos geoespaciales
- **Lucide React:** Iconos
- **Radix UI:** Componentes accesibles
- **Tailwind CSS:** Estilos utility-first

## 🚧 Próximos Pasos

- [ ] Integrar lógica completa del consolidador_engine.py
- [ ] Implementar autenticación y autorización
- [ ] Agregar tests unitarios y de integración
- [ ] Configurar CI/CD
- [ ] Implementar WebSockets para progreso en tiempo real
- [ ] Optimizar queries de base de datos
- [ ] Agregar paginación en todas las tablas
- [ ] Implementar exportación a diferentes formatos (CSV, PDF)

## 📄 Licencia

© 2025 POSITIVA Compañía de Seguros S.A. - Todos los derechos reservados.

## 👥 Autor

Desarrollado por Daniel Romero para POSITIVA Compañía de Seguros S.A.

---

**Versión:** 1.0.0
**Última actualización:** Diciembre 2025
