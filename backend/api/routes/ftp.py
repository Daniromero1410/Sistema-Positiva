from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import os

router = APIRouter()

# Configuración SFTP (de variables de entorno)
SFTP_CONFIG = {
    "host": os.getenv("SFTP_HOST", "mft.positiva.gov.co"),
    "port": int(os.getenv("SFTP_PORT", 2243)),
    "username": os.getenv("SFTP_USER", "G_medica"),
    "password": os.getenv("SFTP_PASSWORD", ""),
}

@router.get("/status")
async def get_status():
    """Verifica el estado de la conexión SFTP."""
    # Aquí iría la lógica real de conexión
    return {
        "conectado": True,
        "host": SFTP_CONFIG["host"],
        "ultimo_acceso": "2025-12-29T10:30:00"
    }

@router.get("/browse")
async def browse_ftp(
    path: str = Query("/", description="Ruta a explorar"),
    db = None
):
    """Navega por el servidor SFTP y lista archivos/carpetas."""

    # Datos de ejemplo - aquí iría la conexión real SFTP
    if path == "/" or path == "":
        return {
            "ruta_actual": "/R.A-ABASTECIMIENTO RED ASISTENCIAL",
            "carpetas": [
                {"nombre": "0123-2025", "tipo": "carpeta", "fecha_modificacion": "2025-12-20"},
                {"nombre": "0124-2025", "tipo": "carpeta", "fecha_modificacion": "2025-12-18"},
                {"nombre": "0125-2025", "tipo": "carpeta", "fecha_modificacion": "2025-12-15"},
            ],
            "archivos": []
        }

    # Simulación de contenido de carpeta
    return {
        "ruta_actual": path,
        "carpetas": [
            {"nombre": "ACTAS", "tipo": "carpeta"},
            {"nombre": "TARIFAS", "tipo": "carpeta"},
            {"nombre": "OTROSIES", "tipo": "carpeta"},
        ],
        "archivos": [
            {"nombre": "ANEXO_1.xlsx", "tamano": "2.3 MB", "fecha": "2025-12-15"},
            {"nombre": "CONTRATO_INICIAL.pdf", "tamano": "1.5 MB", "fecha": "2025-01-10"},
        ]
    }

@router.get("/preview")
async def preview_file(
    path: str = Query(..., description="Ruta del archivo"),
    hoja: Optional[str] = Query(None, description="Nombre de la hoja Excel")
):
    """Vista previa de un archivo Excel."""

    # Datos de ejemplo
    return {
        "archivo": path,
        "hojas": ["TARIFAS DE SERVICIOS", "PAQUETES", "MEDICAMENTOS"],
        "hoja_actual": hoja or "TARIFAS DE SERVICIOS",
        "total_filas": 1234,
        "columnas": ["CUPS", "DESCRIPCION", "TARIFA", "MANUAL", "PORCENTAJE"],
        "datos": [
            {"CUPS": "890201", "DESCRIPCION": "Consulta medicina general", "TARIFA": 45000, "MANUAL": "SOAT", "PORCENTAJE": 100},
            {"CUPS": "890301", "DESCRIPCION": "Consulta especialista", "TARIFA": 65000, "MANUAL": "SOAT", "PORCENTAJE": 100},
            {"CUPS": "890401", "DESCRIPCION": "Consulta subespecialista", "TARIFA": 85000, "MANUAL": "ISS", "PORCENTAJE": 125},
        ]
    }

@router.post("/download")
async def download_file(path: str):
    """Descarga un archivo del servidor SFTP."""
    # Aquí iría la lógica de descarga real
    return {"success": True, "mensaje": f"Archivo {path} descargado"}
