"""
Materias CRUD (create, read, update, and delete)
"""
from typing import Any
import requests

from config.settings import BASE_URL, LIMIT, TIMEOUT
import lib.exceptions


def get_materias(
    authorization_header: dict,
    limit: int = LIMIT,
) -> Any:
    """Solicitar materias"""
    parametros = {"limit": limit}
    try:
        response = requests.get(
            f"{BASE_URL}/materias",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("No hay respuesta al solicitar materias") from error
    if response.status_code != 200:
        raise lib.exceptions.CLIStatusCodeError(f"No es lo esperado el status code: {response.status_code} al solicitar materias\nmensaje: {response.text}")
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total en la respuesta al solicitar materias")
    return data_json
