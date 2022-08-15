"""
CLI Exceptions
"""


class CLIAnyError(Exception):
    """Excepcion base para todas las excepciones del CLI"""


class CLIConfigurationError(CLIAnyError):
    """Excepcion porque falta algo en la configuracion"""


class CLIAuthenticationError(CLIAnyError):
    """Excepcion porque falla la autenticacion"""


class CLIConnectionError(CLIAnyError):
    """Excepcion porque falla la comunicacion o no llega la respuesta"""


class CLIStatusCodeError(CLIAnyError):
    """Excepcion porque el status code no es 200"""


class CLIResponseError(CLIAnyError):
    """Excepcion porque lo que llega no es lo esperado"""
