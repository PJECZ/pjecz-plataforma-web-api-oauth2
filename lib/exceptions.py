"""
Exceptions
"""


class PWAnyError(Exception):
    """Base exception class"""


class PWAlreadyExistsError(PWAnyError):
    """Excepción ya existe"""


class PWAuthenticationError(PWAnyError):
    """Excepción por que fallo la autentificacion"""


class PWEmptyError(PWAnyError):
    """Excepción por que no hay resultados"""


class PWIsDeletedError(PWAnyError):
    """Excepción esta eliminado"""


class PWNotExistsError(PWAnyError):
    """Excepción no existe"""


class PWNotValidParamError(PWAnyError):
    """Excepción porque un parámetro es inválido"""


class PWOutOfRangeParamError(PWAnyError):
    """Excepción porque un parámetro esta fuera de rango"""
