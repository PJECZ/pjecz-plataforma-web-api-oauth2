"""
Usuarios CRUD (create, read, update, and delete)
"""
from typing import Any

import requests

from config.settings import BASE_URL, LIMIT, TIMEOUT
import lib.exceptions


def get_usuarios(
    authorization_header: dict,
    limit: int = LIMIT,
    autoridad_id: int = None,
    autoridad_clave: str = None,
    offset: int = 0,
    oficina_id: int = None,
    oficina_clave: str = None,
) -> Any:
    """Solicitar usuarios"""
    parametros = {"limit": limit}
    if autoridad_id is not None:
        parametros["autoridad_id"] = autoridad_id
    if autoridad_clave is not None:
        parametros["autoridad_clave"] = autoridad_clave
    if offset > 0:
        parametros["offset"] = offset
    if oficina_id is not None:
        parametros["oficina_id"] = oficina_id
    if oficina_clave is not None:
        parametros["oficina_clave"] = oficina_clave
    try:
        response = requests.get(
            f"{BASE_URL}/usuarios",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise lib.exceptions.CLIStatusCodeError("No hubo respuesta al solicitar usuarios") from error
    except requests.exceptions.HTTPError as error:
        raise lib.exceptions.CLIStatusCodeError("Error Status Code al solicitar usuarios: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("Error inesperado al solicitar usuarios") from error
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total en la respuesta al solicitar usuarios")
    return data_json
