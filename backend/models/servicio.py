from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Date, Text
from sqlalchemy.sql import func
from .database import Base

class Servicio(Base):
    __tablename__ = "servicios"

    id = Column(Integer, primary_key=True, index=True)

    # Identificación del contrato
    contrato = Column(String(50), index=True, nullable=False)
    nit_proveedor = Column(String(20), index=True)
    nombre_proveedor = Column(String(255))

    # Ubicación
    departamento = Column(String(100), index=True)
    municipio = Column(String(100), index=True)
    codigo_habilitacion = Column(String(50))

    # Servicio médico
    codigo_cups = Column(String(20), index=True, nullable=False)
    codigo_homologo = Column(String(20), nullable=True)
    descripcion_cups = Column(Text)

    # Tarifa
    tarifa_unitaria = Column(Float, default=0.0)
    manual_tarifario = Column(String(50))  # SOAT, ISS, PROPIO
    porcentaje_manual = Column(Float, nullable=True)
    observaciones = Column(Text, nullable=True)

    # Origen de la tarifa
    origen_tarifa = Column(String(50))  # Inicial, Otrosí, Acta
    numero_otrosi = Column(Integer, nullable=True)
    fecha_vigencia_inicio = Column(Date, nullable=True)
    fecha_vigencia_fin = Column(Date, nullable=True)

    # Auditoría
    fecha_procesamiento = Column(DateTime, server_default=func.now())
    id_ejecucion = Column(Integer, ForeignKey("ejecuciones.id"))
