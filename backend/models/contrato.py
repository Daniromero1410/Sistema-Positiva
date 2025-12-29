from sqlalchemy import Column, Integer, String, Float, DateTime, Date
from sqlalchemy.sql import func
from .database import Base

class Contrato(Base):
    __tablename__ = "contratos"

    id = Column(Integer, primary_key=True, index=True)

    numero_contrato = Column(String(50), unique=True, index=True, nullable=False)
    ano = Column(Integer, index=True)
    nit = Column(String(20))
    razon_social = Column(String(255))

    # Ubicación
    departamento = Column(String(100))
    municipio = Column(String(100))
    direccion = Column(String(255), nullable=True)

    # Clasificación
    categoria = Column(String(100))
    tipo_prestador = Column(String(100), nullable=True)

    # Vigencia
    fecha_inicio = Column(Date, nullable=True)
    fecha_fin = Column(Date, nullable=True)
    estado = Column(String(20), default="ACTIVO")

    # Coordenadas para mapa
    latitud = Column(Float, nullable=True)
    longitud = Column(Float, nullable=True)

    # Estadísticas
    total_servicios = Column(Integer, default=0)
    total_alertas = Column(Integer, default=0)

    # Auditoría
    fecha_carga = Column(DateTime, server_default=func.now())
    ultima_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())
