"""
Inventarios Modelos v1, modelos
"""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class InvModelo(Base, UniversalMixin):
    """InvModelo"""

    # Nombre de la tabla
    __tablename__ = "inv_modelos"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Clave foránea
    inv_marca_id = Column(Integer, ForeignKey("inv_marcas.id"), index=True, nullable=False)
    inv_marca = relationship("InvMarca", back_populates="inv_modelos")

    # Columnas
    descripcion = Column(String(256), nullable=False)

    # Hijos
    inv_equipos = relationship("InvEquipo", back_populates="inv_modelo", lazy="noload")

    @property
    def inv_marca_nombre(self):
        """Nombre de la marca"""
        return self.inv_marca.nombre

    def __repr__(self):
        """Representación"""
        return f"<InvModelo {self.descripcion}>"
