"""
Centros de Trabajo, modelos
"""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class CentroTrabajo(Base, UniversalMixin):
    """CentroTrabajo"""

    # Nombre de la tabla
    __tablename__ = "centros_trabajos"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Claves foráneas
    distrito_id = Column(Integer, ForeignKey("distritos.id"), index=True, nullable=False)
    distrito = relationship("Distrito", back_populates="centros_trabajos")
    domicilio_id = Column(Integer, ForeignKey("domicilios.id"), index=True, nullable=False)
    domicilio = relationship("Domicilio", back_populates="centros_trabajos")

    # Columnas
    clave = Column(String(16), unique=True, nullable=False)
    nombre = Column(String(256), nullable=False)
    telefono = Column(String(48), nullable=False)

    # Hijos
    funcionarios = relationship("Funcionario", back_populates="centro_trabajo")

    @property
    def distrito_nombre(self):
        """Nombre del distrito"""
        return self.distrito.nombre

    @property
    def distrito_nombre_corto(self):
        """Nombre corto del distrito"""
        return self.distrito.nombre_corto

    @property
    def domicilio_completo(self):
        """Domicilio completo"""
        return self.domicilio.completo

    def __repr__(self):
        """Representación"""
        return f"<CentroTrabajo {self.clave}>"
