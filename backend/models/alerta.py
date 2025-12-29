from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from .database import Base

class Alerta(Base):
    __tablename__ = "alertas"

    id = Column(Integer, primary_key=True, index=True)

    tipo = Column(String(50), index=True)  # SIN_ANEXO1, FORMATO_INVALIDO, TIMEOUT, etc.
    prioridad = Column(Integer, default=3)  # 1=CRÍTICA, 2=ALTA, 3=MEDIA, 4=BAJA
    mensaje = Column(Text)

    contrato = Column(String(50), index=True)
    archivo = Column(String(255), nullable=True)
    sugerencia = Column(Text, nullable=True)

    # Auditoría
    fecha_creacion = Column(DateTime, server_default=func.now())
    id_ejecucion = Column(Integer, index=True)

    # Estado
    resuelta = Column(Boolean, default=False)
    fecha_resolucion = Column(DateTime, nullable=True)
    comentario_resolucion = Column(Text, nullable=True)
