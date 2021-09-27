"""
Listas de Acuerdos v1, modelos
"""
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class ListaDeAcuerdo(Base, UniversalMixin):
    """ListaDeAcuerdo"""

    # Nombre de la tabla
    __tablename__ = "listas_de_acuerdos"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Clave foránea
    autoridad_id = Column(Integer, ForeignKey("autoridades.id"), index=True, nullable=False)
    autoridad = relationship("Autoridad", back_populates="listas_de_acuerdos")

    # Columnas
    fecha = Column(Date, index=True, nullable=False)
    descripcion = Column(String(256), nullable=False)
    archivo = Column(String(256), default="")
    url = Column(String(512), default="")

    # Hijos
    listas_de_acuerdos_acuerdos = relationship('ListaDeAcuerdoAcuerdo', back_populates='lista_de_acuerdo')

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
    def autoridad_clave(self):
        """Autoridad clave"""
        return self.autoridad.clave

    def __repr__(self):
        """Representación"""
        return f"<ListaDeAcuerdo {self.fecha}>"
