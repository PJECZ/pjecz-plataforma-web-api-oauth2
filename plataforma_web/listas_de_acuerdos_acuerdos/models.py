"""
Listas de Acuerdos Acuerdos, modelos
"""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from lib.database import Base
from lib.universal_mixin import UniversalMixin


class ListaDeAcuerdoAcuerdo(Base, UniversalMixin):
    """ ListaDeAcuerdoAcuerdo """

    # Nombre de la tabla
    __tablename__ = 'listas_de_acuerdos_acuerdos'

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Clave foránea
    lista_de_acuerdo_id = Column(Integer, ForeignKey("listas_de_acuerdos.id"), index=True, nullable=False)
    lista_de_acuerdo = relationship("ListaDeAcuerdo", back_populates="listas_de_acuerdos_acuerdos")

    # Columnas
    folio = Column(String(16), default="")
    expediente = Column(String(16), default="")
    actor = Column(String(256), nullable=False, default="")
    demandado = Column(String(256), nullable=False, default="")
    tipo_acuerdo = Column(String(256), nullable=False, default="")
    tipo_juicio = Column(String(256), nullable=False, default="")
    referencia = Column(Integer(), nullable=False)

    def __repr__(self):
        """Representación"""
        return f"<ListaDeAcuerdoAcuerdo {self.id}>"
