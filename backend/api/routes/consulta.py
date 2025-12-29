from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from typing import Optional

from models.database import get_db
from models.servicio import Servicio

router = APIRouter()

@router.get("/search")
async def search_servicios(
    q: str = Query(..., min_length=2, description="Término de búsqueda"),
    departamento: Optional[str] = None,
    ano: Optional[int] = None,
    manual: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Búsqueda de servicios con filtros."""

    query = db.query(Servicio)

    # Aplicar filtros
    if q:
        query = query.filter(
            (Servicio.codigo_cups.contains(q)) |
            (Servicio.descripcion_cups.ilike(f"%{q}%")) |
            (Servicio.contrato.contains(q)) |
            (Servicio.nombre_proveedor.ilike(f"%{q}%"))
        )

    if departamento:
        query = query.filter(Servicio.departamento == departamento)

    if manual:
        query = query.filter(Servicio.manual_tarifario == manual)

    total = query.count()
    servicios = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "resultados": [
            {
                "id": s.id,
                "contrato": s.contrato,
                "proveedor": s.nombre_proveedor,
                "cups": s.codigo_cups,
                "descripcion": s.descripcion_cups,
                "tarifa": s.tarifa_unitaria,
                "manual": s.manual_tarifario,
                "departamento": s.departamento,
            }
            for s in servicios
        ],
        "total": total,
        "pagina": page,
        "total_paginas": (total + limit - 1) // limit,
    }

@router.get("/sugerencias")
async def get_sugerencias(
    q: str = Query(..., min_length=2),
    limit: int = Query(10, ge=1, le=20)
):
    """Autocompletado para búsqueda."""

    # Datos de ejemplo
    sugerencias = [
        "890201 - Consulta medicina general",
        "890301 - Consulta especialista",
        "890401 - Consulta subespecialista",
        "890501 - Consulta urgencias",
    ]

    return [s for s in sugerencias if q.lower() in s.lower()][:limit]

@router.get("/detalle/{servicio_id}")
async def get_detalle_servicio(servicio_id: int, db: Session = Depends(get_db)):
    """Obtiene el detalle completo de un servicio."""

    servicio = db.query(Servicio).filter(Servicio.id == servicio_id).first()

    if not servicio:
        return {"error": "Servicio no encontrado"}

    return {
        "id": servicio.id,
        "contrato": {
            "numero": servicio.contrato,
            "proveedor": servicio.nombre_proveedor,
            "nit": servicio.nit_proveedor,
            "departamento": servicio.departamento,
            "municipio": servicio.municipio,
        },
        "servicio": {
            "cups": servicio.codigo_cups,
            "descripcion": servicio.descripcion_cups,
            "tarifa": servicio.tarifa_unitaria,
            "manual": servicio.manual_tarifario,
            "porcentaje": servicio.porcentaje_manual,
        },
        "origen": {
            "tipo": servicio.origen_tarifa,
            "otrosi": servicio.numero_otrosi,
            "vigencia_inicio": servicio.fecha_vigencia_inicio,
            "vigencia_fin": servicio.fecha_vigencia_fin,
        },
        "fecha_procesamiento": servicio.fecha_procesamiento,
    }

@router.get("/filtros")
async def get_filtros_disponibles(db: Session = Depends(get_db)):
    """Obtiene los valores disponibles para filtros."""

    return {
        "departamentos": [
            "BOGOTA", "ANTIOQUIA", "SANTANDER", "ATLANTICO",
            "VALLE DEL CAUCA", "CUNDINAMARCA", "BOLIVAR"
        ],
        "manuales": ["SOAT", "ISS", "PROPIO"],
        "anos": [2023, 2024, 2025],
        "categorias": [
            "CUENTAS MEDICAS",
            "AMBULANCIAS",
            "SERVICIOS ESPECIALES"
        ]
    }
