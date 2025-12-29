"""
Modelo Ejecución - Historial de ejecuciones del consolidador.
"""
import reflex as rx
from sqlmodel import Field
from typing import Optional
from datetime import datetime


class Ejecucion(rx.Model, table=True):
    """Historial de ejecuciones del consolidador."""

    __tablename__ = "ejecuciones"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Tiempos
    fecha_inicio: datetime = Field(default_factory=datetime.now)
    fecha_fin: Optional[datetime] = Field(default=None)
    estado: str = Field(default="EN_PROCESO", max_length=20)  # EN_PROCESO, COMPLETADO, ERROR, CANCELADO

    # Configuración de la ejecución
    modo: str = Field(max_length=20)  # COMPLETO, POR_ANO, ESPECIFICO
    ano_filtro: Optional[int] = Field(default=None)
    contratos_filtro: Optional[str] = Field(default=None)  # JSON list

    # Resultados
    total_contratos: int = Field(default=0)
    contratos_exitosos: int = Field(default=0)
    contratos_fallidos: int = Field(default=0)
    total_servicios: int = Field(default=0)
    total_alertas: int = Field(default=0)

    # Progreso
    contrato_actual: Optional[str] = Field(default=None, max_length=50)
    progreso_porcentaje: float = Field(default=0.0)
    log_mensajes: Optional[str] = Field(default=None)  # JSON array de mensajes

    # Archivos generados
    archivo_consolidado: Optional[str] = Field(default=None, max_length=255)
    archivo_ml_limpio: Optional[str] = Field(default=None, max_length=255)
    archivo_alertas: Optional[str] = Field(default=None, max_length=255)
    archivo_resumen: Optional[str] = Field(default=None, max_length=255)
    archivo_no_positiva: Optional[str] = Field(default=None, max_length=255)

    # Usuario
    usuario: Optional[str] = Field(default=None, max_length=100)

    # Mensaje de error (si aplica)
    mensaje_error: Optional[str] = Field(default=None, max_length=1000)

    class Config:
        """Configuración del modelo."""
        arbitrary_types_allowed = True
