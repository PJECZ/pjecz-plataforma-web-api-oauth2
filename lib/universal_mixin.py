"""
UniversalMixin define las columnas y métodos comunes de todos los modelos
"""
from sqlalchemy import Column, String


class UniversalMixin:
    """Columnas y métodos comunes a todas las tablas"""

    estatus = Column(String(1), server_default="A", nullable=False)
