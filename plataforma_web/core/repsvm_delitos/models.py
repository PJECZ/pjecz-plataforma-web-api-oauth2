"""
REPSVM Delitos, modelos
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class REPSVMDelito(Base, UniversalMixin):
    """REPSVMDelito"""

    # Nombre de la tabla
    __tablename__ = "repsvm_delitos"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Columnas
    nombre = Column(String(256), unique=True, nullable=False)

    # Hijos
    repsvm_agresores_delitos = relationship("REPSVMAgresorDelito", back_populates="repsvm_delito")

    def __repr__(self):
        """Representación"""
        return f"<REPSVMDelito {self.id}>"
