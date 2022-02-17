"""
Soportes Tickets v1, modelos
"""
from collections import OrderedDict
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class SoporteTicket(Base, UniversalMixin):
    """ SoporteTicket """

    ESTADOS = OrderedDict(
        [
            ("ABIERTO", "Abierto o pendiente"),
            ("TRABAJANDO", "Trabjando"),
            ("CERRADO", "Cerrado o terminado"),
            ("NO RESUELTO", "No resuelto"),
            ("CANCELADO", "Cancelado"),
        ]
    )

    # Nombre de la tabla
    __tablename__ = 'soportes_tickets'

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Claves foránea la categoría
    soporte_categoria_id = Column(Integer, ForeignKey("soportes_categorias.id"), index=True, nullable=True)
    soporte_categoria = relationship("SoporteCategoria", back_populates="soportes_tickets")

    # Claves foránea el usario que solicita soporte
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), index=True, nullable=False)
    usuario = relationship("Usuario", back_populates="soportes_tickets")

    # Columnas
    descripcion = Column(Text, nullable=False)
    estado = Column(Enum(*ESTADOS, name="estados", native_enum=False), index=True, nullable=False)
    resolucion = Column(DateTime, nullable=True)
    soluciones = Column(Text, nullable=True)

    def __repr__(self):
        """ Representación """
        return f"<SoporteTicket {self.descripcion}>"
