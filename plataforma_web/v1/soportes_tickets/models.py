"""
Soportes Tickets v1, modelos
"""
from collections import OrderedDict
from sqlalchemy import Column, Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class SoporteTicket(Base, UniversalMixin):
    """SoporteTicket"""

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
    __tablename__ = "soportes_tickets"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Claves foránea el funcionario es el técnico de soporte
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"), index=True, nullable=True)
    funcionario = relationship("Funcionario", back_populates="soportes_tickets")

    # Claves foránea la categoría
    soporte_categoria_id = Column(Integer, ForeignKey("soportes_categorias.id"), index=True, nullable=True)
    soporte_categoria = relationship("SoporteCategoria", back_populates="soportes_tickets")

    # Claves foránea el usario que solicita soporte
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), index=True, nullable=False)
    usuario = relationship("Usuario", back_populates="soportes_tickets")

    # Columnas
    descripcion = Column(Text, nullable=False)
    estado = Column(Enum(*ESTADOS, name="estados", native_enum=False), index=True, nullable=False)
    soluciones = Column(Text, nullable=False)

    @property
    def funcionario_nombre(self):
        """Nombre del funcionario"""
        return self.funcionario.nombre

    @property
    def soporte_categoria_nombre(self):
        """Nombre del sopote categoria"""
        return self.soporte_categoria.nombre

    @property
    def usuario_email(self):
        """e-mail del usuario"""
        return self.usuario.email

    @property
    def usuario_nombre(self):
        """Nombre del usuario"""
        return self.usuario.nombre

    @property
    def usuario_oficina_id(self):
        """ID de la oficina del usuario"""
        return self.usuario.oficina_id

    @property
    def usuario_oficina_clave(self):
        """Clave de la oficina del usuario"""
        return self.usuario.oficina.clave

    def __repr__(self):
        """Representación"""
        return f"<SoporteTicket {self.descripcion}>"
