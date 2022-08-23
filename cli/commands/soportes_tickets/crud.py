"""
Soportes Tickets CRUD (create, read, update, and delete)
"""
from typing import Any

import requests

from config.settings import BASE_URL, LIMIT, TIMEOUT
import lib.exceptions


def get_soportes_tickets(
    authorization_header: dict,
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
    descripcion: str = None,
    estado: str = None,
    limit: int = LIMIT,
    oficina_id: int = None,
    oficina_clave: str = None,
    offset: int = 0,
    soporte_categoria_id: int = None,
    usuario_id: int = None,
    usuario_email: str = None,
) -> Any:
    """Solicitar tickets de soporte"""
    parametros = {"limit": limit}
    if creado is not None:
        parametros["creado"] = creado
    if creado_desde is not None:
        parametros["creado_desde"] = creado_desde
    if creado_hasta is not None:
        parametros["creado_hasta"] = creado_hasta
    if descripcion is not None:
        parametros["descripcion"] = descripcion
    if estado is not None:
        parametros["estado"] = estado
    if oficina_id is not None:
        parametros["oficina_id"] = oficina_id
    if oficina_clave is not None:
        parametros["oficina_clave"] = oficina_clave
    if offset > 0:
        parametros["offset"] = offset
    if soporte_categoria_id is not None:
        parametros["soporte_categoria_id"] = soporte_categoria_id
    if usuario_id is not None:
        parametros["usuario_id"] = usuario_id
    if usuario_email is not None:
        parametros["usuario_email"] = usuario_email
    try:
        response = requests.get(
            f"{BASE_URL}/soportes_tickets",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise lib.exceptions.CLIStatusCodeError("No hubo respuesta al solicitar tickets") from error
    except requests.exceptions.HTTPError as error:
        raise lib.exceptions.CLIStatusCodeError("Error Status Code al solicitar tickets: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("Error inesperado al solicitar tickets") from error
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise lib.exceptions.CLIResponseError("No se recibio items o total en la respuesta al solicitar tickets")
    return data_json


def get_soportes_tickets_cantidades_por_distrito_por_categoria(
    authorization_header: dict,
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
):
    """Solicitar cantidades de tickets de soportes por distritos y por categorias"""
    parametros = {}
    if creado is not None:
        parametros["creado"] = creado
    if creado_desde is not None:
        parametros["creado_desde"] = creado_desde
    if creado_hasta is not None:
        parametros["creado_hasta"] = creado_hasta
    try:
        response = requests.get(
            f"{BASE_URL}/soportes_tickets/cantidades_por_distrito_por_categoria",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise lib.exceptions.CLIStatusCodeError("No hubo respuesta al solicitar tickets") from error
    except requests.exceptions.HTTPError as error:
        raise lib.exceptions.CLIStatusCodeError("Error Status Code al solicitar tickets: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("Error inesperado al solicitar tickets") from error
    data_json = response.json()
    return data_json


def get_soportes_tickets_cantidades_por_funcionario_por_estado(
    authorization_header: dict,
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
):
    """Solicitar cantidades de tickets de soportes por funcionarios y por estados"""
    parametros = {}
    if creado is not None:
        parametros["creado"] = creado
    if creado_desde is not None:
        parametros["creado_desde"] = creado_desde
    if creado_hasta is not None:
        parametros["creado_hasta"] = creado_hasta
    try:
        response = requests.get(
            f"{BASE_URL}/soportes_tickets/cantidades_por_funcionario_por_estado",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise lib.exceptions.CLIStatusCodeError("No hubo respuesta al solicitar tickets") from error
    except requests.exceptions.HTTPError as error:
        raise lib.exceptions.CLIStatusCodeError("Error Status Code al solicitar tickets: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("Error inesperado al solicitar tickets") from error
    data_json = response.json()
    return data_json
