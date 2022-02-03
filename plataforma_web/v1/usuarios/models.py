"""
Usuarios v1.0, modelos
"""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class Usuario(Base, UniversalMixin):
    """Usuario"""

    # Nombre de la tabla
    __tablename__ = "usuarios"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Claves foráneas
    autoridad_id = Column(Integer, ForeignKey("autoridades.id"), index=True, nullable=False)
    autoridad = relationship("Autoridad", back_populates="usuarios")

    # Columnas
    email = Column(String(256), unique=True, index=True)
    contrasena = Column(String(256), nullable=False)
    nombres = Column(String(256), nullable=False)
    apellido_paterno = Column(String(256), nullable=False)
    apellido_materno = Column(String(256))
    curp = Column(String(18))
    puesto = Column(String(256))
    telefono_celular = Column(String(256))

    @property
    def rol_nombre(self):
        """Rol nombre"""
        return self.rol.nombre

    @property
    def distrito_id(self):
        """Distrito id"""
        return self.autoridad.distrito_id

    @property
    def distrito_nombre(self):
        """Distrito nombre"""
        return self.autoridad.distrito.nombre

    @property
    def distrito_nombre_corto(self):
        """Distrito nombre corto"""
        return self.autoridad.distrito.nombre_corto

    @property
    def autoridad_descripcion(self):
        """Autoridad descripcion"""
        return self.autoridad.descripcion

    @property
    def autoridad_descripcion_corta(self):
        """Autoridad descripcion corta"""
        return self.autoridad.descripcion_corta

    def __repr__(self):
        """Representación"""
        return f"<Usuario {self.email}>"
