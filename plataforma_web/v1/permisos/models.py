"""
Permisos v1, modelos
"""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class Permiso(Base, UniversalMixin):
    """Permiso"""

    VER = 1
    MODIFICAR = 2
    CREAR = 3
    ADMINISTRAR = 4
    NIVELES = {
        1: "VER",
        2: "VER y MODIFICAR",
        3: "VER, MODIFICAR y CREAR",
        4: "ADMINISTRAR",
    }

    # Nombre de la tabla
    __tablename__ = "permisos"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Claves foráneas
    modulo_id = Column(Integer, ForeignKey("modulos.id"), index=True, nullable=False)
    modulo = relationship("Modulo", back_populates="permisos")
    rol_id = Column(Integer, ForeignKey("roles.id"), index=True, nullable=False)
    rol = relationship("Rol", back_populates="permisos")

    # Columnas
    nombre = Column(String(256), nullable=False, unique=True)
    nivel = Column(Integer(), nullable=False)

    @property
    def rol_nombre(self):
        """Nombre del rol"""
        return self.rol.nombre

    @property
    def modulo_nombre(self):
        """Nombre del modulo"""
        return self.modulo.nombre

    def __repr__(self):
        """Representación"""
        return f"<Permiso {self.nombre}>"
