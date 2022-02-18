"""
Usuarios v1.0, modelos
"""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin

from plataforma_web.v1.modulos.models import Modulo
from plataforma_web.v1.permisos.models import Permiso


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

    # Hijos
    usuarios_roles = relationship("UsuarioRol", back_populates="usuario")
    soportes_tickets = relationship("SoporteTicket", back_populates="usuario")

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

    @property
    def nombre(self):
        """Junta nombres, apellido_paterno y apellido materno"""
        return self.nombres + " " + self.apellido_paterno + " " + self.apellido_materno

    def permissions(self):
        """Entrega un diccionario con todos los permisos"""
        todos = {}
        for usuario_rol in self.usuarios_roles:
            if usuario_rol.estatus == "A":
                for permiso in usuario_rol.rol.permisos:
                    if permiso.estatus == "A":
                        etiqueta = permiso.modulo.nombre
                        if etiqueta not in todos or permiso.nivel > todos[etiqueta]:
                            todos[etiqueta] = permiso.nivel
        return todos

    def __repr__(self):
        """Representación"""
        return f"<Usuario {self.email}>"
