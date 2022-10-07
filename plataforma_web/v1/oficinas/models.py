"""
Oficinas v1, modelos
"""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class Oficina(Base, UniversalMixin):
    """Oficina"""

    # Nombre de la tabla
    __tablename__ = "oficinas"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Clave foránea
    distrito_id = Column(Integer, ForeignKey("distritos.id"), index=True, nullable=False)
    distrito = relationship("Distrito", back_populates="oficinas")
    domicilio_id = Column(Integer, ForeignKey("domicilios.id"), index=True, nullable=False)
    domicilio = relationship("Domicilio", back_populates="oficinas")

    # Columnas
    clave = Column(String(32), unique=True, nullable=False)
    descripcion = Column(String(512), nullable=False)
    descripcion_corta = Column(String(64), nullable=False)
    es_jurisdiccional = Column(Boolean, nullable=False, default=False)
    apertura = Column(Time(), nullable=False)
    cierre = Column(Time(), nullable=False)
    limite_personas = Column(Integer(), nullable=False)

    # Hijos
    usuarios = relationship("Usuario", back_populates="oficina")

    @property
    def distrito_nombre_corto(self):
        """Nombre corto del distrito"""
        return self.distrito.nombre_corto

    @property
    def domicilio_completo(self):
        """Domicilio completo de la oficina"""
        return self.domicilio.completo

    def __repr__(self):
        """Representación"""
        return f"<Oficina {self.descripcion}>"
