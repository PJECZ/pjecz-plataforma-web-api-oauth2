"""
Inv Modelos CRUD (create, read, update, and delete)
"""
from typing import Any

import requests

from config.settings import BASE_URL, LIMIT, TIMEOUT
import lib.exceptions


def get_inv_modelos(
    authorization_header: dict,
    limit: int = LIMIT,
    inv_marca_id: int = None,
) -> Any:
    """Solicitar modelos"""
    parametros = {"limit": limit}
    if inv_marca_id is not None:
        parametros["inv_marca_id"] = inv_marca_id
    try:
        response = requests.get(
            f"{BASE_URL}/inv_modelos",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("No hay respuesta al solicitar modelos") from error
    if response.status_code != 200:
        raise lib.exceptions.CLIStatusCodeError(f"No es lo esperado el status code: {response.status_code} al solicitar modelos\nmensaje: {response.text}")
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total en la respuesta al solicitar modelos")
    return data_json
