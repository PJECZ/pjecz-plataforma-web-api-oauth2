"""
Materias, modelos
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from lib.database import Base
from lib.universal_mixin import UniversalMixin


class Materia(Base, UniversalMixin):
    """ Materia """

    # Nombre de la tabla
    __tablename__ = 'materias'

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Columnas
    nombre = Column(String(64), unique=True, nullable=False)

    # Hijos
    autoridades = relationship("Autoridad", back_populates="materia")
