"""
Inventarios
"""
import click
import pandas as pd
import requests
from tabulate import tabulate

from cli.commands.autentificar import autentificar, BASE_URL


def get_cantidades_oficina_tipo(authorization_header):
    """Consultar las cantidades de equipos por oficina y por tipo"""
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
    data_json = response.json()  # Listado con inv_equipo_tipo, oficina_clave y cantidad
    dataframe = pd.json_normalize(data_json)
    total = dataframe.size
    if total > 0:
        dataframe.oficina_clave = dataframe.oficina_clave.astype("category")
        dataframe.inv_equipo_tipo = dataframe.inv_equipo_tipo.astype("category")
        reporte = dataframe.pivot_table(
            index=["oficina_clave"],
            columns=["inv_equipo_tipo"],
            values="cantidad",
        )
        return reporte, ["OFICINA"] + list(dataframe.inv_equipo_tipo), total
    return None, None, total


@click.group()
def cli():
    """Inventarios Equipos"""


@click.command()
def enviar():
    """Enviar"""


@click.command()
@click.option("--output", default="inv_equipos.csv", type=str, help="Archivo CSV a escribir")
def guardar(output):
    """Guardar"""


@click.command()
def ver():
    """Ver inventario de equipos en la terminal"""
    try:
        token = autentificar()
        authorization_header = {"Authorization": "Bearer " + token}
        cantidades_oficina_tipo, columns, total = get_cantidades_oficina_tipo(authorization_header)
        if total == 0:
            print("No hay equipos")
        else:
            print(tabulate(cantidades_oficina_tipo, headers=columns))
    except requests.HTTPError as error:
        print("ERROR de comunicacion " + str(error))


cli.add_command(enviar)
cli.add_command(guardar)
cli.add_command(ver)
