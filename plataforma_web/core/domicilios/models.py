"""
Domicilios, modelos
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class Domicilio(Base, UniversalMixin):
    """Domicilio"""

    # Nombre de la tabla
    __tablename__ = "domicilios"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Columnas
    edificio = Column(String(64), nullable=True, unique=True)
    estado = Column(String(64), nullable=False)
    municipio = Column(String(64), nullable=False)
    calle = Column(String(256), nullable=False)
    num_ext = Column(String(24), nullable=False)
    num_int = Column(String(24), nullable=False)
    colonia = Column(String(256), nullable=False)
    cp = Column(Integer(), nullable=False)
    completo = Column(String(1024), nullable=False)
    numeracion_telefonica = Column(String(256), nullable=False)

    # Hijos
    centros_trabajos = relationship("CentroTrabajo", back_populates="domicilio")
    oficinas = relationship("Oficina", back_populates="domicilio")

    def __repr__(self):
        """Representación"""
        return f"<Domicilio {self.completo}>"
