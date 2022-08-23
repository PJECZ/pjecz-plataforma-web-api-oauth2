"""
Centros de Trabajo CRUD (create, read, update, and delete)
"""
from typing import Any

import requests

from config.settings import BASE_URL, LIMIT, TIMEOUT
import lib.exceptions


def get_centros_trabajos(
    authorization_header: dict,
    distrito_id: int = None,
    domicilio_id: int = None,
    limit: int = LIMIT,
    offset: int = 0,
) -> Any:
    """Solicitar centros de trabajo"""
    parametros = {"limit": limit}
    if distrito_id is not None:
        parametros["distrito_id"] = distrito_id
    if domicilio_id is not None:
        parametros["domicilio_id"] = domicilio_id
    if offset > 0:
        parametros["offset"] = offset
    try:
        response = requests.get(
            f"{BASE_URL}/centros_trabajos",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise lib.exceptions.CLIStatusCodeError("No hubo respuesta al solicitar centros de trabajo") from error
    except requests.exceptions.HTTPError as error:
        raise lib.exceptions.CLIStatusCodeError("Error Status Code al solicitar centros de trabajo: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("Error inesperado al solicitar centros de trabajo") from error
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total en la respuesta al solicitar centros de trabajo")
    return data_json
