"""
UniversalMixin define las columnas y métodos comunes de todos los modelos
"""
from sqlalchemy import Column, DateTime, String


class UniversalMixin:
    """Columnas y métodos comunes a todas las tablas"""

    creado = Column(DateTime, nullable=False)
    estatus = Column(String(1), server_default="A", nullable=False)
