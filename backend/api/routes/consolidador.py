from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
import os
import json

from models.database import get_db
from models.ejecucion import Ejecucion

router = APIRouter()

class ConsolidadorConfig(BaseModel):
    modo: str  # "completo", "por_ano", "especifico"
    ano: Optional[int] = None
    contratos: Optional[list[str]] = None
    guardar_en_bd: bool = True
    exportar_alertas: bool = True

class ConsolidadorResponse(BaseModel):
    ejecucion_id: int
    status: str
    message: str

@router.post("/upload-maestra")
async def upload_maestra(file: UploadFile = File(...)):
    """Sube y procesa la maestra de contratos."""

    # Validar extensión
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(400, "El archivo debe ser Excel (.xlsx o .xls)")

    # Guardar archivo
    upload_path = f"uploads/{file.filename}"
    contents = await file.read()

    with open(upload_path, "wb") as f:
        f.write(contents)

    # Aquí procesarías el Excel para obtener información
    # Por ahora retornamos datos de ejemplo
    return {
        "success": True,
        "nombre": file.filename,
        "tamano": f"{len(contents) / 1024 / 1024:.1f} MB",
        "ruta": upload_path,
        "resumen": {
            "total_contratos": 925,
            "por_ano": {
                "2024": 456,
                "2025": 469
            },
            "columnas_detectadas": [
                "CONTRATO", "AÑO", "NIT", "RAZON SOCIAL",
                "DEPARTAMENTO", "MUNICIPIO", "CATEGORIA"
            ]
        }
    }

@router.post("/iniciar", response_model=ConsolidadorResponse)
async def iniciar_consolidacion(
    config: ConsolidadorConfig,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Inicia el proceso de consolidación."""

    # Crear registro de ejecución
    ejecucion = Ejecucion(
        modo=config.modo,
        ano_filtro=config.ano,
        contratos_filtro=json.dumps(config.contratos) if config.contratos else None,
        estado="EN_PROCESO",
        total_contratos=150 if config.modo == "completo" else len(config.contratos or [])
    )
    db.add(ejecucion)
    db.commit()
    db.refresh(ejecucion)

    # Agregar tarea en background
    # background_tasks.add_task(ejecutar_consolidacion, ejecucion.id, config)

    return ConsolidadorResponse(
        ejecucion_id=ejecucion.id,
        status="iniciado",
        message="Consolidación iniciada correctamente"
    )

@router.get("/progreso/{ejecucion_id}")
async def get_progreso(ejecucion_id: int, db: Session = Depends(get_db)):
    """Obtiene el progreso de una ejecución."""

    ejecucion = db.query(Ejecucion).filter(Ejecucion.id == ejecucion_id).first()

    if not ejecucion:
        raise HTTPException(404, "Ejecución no encontrada")

    return {
        "ejecucion_id": ejecucion.id,
        "estado": ejecucion.estado,
        "progreso": ejecucion.progreso_porcentaje,
        "contrato_actual": ejecucion.contrato_actual or "0456-2025",
        "contratos_procesados": ejecucion.contratos_exitosos + ejecucion.contratos_fallidos,
        "total_contratos": ejecucion.total_contratos,
        "servicios_extraidos": ejecucion.total_servicios,
        "alertas_generadas": ejecucion.total_alertas,
    }

@router.get("/resultados/{ejecucion_id}")
async def get_resultados(ejecucion_id: int, db: Session = Depends(get_db)):
    """Obtiene los resultados de una ejecución completada."""

    ejecucion = db.query(Ejecucion).filter(Ejecucion.id == ejecucion_id).first()

    if not ejecucion:
        raise HTTPException(404, "Ejecución no encontrada")

    archivos = []

    if ejecucion.archivo_ml_limpio:
        archivos.append({
            "nombre": "CONSOLIDADO_ML_LIMPIO.xlsx",
            "descripcion": "Datos consolidados con limpieza ML",
            "tamano": "12.5 MB",
            "ruta": f"/api/archivos/download/{ejecucion_id}/ml_limpio",
            "es_principal": True,
        })

    if ejecucion.archivo_consolidado:
        archivos.append({
            "nombre": f"CONSOLIDADO_{ejecucion.ano_filtro or 2025}.xlsx",
            "descripcion": "Datos crudos del GoAnywhere",
            "tamano": "8.2 MB",
            "ruta": f"/api/archivos/download/{ejecucion_id}/consolidado",
            "es_principal": False,
        })

    if ejecucion.archivo_alertas:
        archivos.append({
            "nombre": "ALERTAS.xlsx",
            "descripcion": "Alertas categorizadas",
            "tamano": "245 KB",
            "ruta": f"/api/archivos/download/{ejecucion_id}/alertas",
            "es_principal": False,
        })

    return {
        "ejecucion_id": ejecucion.id,
        "estado": ejecucion.estado,
        "resumen": {
            "total_contratos": ejecucion.total_contratos,
            "exitosos": ejecucion.contratos_exitosos,
            "fallidos": ejecucion.contratos_fallidos,
            "total_servicios": ejecucion.total_servicios,
            "total_alertas": ejecucion.total_alertas,
        },
        "archivos": archivos,
        "duracion": "05:23",  # Calcular de fecha_inicio a fecha_fin
    }

@router.post("/cancelar/{ejecucion_id}")
async def cancelar_ejecucion(ejecucion_id: int, db: Session = Depends(get_db)):
    """Cancela una ejecución en proceso."""

    ejecucion = db.query(Ejecucion).filter(Ejecucion.id == ejecucion_id).first()

    if not ejecucion:
        raise HTTPException(404, "Ejecución no encontrada")

    if ejecucion.estado != "EN_PROCESO":
        raise HTTPException(400, "Solo se pueden cancelar ejecuciones en proceso")

    ejecucion.estado = "CANCELADO"
    db.commit()

    return {"success": True, "message": "Ejecución cancelada"}
