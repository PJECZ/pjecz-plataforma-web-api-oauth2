"""
Inventarios Equipos
"""
import click
import pandas as pd
import requests
from tabulate import tabulate

from cli.commands.autentificar import autentificar, BASE_URL


def get_inv_equipos(authorization_header, creado=None, creado_desde=None, creado_hasta=None):
    """Consultar equipos"""
    params = {"limit": 1000}
    if creado is not None and creado != "":
        params["creado"] = creado
    if creado_desde is not None and creado_desde != "":
        params["creado_desde"] = creado_desde
    if creado_hasta is not None and creado_hasta != "":
        params["creado_hasta"] = creado_hasta
    try:
        response = requests.get(
            f"{BASE_URL}/v1/inv_equipos",
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
        columns = ["id", "inv_custodia_nombre_completo", "inv_marca_nombre", "inv_modelo_descripcion", "fecha_fabricacion", "numero_serie", "numero_inventario", "descripcion", "tipo"]
        dataframe = dataframe[columns]
        return dataframe, columns, total
    return None, None, total


@click.group()
@click.option("--creado", default="", type=str, help="Fecha de creacion")
@click.option("--creado-desde", default="", type=str, help="Fecha desde")
@click.option("--creado-hasta", default="", type=str, help="Fecha hasta")
@click.pass_context
def cli(ctx, creado, creado_desde, creado_hasta):
    """Inventarios Equipos"""
    ctx.obj = {}
    ctx.obj["creado"] = creado
    ctx.obj["creado_desde"] = creado_desde
    ctx.obj["creado_hasta"] = creado_hasta


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
    """Ver inventario de equipos en la terminal"""
    try:
        token = autentificar()
        authorization_header = {"Authorization": "Bearer " + token}
        cantidades_oficina_tipo, columns, total = get_inv_equipos(
            authorization_header,
            creado=ctx.obj["creado"],
            creado_desde=ctx.obj["creado_desde"],
            creado_hasta=ctx.obj["creado_hasta"],
        )
        if total == 0:
            print("No hay equipos")
        else:
            print(tabulate(cantidades_oficina_tipo, headers=columns))
    except requests.HTTPError as error:
        print("ERROR de comunicacion " + str(error))


cli.add_command(enviar)
cli.add_command(guardar)
cli.add_command(ver)
