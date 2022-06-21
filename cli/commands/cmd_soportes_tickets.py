"""
Soportes tickets
"""
import click
import pandas as pd
import requests
from tabulate import tabulate

from cli.commands.autentificar import autentificar, BASE_URL


def get_cantidades_distrito_categoria(authorization_header, creado=None, creado_desde=None, creado_hasta=None, estado=None):
    """Consultar las cantidades de tickets por distrito y por categoria"""
    params = {}
    if creado is not None and creado != "":
        params["creado"] = creado
    if creado_desde is not None and creado_desde != "":
        params["creado_desde"] = creado_desde
    if creado_hasta is not None and creado_hasta != "":
        params["creado_hasta"] = creado_hasta
    if estado is not None and estado != "":
        params["estado"] = estado
    try:
        response = requests.get(
            f"{BASE_URL}/v1/soportes_tickets/cantidades_distrito_categoria",
            headers=authorization_header,
            params=params,
            timeout=12,
        )
    except requests.exceptions.RequestException as error:
        raise error
    if response.status_code != 200:
        raise requests.HTTPError(response.status_code)
    data_json = response.json()  # Listado con distrito_clave, soporte_categoria_nombre y cantidad
    dataframe = pd.json_normalize(data_json)
    total = dataframe.size
    if total > 0:
        dataframe.distrito_clave = dataframe.distrito_clave.astype("category")
        dataframe.soporte_categoria_nombre = dataframe.soporte_categoria_nombre.astype("category")
        reporte = dataframe.pivot_table(
            index=["soporte_categoria_nombre"],
            columns=["distrito_clave"],
            values="cantidad",
        )
        return reporte, ["CATEGORIA"] + list(dataframe["distrito_clave"].cat.categories), total
    return None, None, total


@click.group()
@click.option("--creado", default="", type=str, help="Fecha de creacion")
@click.option("--creado-desde", default="", type=str, help="Fecha desde")
@click.option("--creado-hasta", default="", type=str, help="Fecha hasta")
@click.option("--estado", default="terminado", type=str, help="Estado")
@click.pass_context
def cli(ctx, creado, creado_desde, creado_hasta, estado):
    """Soportes tickets"""
    ctx.obj = {}
    ctx.obj["creado"] = creado
    ctx.obj["creado_desde"] = creado_desde
    ctx.obj["creado_hasta"] = creado_hasta
    ctx.obj["estado"] = estado


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
    """Ver tickets en la terminal"""
    try:
        token = autentificar()
        authorization_header = {"Authorization": "Bearer " + token}
        cantidades_distrito_categoria, columns, total = get_cantidades_distrito_categoria(
            authorization_header,
            creado=ctx.obj["creado"],
            creado_desde=ctx.obj["creado_desde"],
            creado_hasta=ctx.obj["creado_hasta"],
            estado=ctx.obj["estado"],
        )
        if total == 0:
            print("No hay tickets")
        else:
            print(tabulate(cantidades_distrito_categoria, headers=columns))
    except requests.HTTPError as error:
        print("Error de comunicacion " + str(error))


cli.add_command(enviar)
cli.add_command(guardar)
cli.add_command(ver)
