"""
Materias Tipos Juicios v1, modelos
"""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class MateriaTipoJuicio(Base, UniversalMixin):
    """ MateriaTipoJuicio """

    # Nombre de la tabla
    __tablename__ = 'materias_tipos_juicios'

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Clave foránea
    materia_id = Column(Integer, ForeignKey("materias.id"), index=True, nullable=False)
    materia = relationship("Materia", back_populates="materias_tipos_juicios")

    # Columnas
    descripcion = Column(String(256), nullable=False)

    # Hijos
    sentencias = relationship("Sentencia", back_populates="materia_tipo_juicio", lazy="noload")

    @property
    def materia_nombre(self):
        """Nombre de la materia"""
        return self.materia.nombre

    def __repr__(self):
        """ Representación """
        return f"<MateriaTipoJuicio {self.descripcion}>"
