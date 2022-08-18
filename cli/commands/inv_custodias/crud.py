"""
Inv Custodias CRUD (create, read, update, and delete)
"""
from datetime import date
from typing import Any

import requests

from config.settings import BASE_URL, LIMIT, TIMEOUT
import lib.exceptions


def get_inv_custodias(
    authorization_header: dict,
    limit: int = LIMIT,
    usuario_id: int = None,
    usuario_email: str = None,
    fecha_desde: date = None,
    fecha_hasta: date = None,
) -> Any:
    """Solicitar inventarios custodias"""
    parametros = {"limit": limit}
    if usuario_id is not None:
        parametros["usuario_id"] = usuario_id
    if usuario_email is not None:
        parametros["usuario_email"] = usuario_email
    if fecha_desde is not None:
        parametros["fecha_desde"] = fecha_desde
    if fecha_hasta is not None:
        parametros["fecha_hasta"] = fecha_hasta
    try:
        response = requests.get(
            f"{BASE_URL}/inv_custodias",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise lib.exceptions.CLIStatusCodeError("No hubo respuesta al solicitar custodias") from error
    except requests.exceptions.HTTPError as error:
        raise lib.exceptions.CLIStatusCodeError("Error Status Code al solicitar custodias: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("Error inesperado al solicitar autoridades") from error
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total en la respuesta al solicitar inventarios custodias")
    return data_json
