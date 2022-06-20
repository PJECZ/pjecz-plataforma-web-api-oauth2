"""
Soportes tickets
"""
import click
import pandas as pd
import requests
from tabulate import tabulate

from cli.commands.autentificar import autentificar, BASE_URL


def get_cantidades_distrito_categoria(authorization_header, estado, creado_desde, creado_hasta):
    """Obtener el reporte de soportes tickets"""
    try:
        response = requests.get(
            f"{BASE_URL}/v1/soportes_tickets/cantidades_distrito_categoria",
            headers=authorization_header,
            params={"estado": estado, "creado_desde": creado_desde, "creado_hasta": creado_hasta},
            timeout=12,
        )
    except requests.exceptions.RequestException as error:
        raise error
    if response.status_code != 200:
        raise requests.HTTPError(response.status_code)
    data_json = response.json()  # Listado con distrito_clave, soporte_categoria_nombre y cantidad
    dataframe = pd.json_normalize(data_json)
    if dataframe.size > 0:
        dataframe.distrito_clave = dataframe.distrito_clave.astype("category")
        dataframe.soporte_categoria_nombre = dataframe.soporte_categoria_nombre.astype("category")
        reporte = dataframe.pivot_table(
            index=["soporte_categoria_nombre"],
            columns=["distrito_clave"],
            values="cantidad",
        )
        return reporte, ["CATEGORIA"] + list(dataframe["distrito_clave"].cat.categories)
    return None, None


@click.group()
@click.option("--creado-desde", default="", type=str, help="Fecha desde")
@click.option("--creado-hasta", default="", type=str, help="Fecha hasta")
@click.option("--estado", default="terminado", type=str, help="Estado")
@click.pass_context
def cli(ctx, creado_desde, creado_hasta, estado):
    """Soportes tickets"""
    ctx.obj = {}
    ctx.obj["creado_desde"] = creado_desde
    ctx.obj["creado_hasta"] = creado_hasta
    ctx.obj["estado"] = estado


@click.command()
@click.pass_context
def enviar(ctx):
    """Enviar mensaje"""


@click.command()
@click.option("--output", default="inv_equipos.csv", type=str, help="Archivo CSV a escribir")
@click.pass_context
def guardar(ctx, output):
    """Enviar mensaje"""


@click.command()
@click.pass_context
def ver(ctx):
    """Ver reporte de tickets en la terminal"""
    try:
        token = autentificar()
        authorization_header = {"Authorization": "Bearer " + token}
        cantidades_distrito_categoria, columns = get_cantidades_distrito_categoria(
            authorization_header,
            creado_desde=ctx.obj["creado_desde"],
            creado_hasta=ctx.obj["creado_hasta"],
            estado=ctx.obj["estado"],
        )
        if cantidades_distrito_categoria is None:
            print("No hay soportes tickets")
        else:
            print(tabulate(cantidades_distrito_categoria, headers=columns))
    except requests.HTTPError as error:
        print("Error de comunicacion " + str(error))


cli.add_command(enviar)
cli.add_command(ver)
