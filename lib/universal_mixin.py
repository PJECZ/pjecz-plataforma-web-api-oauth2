"""
UniversalMixin define las columnas y métodos comunes de todos los modelos
"""
import os
import re
from hashids import Hashids
from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import func

HASHID_REGEXP = re.compile("[0-9a-zA-Z]{8,16}")
SALT = os.environ.get("SALT", "Esta es una muy mala cadena aleatoria")

hashids = Hashids(salt=SALT, min_length=8)


class UniversalMixin:
    """Columnas y métodos comunes a todas las tablas"""

    creado = Column(DateTime, nullable=False)
    modificado = Column(DateTime, onupdate=func.now(), server_default=func.now())
    estatus = Column(String(1), server_default="A", nullable=False)

    def encode_id(self):
        """Convertir el ID de entero a cadena"""
        return hashids.encode(self.id)

    @classmethod
    def decode_id(cls, id_encoded: str):
        """Convertir el ID de entero a cadena"""
        if re.fullmatch(HASHID_REGEXP, id_encoded) is None:
            return None
        descifrado = hashids.decode(id_encoded)
        try:
            return descifrado[0]
        except IndexError:
            return None
