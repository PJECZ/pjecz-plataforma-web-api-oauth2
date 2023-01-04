"""
Inventarios Custodias, modelos
"""
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class InvCustodia(Base, UniversalMixin):
    """InvCustodia"""

    # Nombre de la tabla
    __tablename__ = "inv_custodias"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Clave foránea
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), index=True, nullable=False)
    usuario = relationship("Usuario", back_populates="inv_custodias")

    # Columnas
    fecha = Column(Date, nullable=False, index=True)
    curp = Column(String(256), nullable=True)
    nombre_completo = Column(String(256))

    # Hijos
    inv_equipos = relationship("InvEquipo", back_populates="inv_custodia")

    @property
    def usuario_email(self):
        """Email del usuario"""
        return self.usuario.email

    @property
    def usuario_nombre(self):
        """Nombre del usuario"""
        return self.usuario.nombre

    def __repr__(self):
        """Representación"""
        return f"<InvCustodia {self.id}>"
