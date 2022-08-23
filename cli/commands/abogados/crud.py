"""
Abogados CRUD (create, read, update, and delete)
"""
from typing import Any

import requests

from config.settings import BASE_URL, LIMIT, TIMEOUT
import lib.exceptions


def get_abogados(
    authorization_header: dict,
    anio_desde: int = None,
    anio_hasta: int = None,
    limit: int = LIMIT,
    nombre: str = None,
    offset: int = 0,
) -> Any:
    """Solicitar abogados"""
    parametros = {"limit": limit}
    if anio_desde is not None:
        parametros["anio_desde"] = anio_desde
    if anio_hasta is not None:
        parametros["anio_hasta"] = anio_hasta
    if nombre is not None:
        parametros["nombre"] = nombre
    if offset > 0:
        parametros["offset"] = offset
    try:
        response = requests.get(
            f"{BASE_URL}/abogados",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise lib.exceptions.CLIStatusCodeError("No hubo respuesta al solicitar abogados") from error
    except requests.exceptions.HTTPError as error:
        raise lib.exceptions.CLIStatusCodeError("Error Status Code al solicitar abogados: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("Error inesperado al solicitar abogados") from error
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total en la respuesta al solicitar abogados")
    return data_json
