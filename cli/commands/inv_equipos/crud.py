"""
Inv Equipos CRUD (create, read, update, and delete)
"""
from datetime import date
from typing import Any

import requests

from config.settings import BASE_URL, LIMIT, TIMEOUT
import lib.exceptions


def get_inv_equipos(
    authorization_header: dict,
    limit: int = LIMIT,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    fecha_fabricacion_desde: date = None,
    fecha_fabricacion_hasta: date = None,
    inv_custodia_id: int = None,
    inv_modelo_id: int = None,
    inv_red_id: int = None,
) -> Any:
    """Solicitar inventarios equipos"""
    parametros = {"limit": limit}
    if creado is not None:
        parametros["creado"] = creado
    if creado_desde is not None:
        parametros["creado_desde"] = creado_desde
    if creado_hasta is not None:
        parametros["creado_hasta"] = creado_hasta
    if fecha_fabricacion_desde is not None:
        parametros["fecha_fabricacion_desde"] = fecha_fabricacion_desde
    if fecha_fabricacion_hasta is not None:
        parametros["fecha_fabricacion_hasta"] = fecha_fabricacion_hasta
    if inv_custodia_id is not None:
        parametros["inv_custodia_id"] = inv_custodia_id
    if inv_modelo_id is not None:
        parametros["inv_modelo_id"] = inv_modelo_id
    if inv_red_id is not None:
        parametros["inv_red_id"] = inv_red_id
    try:
        response = requests.get(
            f"{BASE_URL}/inv_equipos",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("No hay respuesta al solicitar inventarios equipos") from error
    if response.status_code != 200:
        raise lib.exceptions.CLIStatusCodeError(f"No es lo esperado el status code: {response.status_code} al solicitar inventarios equipos\nmensaje: {response.text}")
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total en la respuesta al solicitar inventarios equipos")
    return data_json
