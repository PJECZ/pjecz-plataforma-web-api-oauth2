"""
Exceptions
"""


class AlredyExistsException(Exception):
    """Excepción ya existe"""


class IsDeletedException(Exception):
    """Excepción esta eliminado"""


class NotExistsException(Exception):
    """Excepción no existe"""


class NotValidException(Exception):
    """Excepción porque un parámetro es inválido"""


class OutOfRangeException(Exception):
    """Excepción porque un parámetro esta fuera de rango"""
