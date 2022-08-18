"""
Exceptions
"""


class PlataformaWebAnyError(Exception):
    """Base exception class"""


class AlredyExistsException(PlataformaWebAnyError):
    """Excepción ya existe"""


class IsDeletedException(PlataformaWebAnyError):
    """Excepción esta eliminado"""


class NotExistsException(PlataformaWebAnyError):
    """Excepción no existe"""


class NotValidException(PlataformaWebAnyError):
    """Excepción porque un parámetro es inválido"""


class OutOfRangeException(PlataformaWebAnyError):
    """Excepción porque un parámetro esta fuera de rango"""
