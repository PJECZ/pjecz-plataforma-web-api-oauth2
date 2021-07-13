"""
Usuarios, modelos
"""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from lib.database import Base
from lib.universal_mixin import UniversalMixin


class Usuario(Base, UniversalMixin):
    """ Usuario """

    # Nombre de la tabla
    __tablename__ = 'usuarios'

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Claves foráneas
    rol_id = Column(Integer, ForeignKey("roles.id"), index=True, nullable=False)
    rol = relationship("Rol", back_populates="usuarios")
    autoridad_id = Column(Integer, ForeignKey("autoridades.id"), index=True, nullable=False)
    autoridad = relationship("Autoridad", back_populates="usuarios")

    # Columnas
    email = Column(String(256), unique=True, index=True)
    contrasena = Column(String(256), nullable=False)
    nombres = Column(String(256), nullable=False)
    apellido_paterno = Column(String(256), nullable=False)
    apellido_materno = Column(String(256))
