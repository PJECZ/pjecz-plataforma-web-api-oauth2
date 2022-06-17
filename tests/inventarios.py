"""
Inventarios

Escriba un archivo .env con las variables de entorno:

    BASE_URL=http://127.0.0.1:8002
    USERNAME=nombre.apellido@pjecz.gob.mx
    PASSWORD=UnaContrasenaMuyDificil

"""
import os

from dotenv import load_dotenv
import pandas as pd
import requests

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


def authenticate():
    """Autentificarse y obtener el token"""
    data = {"username": USERNAME, "password": PASSWORD}
    headers = {"content-type": "application/x-www-form-urlencoded"}
    response = requests.post(f"{BASE_URL}/token", data=data, headers=headers)
    if response.status_code == 200:
        return response.json()["access_token"]
    return None


def get_matriz(authorization_header):
    """Matriz"""
    try:
        response = requests.get(f"{BASE_URL}/v1/inv_equipos/matriz", headers=authorization_header, timeout=12)
    except requests.exceptions.RequestException as error:
        raise error
    if response.status_code != 200:
        raise requests.HTTPError(response.status_code)
    return response.json()


def main():
    """Main function"""
    # Authenticate
    token = authenticate()
    if token is None:
        print("Error al autenticarse")
        return
    authorization_header = {"Authorization": "Bearer " + token}
    # Matriz
    matriz = get_matriz(authorization_header)
    dataframe = pd.json_normalize(matriz)
    dataframe.oficina_clave = dataframe.oficina_clave.astype("category")
    dataframe.inv_equipo_tipo = dataframe.inv_equipo_tipo.astype("category")
    print(dataframe.info())
    # reporte = dataframe.pivot_table(
    #     index=["oficina_clave"],
    #     columns=["inv_equipo_tipo"],
    #     values="cantidad",
    # )


if __name__ == "__main__":
    main()
