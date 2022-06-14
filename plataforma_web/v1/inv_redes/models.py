"""
Inventarios Redes v1, modelos
"""
from collections import OrderedDict
from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class InvRed(Base, UniversalMixin):
    """InvRed"""

    TIPOS = OrderedDict(
        [
            ("LAN", "Lan"),
            ("WIRELESS", "Wireless"),
        ]
    )

    # Nombre de la tabla
    __tablename__ = "inv_redes"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Columnas
    nombre = Column(String(256), unique=True, nullable=False)
    tipo = Column(Enum(*TIPOS, name="tipos_redes", native_enum=False), index=True, nullable=False)

    # Hijos
    inv_equipos = relationship("InvEquipo", back_populates="inv_red")

    def __repr__(self):
        """Representación"""
        return f"<InvRed {self.descripcion}>"
