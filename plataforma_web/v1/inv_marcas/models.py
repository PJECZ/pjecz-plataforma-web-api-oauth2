"""
Inventarios Marcas v1, modelos
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class InvMarca(Base, UniversalMixin):
    """InvMarca"""

    # Nombre de la tabla
    __tablename__ = "inv_marcas"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Columnas
    nombre = Column(String(256), unique=True, nullable=False)

    # Hijos
    inv_modelos = relationship("InvModelo", back_populates="inv_marca")

    def __repr__(self):
        """Representación"""
        return f"<InvMarca {self.nombre}>"
