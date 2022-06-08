"""
Funcionarios v1, modelos
"""
from sqlalchemy import Boolean, ForeignKey, Column, Date, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class Funcionario(Base, UniversalMixin):
    """Funcionario"""

    # Nombre de la tabla
    __tablename__ = "funcionarios"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Clave foránea
    centro_trabajo_id = Column(Integer, ForeignKey("centros_trabajos.id"), index=True, nullable=False)
    centro_trabajo = relationship("CentroTrabajo", back_populates="funcionarios")

    # Columnas
    nombres = Column(String(256), nullable=False)
    apellido_paterno = Column(String(256), nullable=False)
    apellido_materno = Column(String(256))
    curp = Column(String(18), unique=True, index=True)
    email = Column(String(256), unique=True, index=True)
    puesto = Column(String(256))
    en_funciones = Column(Boolean, nullable=False, default=True)
    en_soportes = Column(Boolean, nullable=False, default=False)
    telefono = Column(String(48), nullable=False)
    extension = Column(String(24), nullable=False)
    domicilio_oficial = Column(String(512), nullable=False)
    ingreso_fecha = Column(Date(), nullable=False)
    puesto_clave = Column(String(32))
    fotografia_url = Column(String(512), nullable=False)

    # Hijos
    soportes_tickets = relationship("SoporteTicket", back_populates="funcionario")

    @property
    def nombre(self):
        """Junta nombres, apellido_paterno y apellido materno"""
        return self.nombres + " " + self.apellido_paterno + " " + self.apellido_materno

    def __repr__(self):
        """Representación"""
        return f"<Funcionario {self.curp}>"
