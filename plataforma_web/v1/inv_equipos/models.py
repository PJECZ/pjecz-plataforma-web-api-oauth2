"""
Inventarios Equipos v1, modelos
"""
from collections import OrderedDict
from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class InvEquipo(Base, UniversalMixin):
    """InvEquipo"""

    TIPOS = OrderedDict(
        [
            ("COMPUTADORA", "COMPUTADORA"),
            ("LAPTOP", "LAPTOP"),
            ("IMPRESORA", "IMPRESORA"),
            ("MULTIFUNCIONAL", "MULTIFUNCIONAL"),
            ("TELEFONIA", "TELEFONIA"),
            ("SERVIDOR", "SERVIDOR"),
            ("SCANNER", "SCANNER"),
            ("SWITCH", "SWITCH"),
            ("VIDEOGRABACION", "VIDEOGRABACION"),
            ("OTROS", "OTROS"),
        ]
    )

    # Nombre de la tabla
    __tablename__ = "inv_equipos"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Clave foránea
    inv_custodia_id = Column(Integer, ForeignKey("inv_custodias.id"), index=True, nullable=False)
    inv_custodia = relationship("InvCustodia", back_populates="inv_equipos")
    inv_modelo_id = Column(Integer, ForeignKey("inv_modelos.id"), index=True, nullable=False)
    inv_modelo = relationship("InvModelo", back_populates="inv_equipos")
    inv_red_id = Column(Integer, ForeignKey("inv_redes.id"), index=True, nullable=False)
    inv_red = relationship("InvRed", back_populates="inv_equipos")

    # Columnas
    fecha_fabricacion = Column(Date())
    numero_serie = Column(String(256))
    numero_inventario = Column(Integer())
    descripcion = Column(String(256), nullable=False)
    tipo = Column(Enum(*TIPOS, name="tipos", native_enum=False), index=True, nullable=False)
    direccion_ip = Column(String(256))
    direccion_mac = Column(String(256))
    numero_nodo = Column(Integer())
    numero_switch = Column(Integer())
    numero_puerto = Column(Integer())

    # Hijos
    # inv_componentes = relationship("InvComponente", back_populates="inv_equipo", lazy="noload")
    # inv_equipos_fotos = relationship("InvEquipoFoto", back_populates="inv_equipo", lazy="noload")

    @property
    def inv_custodia_nombre_completo(self):
        """Nombre completo de la custodia"""
        return self.inv_custodia.nombre_completo

    @property
    def inv_marca_nombre(self):
        """Nombre de la marca"""
        return self.inv_modelo.inv_marca.nombre

    @property
    def inv_modelo_descripcion(self):
        """Descripción del modelo"""
        return self.inv_modelo.descripcion

    @property
    def inv_red_nombre(self):
        """Nombre de la red"""
        return self.inv_red.nombre

    def __repr__(self):
        """Representación"""
        return f"<InvEquipo {self.id}>"
