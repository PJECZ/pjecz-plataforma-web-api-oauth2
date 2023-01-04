"""
REPSVM Agresores-Delitos, modelos
"""
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class REPSVMAgresorDelito(Base, UniversalMixin):
    """REPSVMAgresorDelito"""

    # Nombre de la tabla
    __tablename__ = "repsvm_agresores_delitos"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Claves foráneas
    repsvm_agresor_id = Column(Integer, ForeignKey("repsvm_agresores.id"), index=True, nullable=False)
    repsvm_agresor = relationship("REPSVMAgresor", back_populates="repsvm_agresores_delitos")
    repsvm_delito_id = Column(Integer, ForeignKey("repsvm_delitos.id"), index=True, nullable=False)
    repsvm_delito = relationship("REPSVMDelito", back_populates="repsvm_agresores_delitos")

    @property
    def repsvm_agresor_nombre(self):
        """Nombre del agresor"""
        return self.repsvm_agresor.nombre

    @property
    def repsvm_delito_nombre(self):
        """Nombre del delito"""
        return self.repsvm_delito.nombre

    def __repr__(self):
        """Representación"""
        return f"<REPSVMAgresorDelito {self.id}>"
