"""
Inventarios Componentes v1, modelos
"""
from collections import OrderedDict
from sqlalchemy import Boolean, Column, Date, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class InvComponente(Base, UniversalMixin):
    """InvComponente"""

    GENERACIONES = OrderedDict(
        [
            ("NO DEFINIDO", "No definido"),
            ("6ta Gen", "Sexta"),
            ("7ma Gen", "Septima"),
            ("8va Gen", "Octava"),
            ("9na Gen", "Novena"),
            ("10ma Gen", "Decima"),
            ("11va Gen", "Onceava"),
            ("12va Gen", "Doceava"),
        ]
    )

    # Nombre de la tabla
    __tablename__ = "inv_componentes"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Clave foránea
    inv_categoria_id = Column(Integer, ForeignKey("inv_categorias.id"), index=True, nullable=False)
    inv_categoria = relationship("InvCategoria", back_populates="inv_componentes")
    inv_equipo_id = Column(Integer, ForeignKey("inv_equipos.id"), index=True, nullable=False)
    inv_equipo = relationship("InvEquipo", back_populates="inv_componentes")

    # Columnas
    descripcion = Column(String(256), nullable=False)
    cantidad = Column(Integer(), nullable=False)
    generacion = Column(
        Enum(*GENERACIONES, name="generacion", native_enum=False),
        index=True,
        nullable=False,
        default="NO DEFINIDO",
        server_default="NO DEFINIDO",
    )
    version = Column(String(256))

    @property
    def inv_categoria_nombre(self):
        """Nombre de la categoría"""
        return self.inv_categoria.nombre

    @property
    def inv_equipo_descripcion(self):
        """Descripción del equipo"""
        return self.inv_equipo.descripcion

    def __repr__(self):
        """Representación"""
        return f"<InvComponente {self.descripcion}>"
