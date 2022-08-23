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
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    fecha_fabricacion_desde: date = None,
    fecha_fabricacion_hasta: date = None,
    inv_custodia_id: int = None,
    inv_modelo_id: int = None,
    inv_red_id: int = None,
    limit: int = LIMIT,
    offset: int = 0,
    oficina_id: int = None,
    oficina_clave: str = None,
    tipo: str = None,
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
    if offset > 0:
        parametros["offset"] = offset
    if oficina_id is not None:
        parametros["oficina_id"] = oficina_id
    if oficina_clave is not None:
        parametros["oficina_clave"] = oficina_clave
    if tipo is not None:
        parametros["tipo"] = tipo
    try:
        response = requests.get(
            f"{BASE_URL}/inv_equipos",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise lib.exceptions.CLIStatusCodeError("No hubo respuesta al solicitar equipos") from error
    except requests.exceptions.HTTPError as error:
        raise lib.exceptions.CLIStatusCodeError("Error Status Code al solicitar equipos: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("Error inesperado al solicitar equipos") from error
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total en la respuesta al solicitar equipos")
    return data_json


def get_inv_equipos_cantidades_por_oficina_por_tipo(
    authorization_header: dict,
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
) -> Any:
    """Obtener cantidades de equipos por oficina y tipo"""
    parametros = {}
    if creado is not None:
        parametros["creado"] = creado
    if creado_desde is not None:
        parametros["creado_desde"] = creado_desde
    if creado_hasta is not None:
        parametros["creado_hasta"] = creado_hasta
    try:
        response = requests.get(
            f"{BASE_URL}/inv_equipos/cantidades_por_oficina_por_tipo",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise lib.exceptions.CLIStatusCodeError("No hubo respuesta al solicitar equipos") from error
    except requests.exceptions.HTTPError as error:
        raise lib.exceptions.CLIStatusCodeError("Error Status Code al solicitar equipos: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("Error inesperado al solicitar equipos") from error
    data_json = response.json()
    return data_json


def get_inv_equipos_cantidades_por_oficina_por_anio_fabricacion(
    authorization_header: dict,
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
    distrito_id: int = None,
    tipo: str = None,
) -> Any:
    """Obtener cantidades de equipos por oficina y año de fabricacion"""
    parametros = {}
    if creado is not None:
        parametros["creado"] = creado
    if creado_desde is not None:
        parametros["creado_desde"] = creado_desde
    if creado_hasta is not None:
        parametros["creado_hasta"] = creado_hasta
    if distrito_id is not None:
        parametros["distrito_id"] = distrito_id
    if tipo is not None:
        parametros["tipo"] = tipo
    try:
        response = requests.get(
            f"{BASE_URL}/inv_equipos/cantidades_por_oficina_por_anio_fabricacion",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise lib.exceptions.CLIStatusCodeError("No hubo respuesta al solicitar equipos") from error
    except requests.exceptions.HTTPError as error:
        raise lib.exceptions.CLIStatusCodeError("Error Status Code al solicitar equipos: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("Error inesperado al solicitar equipos") from error
    data_json = response.json()
    return data_json
