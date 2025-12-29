from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from .database import Base

class Ejecucion(Base):
    __tablename__ = "ejecuciones"

    id = Column(Integer, primary_key=True, index=True)

    fecha_inicio = Column(DateTime, server_default=func.now())
    fecha_fin = Column(DateTime, nullable=True)
    estado = Column(String(20), default="EN_PROCESO")  # EN_PROCESO, COMPLETADO, ERROR, CANCELADO

    # Configuración de la ejecución
    modo = Column(String(20))  # completo, por_ano, especifico
    ano_filtro = Column(Integer, nullable=True)
    contratos_filtro = Column(Text, nullable=True)  # JSON con lista de contratos

    # Resultados
    total_contratos = Column(Integer, default=0)
    contratos_exitosos = Column(Integer, default=0)
    contratos_fallidos = Column(Integer, default=0)
    total_servicios = Column(Integer, default=0)
    total_alertas = Column(Integer, default=0)

    # Progreso actual
    contrato_actual = Column(String(50), nullable=True)
    progreso_porcentaje = Column(Integer, default=0)

    # Archivos generados
    archivo_consolidado = Column(String(255), nullable=True)
    archivo_ml_limpio = Column(String(255), nullable=True)
    archivo_alertas = Column(String(255), nullable=True)
    archivo_resumen = Column(String(255), nullable=True)

    # Información adicional
    usuario = Column(String(100), nullable=True)
    mensaje_error = Column(Text, nullable=True)
    log = Column(Text, nullable=True)  # Log detallado en JSON
