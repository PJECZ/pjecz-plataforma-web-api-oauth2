"""
Autentificar

Debe de tener un archivo .env con las variables de entorno:

    BASE_URL=http://127.0.0.1:8002
    USERNAME=nombre.apellido@pjecz.gob.mx
    PASSWORD=UnaContrasenaMuyDificil

"""
import os

from dotenv import load_dotenv
import requests

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


def autentificar():
    """Autentificarse y obtener el token"""
    if BASE_URL is None:
        raise Exception("Error de configuracion: Falta BASE_URL")
    if USERNAME is None:
        raise Exception("Error de configuracion: Falta USERNAME")
    if PASSWORD is None:
        raise Exception("Error de configuracion: Falta PASSWORD")
    data = {"username": USERNAME, "password": PASSWORD}
    headers = {"content-type": "application/x-www-form-urlencoded"}
    response = requests.post(f"{BASE_URL}/token", data=data, headers=headers)
    if response.status_code != 200:
        raise requests.HTTPError(response.status_code)
    return response.json()["access_token"]
