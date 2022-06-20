"""
Soportes Tickets

Prueba de llamado a la API OAuth2

Escriba un archivo .env con las variables de entorno:

    BASE_URL=http://127.0.0.1:8002
    USERNAME=nombre.apellido@pjecz.gob.mx
    PASSWORD=UnaContrasenaMuyDificil

"""
import os

from dotenv import load_dotenv
import pandas as pd
import requests
from tabulate import tabulate

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


def authenticate():
    """Autentificarse y obtener el token"""
    if BASE_URL is None or USERNAME is None or PASSWORD is None:
        raise Exception("Error de configuracion.")
    data = {"username": USERNAME, "password": PASSWORD}
    headers = {"content-type": "application/x-www-form-urlencoded"}
    response = requests.post(f"{BASE_URL}/token", data=data, headers=headers)
    if response.status_code != 200:
        raise requests.HTTPError(response.status_code)
    return response.json()["access_token"]


def get_cantidades_distrito_categoria(authorization_header):
    """Obtener el reporte de soportes tickets"""
    try:
        response = requests.get(f"{BASE_URL}/v1/soportes_tickets/cantidades_distrito_categoria", headers=authorization_header, timeout=12)
    except requests.exceptions.RequestException as error:
        raise error
    if response.status_code != 200:
        raise requests.HTTPError(response.status_code)
    data_json = response.json()
    dataframe = pd.json_normalize(data_json)
    dataframe.distrito_clave = dataframe.distrito_clave.astype("category")
    dataframe.soporte_categoria_nombre = dataframe.soporte_categoria_nombre.astype("category")
    reporte = dataframe.pivot_table(
        index=["soporte_categoria_nombre"],
        columns=["distrito_clave"],
        values="cantidad",
    )
    return reporte, ["DISTRITO"] + list(dataframe.distrito_clave)


def main():
    """Main function"""
    try:
        token = authenticate()
        authorization_header = {"Authorization": "Bearer " + token}
        cantidades_distrito_categoria, columns = get_cantidades_distrito_categoria(authorization_header)
        print(tabulate(cantidades_distrito_categoria, headers=columns))
    except requests.HTTPError as error:
        print("Error de comunicacion " + str(error))
    except Exception as error:
        print(str(error))


if __name__ == "__main__":
    main()
