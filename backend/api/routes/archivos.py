from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/download/{ejecucion_id}/{tipo}")
async def download_archivo(ejecucion_id: int, tipo: str):
    """Descarga un archivo generado por una ejecución."""

    # Mapeo de tipos a rutas de archivos
    archivos_map = {
        "ml_limpio": f"outputs/CONSOLIDADO_ML_LIMPIO_{ejecucion_id}.xlsx",
        "consolidado": f"outputs/CONSOLIDADO_{ejecucion_id}.xlsx",
        "alertas": f"outputs/ALERTAS_{ejecucion_id}.xlsx",
        "resumen": f"outputs/RESUMEN_{ejecucion_id}.xlsx",
    }

    if tipo not in archivos_map:
        raise HTTPException(400, "Tipo de archivo inválido")

    archivo_path = archivos_map[tipo]

    if not os.path.exists(archivo_path):
        # Por ahora, devolver un mensaje
        raise HTTPException(404, f"Archivo no encontrado: {archivo_path}")

    return FileResponse(
        archivo_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=os.path.basename(archivo_path)
    )

@router.get("/list")
async def listar_archivos():
    """Lista todos los archivos disponibles para descarga."""

    archivos = []

    if os.path.exists("outputs"):
        for filename in os.listdir("outputs"):
            if filename.endswith(('.xlsx', '.xls', '.csv')):
                filepath = os.path.join("outputs", filename)
                size = os.path.getsize(filepath)
                archivos.append({
                    "nombre": filename,
                    "tamano": f"{size / 1024 / 1024:.1f} MB",
                    "ruta": f"/api/archivos/download/file/{filename}"
                })

    return archivos

@router.get("/download/file/{filename}")
async def download_file_by_name(filename: str):
    """Descarga un archivo por nombre."""

    archivo_path = os.path.join("outputs", filename)

    if not os.path.exists(archivo_path):
        raise HTTPException(404, "Archivo no encontrado")

    return FileResponse(
        archivo_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=filename
    )
