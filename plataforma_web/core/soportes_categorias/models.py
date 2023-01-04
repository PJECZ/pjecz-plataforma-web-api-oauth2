"""
Soportes Categorias, modelos
"""
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class SoporteCategoria(Base, UniversalMixin):
    """SoporteCategoria"""

    # Nombre de la tabla
    __tablename__ = "soportes_categorias"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Clave foránea
    rol_id = Column(Integer, ForeignKey("roles.id"), index=True, nullable=False)
    rol = relationship("Rol", back_populates="soportes_categorias")

    # Columnas
    nombre = Column(String(256), unique=True, nullable=False)
    instrucciones = Column(Text())

    # Hijos
    soportes_tickets = relationship("SoporteTicket", back_populates="soporte_categoria")

    @property
    def rol_nombre(self):
        """Nombre de la rol"""
        return self.rol.nombre

    def __repr__(self):
        """Representación"""
        return f"<SoporteCategoria {self.nombre}>"
