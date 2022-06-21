"""
Listas de Acuerdos
"""
import click
import pandas as pd
import requests
from tabulate import tabulate

from cli.commands.autentificar import autentificar, BASE_URL


def get_listas_de_acuerdos(authorization_header, fecha=None):
    """Consultar las listas de acuerdos"""
    params = {}
    if fecha is not None and fecha != "":
        params["fecha"] = fecha
    try:
        response = requests.get(
            f"{BASE_URL}/v1/listas_de_acuerdos",
            headers=authorization_header,
            params=params,
            timeout=12,
        )
    except requests.exceptions.RequestException as error:
        raise error
    if response.status_code != 200:
        raise requests.HTTPError(response.status_code)
    data_json = response.json()  # Items, total, limit, offset
    if "items" not in data_json or "total" not in data_json:
        raise ValueError("Error porque la respuesta de la API no es correcta")
    total = data_json["total"]
    if total > 0:
        dataframe = pd.json_normalize(data_json["items"])
        columns = ["distrito_nombre_corto", "autoridad_clave", "fecha", "descripcion", "archivo"]
        dataframe = dataframe[columns]
        return dataframe, columns, total
    return None, None, total


@click.group()
@click.option("--fecha", default="", type=str, help="Fecha a consultar")
@click.pass_context
def cli(ctx, fecha):
    """Listas de Acuerdos"""
    ctx.obj = {}
    ctx.obj["fecha"] = fecha


@click.command()
@click.pass_context
def enviar(ctx):
    """Enviar"""


@click.command()
@click.option("--output", default="inv_equipos.csv", type=str, help="Archivo CSV a escribir")
@click.pass_context
def guardar(ctx, output):
    """Guardar"""


@click.command()
@click.pass_context
def ver(ctx):
    """Ver listas de acuerdos en la terminal"""
    try:
        token = autentificar()
        authorization_header = {"Authorization": "Bearer " + token}
        sentencias, columns, total = get_listas_de_acuerdos(
            authorization_header,
            fecha=ctx.obj["fecha"],
        )
        if total == 0:
            print("No hay sentencias")
        else:
            print(tabulate(sentencias, headers=columns))
    except requests.HTTPError as error:
        print("Error de comunicacion " + str(error))


cli.add_command(enviar)
cli.add_command(guardar)
cli.add_command(ver)
