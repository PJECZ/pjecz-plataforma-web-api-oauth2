"""
REPSVM Agresores, modelos
"""
from collections import OrderedDict

from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class REPSVMAgresor(Base, UniversalMixin):
    """REPSVMAgresor"""

    TIPOS_JUZGADOS = OrderedDict(
        [
            ("ND", "No Definido"),
            ("JUZGADO ESPECIALIZADO EN VIOLENCIA CONTRA LAS MUJERES", "Juzgado Especializado en Violencia contra las Mujeres"),
            ("JUZGADO ESPECIALIZADO EN VIOLENCIA FAMILIAR", "Juzgado Especializado en Violencia Familiar"),
            ("JUZGADO DE PRIMERA INSTANCIA EN MATERIA PENAL", "Juzgado de Primera Instancia en Materia Penal"),
        ]
    )

    TIPOS_SENTENCIAS = OrderedDict(
        [
            ("ND", "No Definido"),
            ("PROCEDIMIENTO ABREVIADO", "Procedimiento Abreviado"),
            ("JUICIO ORAL", "Juicio Oral"),
        ]
    )

    # Nombre de la tabla
    __tablename__ = "repsvm_agresores"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Claves foráneas
    distrito_id = Column(Integer, ForeignKey("distritos.id"), index=True, nullable=False)
    distrito = relationship("Distrito", back_populates="repsvm_agresores")

    # Columnas
    consecutivo = Column(Integer(), nullable=False)
    delito_generico = Column(String(256), nullable=False)
    delito_especifico = Column(String(256), nullable=False)
    es_publico = Column(Boolean(), nullable=False)
    nombre = Column(String(256), nullable=False)
    numero_causa = Column(String(256), nullable=False)
    pena_impuesta = Column(String(256), nullable=False)
    observaciones = Column(Text(), nullable=True)
    sentencia_url = Column(String(512), nullable=False)
    tipo_juzgado = Column(Enum(*TIPOS_JUZGADOS, name="tipos_juzgados", native_enum=False), index=True, nullable=False)
    tipo_sentencia = Column(Enum(*TIPOS_SENTENCIAS, name="tipos_sentencias", native_enum=False), index=True, nullable=False)

    # Hijos
    repsvm_agresores_delitos = relationship("REPSVMAgresorDelito", back_populates="repsvm_agresor")

    @property
    def distrito_nombre(self):
        """Nombre del distrito"""
        return self.distrito.nombre

    @property
    def distrito_nombre_corto(self):
        """Nombre corto del distrito"""
        return self.distrito.nombre_corto

    def __repr__(self):
        """Representación"""
        return f"<REPSVMAgresor {self.id}>"
