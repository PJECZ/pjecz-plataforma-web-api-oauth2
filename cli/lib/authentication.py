"""
CLI Connections
"""
import requests

from config.settings import HOST, USERNAME, PASSWORD
import lib.exceptions


def authorization_header() -> dict:
    """Definir la cabecera para autentificarse en cada solicitud a la API"""
    if HOST == "":
        raise lib.exceptions.CLIConfigurationError("No se ha definido el host")
    if USERNAME == "":
        raise lib.exceptions.CLIConfigurationError("No se ha definido el usuario")
    if PASSWORD == "":
        raise lib.exceptions.CLIConfigurationError("No se ha definido la contraseña")
    data = {"username": USERNAME, "password": PASSWORD}
    headers = {"content-type": "application/x-www-form-urlencoded"}
    try:
        response = requests.post(f"{HOST}/token", data=data, headers=headers)
    except requests.exceptions.RequestException as error:
        raise lib.exceptions.CLIConnectionError("No hay respuesta al tratar de autentificar") from error
    if response.status_code != 200:
        raise lib.exceptions.CLIStatusCodeError(f"No es lo esperado el status code: {response.status_code}")
    data_json = response.json()
    if not "access_token" in data_json:
        raise lib.exceptions.CLIAuthenticationError("No se recibio el access_token en la respuesta")
    return {"Authorization": "Bearer " + data_json["access_token"]}
