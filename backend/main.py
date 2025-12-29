from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from api.routes import dashboard, consolidador, ftp, consulta, mapa, archivos
from models.database import engine, Base

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Crear directorios necesarios
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

app = FastAPI(
    title="Consolidador T25 API",
    description="API para el Sistema de Consolidación de Tarifas Médicas - POSITIVA",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS - Permitir requests desde Firebase Studio y localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://*.idx.dev",          # Firebase Studio
        "https://*.web.app",          # Firebase Hosting
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos (outputs)
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

# Registrar rutas
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(consolidador.router, prefix="/api/consolidador", tags=["Consolidador"])
app.include_router(ftp.router, prefix="/api/ftp", tags=["FTP"])
app.include_router(consulta.router, prefix="/api/consulta", tags=["Consulta"])
app.include_router(mapa.router, prefix="/api/mapa", tags=["Mapa"])
app.include_router(archivos.router, prefix="/api/archivos", tags=["Archivos"])

@app.get("/")
def root():
    return {
        "app": "Consolidador T25 API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "message": "Consolidador T25 API funcionando correctamente"
    }
