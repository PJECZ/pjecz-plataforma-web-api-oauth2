"""
UniversalMixin define las columnas y métodos comunes de todos los modelos
"""
import re

from hashids import Hashids
from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import func

from config.settings import get_settings

settings = get_settings()
hashids = Hashids(salt=settings.salt, min_length=8)


class UniversalMixin:
    """Columnas y métodos comunes a todas las tablas"""

    creado = Column(DateTime, server_default=func.now(), nullable=False)
    modificado = Column(DateTime, onupdate=func.now(), server_default=func.now())
    estatus = Column(String(1), server_default="A", nullable=False)

    def encode_id(self):
        """Convertir el ID de entero a cadena"""
        return hashids.encode(self.id)

    @classmethod
    def decode_id(cls, id_encoded: str):
        """Convertir el ID de entero a cadena"""
        if re.fullmatch(r"[0-9a-zA-Z]{8,16}", id_encoded) is None:
            return None
        descifrado = hashids.decode(id_encoded)
        try:
            return descifrado[0]
        except IndexError:
            return None
