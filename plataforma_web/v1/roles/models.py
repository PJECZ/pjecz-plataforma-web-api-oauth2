"""
Roles v1.0, modelos
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class Permiso:
    """Permiso tiene como constantes enteros de potencia dos"""

    # CUENTAS
    VER_CUENTAS = 0b1
    MODIFICAR_CUENTAS = 0b10
    CREAR_CUENTAS = MODIFICAR_CUENTAS

    # CATALOGOS
    VER_CATALOGOS = 0b100
    MODIFICAR_CATALOGOS = 0b1000
    CREAR_CATALOGOS = MODIFICAR_CATALOGOS

    # DOCUMENTACIONES
    VER_DOCUMENTACIONES = 0b10000
    MODIFICAR_DOCUMENTACIONES = 0b100000
    CREAR_DOCUMENTACIONES = MODIFICAR_DOCUMENTACIONES

    # CONSULTAS
    VER_CONSULTAS = 0b1000000
    MODIFICAR_CONSULTAS = 0b10000000
    CREAR_CONSULTAS = MODIFICAR_CONSULTAS

    # JUSTICIABLES
    VER_JUSTICIABLES = 0b100000000
    MODIFICAR_JUSTICIABLES = 0b1000000000
    CREAR_JUSTICIABLES = MODIFICAR_JUSTICIABLES
    ADMINISTRAR_JUSTICIABLES = 0b10000000000

    # NOTARIALES
    VER_NOTARIALES = 0b100000000000
    MODIFICAR_NOTARIALES = 0b1000000000000
    CREAR_NOTARIALES = MODIFICAR_NOTARIALES
    ADMINISTRAR_NOTARIALES = 0b10000000000000

    # SEGUNDAS INSTANCIAS
    VER_SEGUNDAS = 0b100000000000000
    MODIFICAR_SEGUNDAS = 0b1000000000000000
    CREAR_SEGUNDAS = MODIFICAR_SEGUNDAS
    ADMINISTRAR_SEGUNDAS = 0b10000000000000000

    def __repr__(self):
        """Representación"""
        return "<Permiso>"


class Rol(Base, UniversalMixin):
    """Rol"""

    # Nombre de la tabla
    __tablename__ = "roles"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Columnas
    nombre = Column(String(256), unique=True, nullable=False)
    permiso = Column(Integer, nullable=False)

    # Hijos
    usuarios = relationship("Usuario", back_populates="rol")

    def has_permission(self, perm):
        """¿Tiene el permiso dado?"""
        return self.permiso & perm == perm

    def __repr__(self):
        """Representación"""
        return f"<Rol {self.nombre}>"
