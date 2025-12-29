"""
Modelo Alerta - Alertas generadas durante procesamiento.
"""
import reflex as rx
from sqlmodel import Field
from typing import Optional
from datetime import datetime


class Alerta(rx.Model, table=True):
    """Alertas generadas durante procesamiento."""

    __tablename__ = "alertas"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Tipo y prioridad
    tipo: str = Field(index=True, max_length=50)  # SIN_ANEXO1, TIMEOUT, etc.
    prioridad: int = Field(default=3)  # 1=CRITICA, 2=ALTA, 3=MEDIA, 4=BAJA

    # Contenido
    mensaje: str = Field(max_length=1000)
    contrato: str = Field(index=True, max_length=50)
    archivo: Optional[str] = Field(default=None, max_length=255)
    sugerencia: str = Field(max_length=500)

    # Detalles adicionales (JSON)
    detalles: Optional[str] = Field(default=None)  # JSON string para info extra

    # Auditoría
    fecha_creacion: datetime = Field(default_factory=datetime.now)
    id_ejecucion: int = Field(foreign_key="ejecuciones.id")

    # Estado de resolución
    resuelta: bool = Field(default=False)
    fecha_resolucion: Optional[datetime] = Field(default=None)
    resolucion_notas: Optional[str] = Field(default=None, max_length=500)

    class Config:
        """Configuración del modelo."""
        arbitrary_types_allowed = True
