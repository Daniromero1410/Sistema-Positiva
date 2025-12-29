"""
Modelo Usuario - Usuarios del sistema (opcional).
"""
import reflex as rx
from sqlmodel import Field
from typing import Optional
from datetime import datetime


class Usuario(rx.Model, table=True):
    """Usuarios del sistema."""

    __tablename__ = "usuarios"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Identificación
    username: str = Field(unique=True, index=True, max_length=50)
    email: str = Field(unique=True, max_length=100)
    nombre_completo: str = Field(max_length=200)

    # Autenticación (hash de contraseña)
    password_hash: str = Field(max_length=255)

    # Rol y permisos
    rol: str = Field(default="usuario", max_length=20)  # admin, usuario, lectura
    activo: bool = Field(default=True)

    # Auditoría
    fecha_creacion: datetime = Field(default_factory=datetime.now)
    ultimo_acceso: Optional[datetime] = Field(default=None)

    class Config:
        """Configuración del modelo."""
        arbitrary_types_allowed = True
