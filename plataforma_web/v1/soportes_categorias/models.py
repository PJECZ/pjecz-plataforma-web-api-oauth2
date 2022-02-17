"""
Soportes Categorias v1, modelos
"""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class SoporteCategoria(Base, UniversalMixin):
    """ SoporteCategoria """

    # Nombre de la tabla
    __tablename__ = 'soportes_categorias'

    # Clave foránea
    rol_id = Column(Integer, ForeignKey('roles.id'), index=True, nullable=False)
    rol = relationship('Rol', back_populates='soportes_categorias_roles')

    # Columnas
    nombre = Column(String(256), unique=True, nullable=False)
    instrucciones = Column(Text(), default="", server_default="")

    # Hijos
    soportes_tickets = relationship("SoporteTicket", back_populates="soporte_categoria")

    def __repr__(self):
        """ Representación """
        return f"<SoporteCategoria {self.nombre}>"
