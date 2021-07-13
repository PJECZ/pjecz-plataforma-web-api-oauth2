"""
Roles, modelos
"""
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from lib.database import Base
from lib.universal_mixin import UniversalMixin


class Rol(Base, UniversalMixin):
    """ Rol """

    # Nombre de la tabla
    __tablename__ = 'roles'

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Columnas
    nombre = Column(String(256), unique=True, nullable=False)
    permiso = Column(Integer, nullable=False)
    por_defecto = Column(Boolean, default=False, index=True)

    # Hijos
    usuarios = relationship("Usuario", back_populates="rol")

    def __repr__(self):
        """Representación"""
        return f"<Rol {self.nombre}>"
