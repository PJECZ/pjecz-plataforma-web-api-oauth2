"""
Glosas, modelos
"""
from collections import OrderedDict

from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class Glosa(Base, UniversalMixin):
    """Glosa"""

    TIPOS_JUICIOS = OrderedDict(
        [
            ("ND", "No Definido"),
            ("AMPARO", "Amparo"),
            ("EJECUCION", "Ejecución"),
            ("JUICIO ORAL", "Juicio Oral"),
            ("JUICIO DE NULIDAD", "Juicio de Nulidad"),
            ("LABORAL LAUDO", "Laboral Laudo"),
            ("ORAL", "Oral"),
            ("PENAL", "Penal"),
            ("SALA CIVIL", "Sala Civil"),
            ("SALA CIVIL Y FAMILIAR", "Sala Civil y Familiar"),
            ("TRADICIONAL", "Tradicional"),
        ]
    )

    # Nombre de la tabla
    __tablename__ = "glosas"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Clave foránea
    autoridad_id = Column(Integer, ForeignKey("autoridades.id"), index=True, nullable=False)
    autoridad = relationship("Autoridad", back_populates="glosas")

    # Columnas
    fecha = Column(Date, index=True, nullable=False)
    tipo_juicio = Column(Enum(*TIPOS_JUICIOS, name="tipos_juicios", native_enum=False), index=True, nullable=False)
    descripcion = Column(String(256), nullable=False)
    expediente = Column(String(16), nullable=False)
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
    def autoridad_clave(self):
        """Autoridad clave"""
        return self.autoridad.clave

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
        return f"<Glosa {self.id}>"
