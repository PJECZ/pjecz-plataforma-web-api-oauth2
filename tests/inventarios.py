"""
Inventarios

Prueba de llamado a la API OAuth2

Escriba un archivo .env con las variables de entorno:

    BASE_URL=http://127.0.0.1:8002
    USERNAME=nombre.apellido@pjecz.gob.mx
    PASSWORD=UnaContrasenaMuyDificil

"""
import pandas as pd
import requests
from tabulate import tabulate

from tests.authenticate import BASE_URL, authenticate


def get_matriz(authorization_header):
    """Matriz"""
    try:
        response = requests.get(
            f"{BASE_URL}/v1/inv_equipos/matriz",
            headers=authorization_header,
            timeout=12,
        )
    except requests.exceptions.RequestException as error:
        raise error
    if response.status_code != 200:
        raise requests.HTTPError(response.status_code)
    data_json = response.json()
    dataframe = pd.json_normalize(data_json)
    return dataframe


def get_cantidades_oficina_tipo(authorization_header):
    """Obtener las cantidades de equipos por oficina y por tipo"""
    try:
        response = requests.get(
            f"{BASE_URL}/v1/inv_equipos/cantidades_oficina_tipo",
            headers=authorization_header,
            timeout=12,
        )
    except requests.exceptions.RequestException as error:
        raise error
    if response.status_code != 200:
        raise requests.HTTPError(response.status_code)
    data_json = response.json()
    dataframe = pd.json_normalize(data_json)
    dataframe.oficina_clave = dataframe.oficina_clave.astype("category")
    dataframe.inv_equipo_tipo = dataframe.inv_equipo_tipo.astype("category")
    reporte = dataframe.pivot_table(
        index=["oficina_clave"],
        columns=["inv_equipo_tipo"],
        values="cantidad",
    )
    return reporte, ["OFICINA"] + list(dataframe.inv_equipo_tipo)


def main():
    """Main function"""
    try:
        token = authenticate()
        authorization_header = {"Authorization": "Bearer " + token}
        cantidades_oficina_tipo, columns = get_cantidades_oficina_tipo(authorization_header)
        print(tabulate(cantidades_oficina_tipo, headers=columns))
    except requests.HTTPError as error:
        print("Error de comunicacion " + str(error))
    except Exception as error:
        print(str(error))


if __name__ == "__main__":
    main()
