"""
Inventarios Equipos
"""
import click
import openpyxl
import pandas as pd
import requests
from tabulate import tabulate

from cli.commands.autentificar import autentificar, BASE_URL


def get_cantidades_oficina_tipo(authorization_header, creado=None, creado_desde=None, creado_hasta=None):
    """Consultar las cantidades de equipos por oficina y por tipo"""
    params = {"limit": 1000}
    if creado is not None and creado != "":
        params["creado"] = creado
    if creado_desde is not None and creado_desde != "":
        params["creado_desde"] = creado_desde
    if creado_hasta is not None and creado_hasta != "":
        params["creado_hasta"] = creado_hasta
    try:
        response = requests.get(
            f"{BASE_URL}/v1/inv_equipos/cantidades_oficina_tipo",
            headers=authorization_header,
            params=params,
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
@click.option("--creado", default="", type=str, help="Fecha de creacion")
@click.option("--creado-desde", default="", type=str, help="Fecha desde")
@click.option("--creado-hasta", default="", type=str, help="Fecha hasta")
@click.pass_context
def cli(ctx, creado, creado_desde, creado_hasta):
    """Cantidades de Equipos en Inventarios"""
    ctx.obj = {}
    ctx.obj["creado"] = creado
    ctx.obj["creado_desde"] = creado_desde
    ctx.obj["creado_hasta"] = creado_hasta


@click.command()
@click.pass_context
def enviar(ctx):
    """Enviar"""


@click.command()
@click.argument("output", type=str)
@click.pass_context
def guardar(ctx, output):
    """Guardar"""
    total = 0
    try:
        token = autentificar()
        authorization_header = {"Authorization": "Bearer " + token}
        cantidades_oficina_tipo, columns, total = get_cantidades_oficina_tipo(
            authorization_header,
            creado=ctx.obj["creado"],
            creado_desde=ctx.obj["creado_desde"],
            creado_hasta=ctx.obj["creado_hasta"],
        )
    except requests.HTTPError as error:
        click.echo("Error de comunicacion " + str(error))
    if total == 0:
        click.echo("No hay equipos")
    else:
        cantidades_oficina_tipo.to_excel(output)
        click.echo(f"Listo el archivo {output}")


@click.command()
@click.pass_context
def ver(ctx):
    """Ver inventario de equipos en la terminal"""
    total = 0
    try:
        token = autentificar()
        authorization_header = {"Authorization": "Bearer " + token}
        cantidades_oficina_tipo, columns, total = get_cantidades_oficina_tipo(
            authorization_header,
            creado=ctx.obj["creado"],
            creado_desde=ctx.obj["creado_desde"],
            creado_hasta=ctx.obj["creado_hasta"],
        )
    except requests.HTTPError as error:
        click.echo("Error de comunicacion " + str(error))
    if total == 0:
        click.echo("No hay equipos")
    else:
        click.echo(tabulate(cantidades_oficina_tipo, headers=columns))


cli.add_command(enviar)
cli.add_command(guardar)
cli.add_command(ver)
