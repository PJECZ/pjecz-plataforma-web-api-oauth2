"""
Listas de Acuerdos, modelos
"""
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from lib.database import Base
from lib.universal_mixin import UniversalMixin


class ListaDeAcuerdo(Base, UniversalMixin):
    """Lista de Acuerdo"""

    # Nombre de la tabla
    __tablename__ = "listas_de_acuerdos"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Clave foránea
    autoridad_id = Column(Integer, ForeignKey("autoridades.id"), index=True, nullable=False)
    autoridad = relationship("Autoridad", back_populates="listas_de_acuerdos")

    # Columnas
    fecha = Column(Date, index=True, nullable=False)
    descripcion = Column(String(256), nullable=False)
    archivo = Column(String(256))
    url = Column(String(512))

    # Hijos
    listas_de_acuerdos_acuerdos = relationship('ListaDeAcuerdoAcuerdo', back_populates='lista_de_acuerdo')
