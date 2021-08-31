"""
Sentencias v1, modelos
"""
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class Sentencia(Base, UniversalMixin):
    """Sentencia"""

    # Nombre de la tabla
    __tablename__ = "sentencias"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Clave foránea
    autoridad_id = Column(Integer, ForeignKey("autoridades.id"), index=True, nullable=False)
    autoridad = relationship("Autoridad", back_populates="sentencias")
    materia_tipo_juicio_id = Column(Integer, ForeignKey("materias_tipos_juicios.id"), index=True, nullable=False)
    materia_tipo_juicio = relationship("MateriaTipoJuicio", back_populates="sentencias")

    # Columnas
    sentencia = Column(String(16), nullable=False)
    sentencia_fecha = Column(Date, index=True, nullable=True)
    expediente = Column(String(16), nullable=False)
    fecha = Column(Date, index=True, nullable=False)
    descripcion = Column(String(1024), nullable=False, default="", server_default="")
    es_perspectiva_genero = Column(Boolean, nullable=False, default=False)
    archivo = Column(String(256), nullable=False, default="", server_default="")
    url = Column(String(512), nullable=False, default="", server_default="")

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
    def materia_id(self):
        """Materia id"""
        return self.materia_tipo_juicio.materia_id

    @property
    def materia_nombre(self):
        """Materia nombre"""
        return self.materia_tipo_juicio.materia.nombre

    @property
    def materia_tipo_juicio_descripcion(self):
        """Materia Tipo Juicio descripcion"""
        return self.materia_tipo_juicio.descripcion

    def __repr__(self):
        """Representación"""
        return f"<Sentencia {self.descripcion}>"
