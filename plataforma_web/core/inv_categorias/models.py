"""
Inventarios Categorias, modelos
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class InvCategoria(Base, UniversalMixin):
    """InvCategoria"""

    # Nombre de la tabla
    __tablename__ = "inv_categorias"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Columnas
    nombre = Column(String(256), unique=True, nullable=False)

    # Hijos
    inv_componentes = relationship("InvComponente", back_populates="inv_categoria")

    def __repr__(self):
        """Representación"""
        return f"<InvCategoria {self.nombre}>"
