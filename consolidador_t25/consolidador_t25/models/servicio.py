"""
Modelo Servicio - Datos consolidados del T25.
"""
import reflex as rx
from sqlmodel import Field
from typing import Optional
from datetime import datetime, date
from decimal import Decimal


class Servicio(rx.Model, table=True):
    """Servicios consolidados del T25."""

    __tablename__ = "servicios"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Identificación del contrato
    contrato: str = Field(index=True, max_length=50)
    nit_proveedor: str = Field(index=True, max_length=20)
    nombre_proveedor: str = Field(max_length=255)

    # Ubicación
    departamento: str = Field(index=True, max_length=100)
    municipio: str = Field(index=True, max_length=100)
    codigo_habilitacion: Optional[str] = Field(default=None, max_length=50)

    # Servicio
    codigo_cups: str = Field(index=True, max_length=20)
    codigo_homologo: Optional[str] = Field(default=None, max_length=20)
    descripcion_cups: str = Field(max_length=500)

    # Tarifa
    tarifa_unitaria: float = Field(default=0.0)
    manual_tarifario: str = Field(max_length=50)  # SOAT, ISS, PROPIO
    porcentaje_manual: Optional[float] = Field(default=None)
    observaciones: Optional[str] = Field(default=None, max_length=1000)

    # Metadata del archivo origen
    origen_tarifa: str = Field(max_length=50)  # Inicial, Otrosí, Acta
    numero_otrosi: Optional[int] = Field(default=None)
    fecha_vigencia_inicio: Optional[date] = Field(default=None)
    fecha_vigencia_fin: Optional[date] = Field(default=None)

    # Auditoría
    fecha_procesamiento: datetime = Field(default_factory=datetime.now)
    id_ejecucion: int = Field(foreign_key="ejecuciones.id")

    class Config:
        """Configuración del modelo."""
        arbitrary_types_allowed = True
