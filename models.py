from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Tarea(Base):
    __tablename__ = "tarea"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    descripcion = Column(String, index=True)
    responsable = Column(String, index=True)
    estado = Column(String, index=True, default="Pendiente")
    fecha_creacion = Column(String, index=True)
    fecha_modificacion = Column(String, index=True)