"""
Modelo Contrato - Maestra de contratos.
"""
import reflex as rx
from sqlmodel import Field
from typing import Optional
from datetime import datetime, date


class Contrato(rx.Model, table=True):
    """Contratos de la maestra."""

    __tablename__ = "contratos"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Identificación
    numero_contrato: str = Field(unique=True, index=True, max_length=50)
    ano: int = Field(index=True)
    nit: str = Field(max_length=20)
    razon_social: str = Field(max_length=255)

    # Ubicación
    departamento: str = Field(max_length=100)
    municipio: str = Field(max_length=100)
    direccion: Optional[str] = Field(default=None, max_length=255)

    # Clasificación
    categoria: str = Field(max_length=100)  # Cuentas médicas, Ambulancias, etc.
    tipo_prestador: Optional[str] = Field(default=None, max_length=100)

    # Vigencia
    fecha_inicio: Optional[date] = Field(default=None)
    fecha_fin: Optional[date] = Field(default=None)
    estado: str = Field(default="ACTIVO", max_length=20)

    # Coordenadas para mapa
    latitud: Optional[float] = Field(default=None)
    longitud: Optional[float] = Field(default=None)

    # Estadísticas
    total_servicios: int = Field(default=0)
    total_alertas: int = Field(default=0)

    # Auditoría
    fecha_carga: datetime = Field(default_factory=datetime.now)
    ultima_actualizacion: datetime = Field(default_factory=datetime.now)

    class Config:
        """Configuración del modelo."""
        arbitrary_types_allowed = True
