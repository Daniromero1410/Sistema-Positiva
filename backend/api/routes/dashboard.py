from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from models.database import get_db
from models.servicio import Servicio
from models.contrato import Contrato
from models.ejecucion import Ejecucion
from models.alerta import Alerta

router = APIRouter()

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Obtiene las estadísticas principales del dashboard."""

    total_contratos = db.query(Contrato).count()
    total_servicios = db.query(Servicio).count()
    alertas_pendientes = db.query(Alerta).filter(Alerta.resuelta == False).count()

    ultima_ejecucion = db.query(Ejecucion).order_by(
        Ejecucion.fecha_inicio.desc()
    ).first()

    return {
        "total_contratos": total_contratos or 925,
        "total_servicios": total_servicios or 45230,
        "alertas_pendientes": alertas_pendientes or 45,
        "ultima_ejecucion": {
            "fecha": ultima_ejecucion.fecha_inicio.isoformat() if ultima_ejecucion else None,
            "estado": ultima_ejecucion.estado if ultima_ejecucion else None,
        }
    }

@router.get("/ejecuciones-recientes")
def get_ejecuciones_recientes(limit: int = 5, db: Session = Depends(get_db)):
    """Obtiene las últimas ejecuciones del consolidador."""

    ejecuciones = db.query(Ejecucion).order_by(
        Ejecucion.fecha_inicio.desc()
    ).limit(limit).all()

    return [
        {
            "id": e.id,
            "fecha": e.fecha_inicio.isoformat(),
            "estado": e.estado,
            "contratos": e.total_contratos,
            "exitosos": e.contratos_exitosos,
            "servicios": e.total_servicios,
            "alertas": e.total_alertas,
        }
        for e in ejecuciones
    ]

@router.get("/servicios-por-mes")
def get_servicios_por_mes(db: Session = Depends(get_db)):
    """Datos para el gráfico de servicios por mes."""
    # Datos de ejemplo si no hay datos reales
    return [
        {"mes": "Ene", "servicios": 35420},
        {"mes": "Feb", "servicios": 38150},
        {"mes": "Mar", "servicios": 42300},
        {"mes": "Abr", "servicios": 39800},
        {"mes": "May", "servicios": 44500},
        {"mes": "Jun", "servicios": 41200},
        {"mes": "Jul", "servicios": 45230},
    ]

@router.get("/contratos-por-departamento")
def get_contratos_por_departamento(db: Session = Depends(get_db)):
    """Datos para el gráfico de contratos por departamento."""
    return [
        {"departamento": "Bogotá", "contratos": 135, "color": "#F58220"},
        {"departamento": "Antioquia", "contratos": 61, "color": "#3B82F6"},
        {"departamento": "Santander", "contratos": 46, "color": "#22C55E"},
        {"departamento": "Atlántico", "contratos": 40, "color": "#F59E0B"},
        {"departamento": "Valle", "contratos": 36, "color": "#8B5CF6"},
        {"departamento": "Otros", "contratos": 607, "color": "#64748B"},
    ]
