"""
Autoridades CRUD (create, read, update, and delete)
"""
from typing import Any

import requests

from config.settings import BASE_URL, LIMIT, TIMEOUT
import lib.exceptions


def get_autoridades(
    authorization_header: dict,
    limit: int = LIMIT,
    distrito_id: int = None,
    materia_id: int = None,
) -> Any:
    """Solicitar autoridades"""
    parametros = {"limit": limit}
    if distrito_id is not None:
        parametros["distrito_id"] = distrito_id
    if materia_id is not None:
        parametros["materia_id"] = materia_id
    try:
        response = requests.get(
            f"{BASE_URL}/autoridades",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("No hay respuesta al solicitar autoridades") from error
    if response.status_code != 200:
        raise lib.exceptions.CLIStatusCodeError(f"No es lo esperado el status code: {response.status_code} al solicitar autoridades\nmensaje: {response.text}")
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total en la respuesta al solicitar autoridades")
    return data_json
