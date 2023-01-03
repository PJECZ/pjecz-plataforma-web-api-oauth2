"""
Abogados, modelos
"""
from sqlalchemy import Column, Date, Integer, String

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class Abogado(Base, UniversalMixin):
    """Abogado"""

    # Nombre de la tabla
    __tablename__ = "abogados"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Columnas
    fecha = Column(Date, nullable=False, index=True)
    libro = Column(String(256), nullable=False)
    numero = Column(String(16), nullable=False)  # Hay datos como 000-Bis
    nombre = Column(String(256), nullable=False)

    def __repr__(self):
        """Representación"""
        return f"<Abogado {self.id}>"
