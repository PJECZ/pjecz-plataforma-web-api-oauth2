"""
Sentencias CRUD (create, read, update, and delete)
"""
from datetime import date
from typing import Any

import requests

from config.settings import BASE_URL, LIMIT, TIMEOUT
import lib.exceptions


def get_sentencias(
    authorization_header: dict,
    limit: int = LIMIT,
    autoridad_id: int = None,
    autoridad_clave: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    materia_tipo_juicio_id: int = None,
    fecha: date = None,
    fecha_desde: date = None,
    fecha_hasta: date = None,
) -> Any:
    """Solicitar sentencias"""
    parametros = {"limit": limit}
    if autoridad_id is not None:
        parametros["autoridad_id"] = autoridad_id
    if autoridad_clave is not None:
        parametros["autoridad_clave"] = autoridad_clave
    if creado is not None:
        parametros["creado"] = creado
    if creado_desde is not None:
        parametros["creado_desde"] = creado_desde
    if creado_hasta is not None:
        parametros["creado_hasta"] = creado_hasta
    if materia_tipo_juicio_id is not None:
        parametros["materia_tipo_juicio_id"] = materia_tipo_juicio_id
    if fecha is not None:
        parametros["fecha"] = fecha
    if fecha_desde is not None:
        parametros["fecha_desde"] = fecha_desde
    if fecha_hasta is not None:
        parametros["fecha_hasta"] = fecha_hasta
    try:
        response = requests.get(
            f"{BASE_URL}/sentencias",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
    except requests.exceptions.ConnectionError as error:
        raise lib.exceptions.CLIStatusCodeError("No hubo respuesta al solicitar sentencias") from error
    except requests.exceptions.HTTPError as error:
        raise lib.exceptions.CLIStatusCodeError("Error Status Code al solicitar sentencias: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("Error inesperado al solicitar sentencias") from error
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total en la respuesta al solicitar sentencias")
    return data_json
