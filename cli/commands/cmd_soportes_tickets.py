"""
Soportes tickets
"""
import click
import pandas as pd
import requests
from tabulate import tabulate

from cli.commands.autentificar import autentificar, BASE_URL


def get_soportes_tickets(authorization_header, creado=None, creado_desde=None, creado_hasta=None, estado=None):
    """Consultar tickets"""
    params = {"limit": 1000}
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
            f"{BASE_URL}/v1/soportes_tickets",
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
        columns = ["id", "funcionario_nombre", "soporte_categoria_nombre", "usuario_nombre", "usuario_oficina_clave", "estado"]
        dataframe = dataframe[columns]
        return dataframe, columns, total
    return None, None, total


@click.group()
@click.option("--creado", default="", type=str, help="Fecha de creacion")
@click.option("--creado-desde", default="", type=str, help="Fecha desde")
@click.option("--creado-hasta", default="", type=str, help="Fecha hasta")
@click.option("--estado", default="", type=str, help="Estado")
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
    total = 0
    try:
        soportes_tickets, columns, total = get_soportes_tickets(
            autentificar(),
            creado=ctx.obj["creado"],
            creado_desde=ctx.obj["creado_desde"],
            creado_hasta=ctx.obj["creado_hasta"],
            estado=ctx.obj["estado"],
        )
    except requests.HTTPError as error:
        click.echo("Error de comunicacion " + str(error))
        return
    if total == 0:
        click.echo("No hay tickets")
        return
    soportes_tickets.to_excel(output)
    click.echo(f"Listo el archivo {output}")


@click.command()
@click.pass_context
def ver(ctx):
    """Ver tickets en la terminal"""
    total = 0
    try:
        soportes_tickets, columns, total = get_soportes_tickets(
            autentificar(),
            creado=ctx.obj["creado"],
            creado_desde=ctx.obj["creado_desde"],
            creado_hasta=ctx.obj["creado_hasta"],
            estado=ctx.obj["estado"],
        )
    except requests.HTTPError as error:
        click.echo("Error de comunicacion " + str(error))
        return
    if total == 0:
        click.echo("No hay tickets")
        return
    click.echo(tabulate(soportes_tickets, headers=columns))


cli.add_command(enviar)
cli.add_command(guardar)
cli.add_command(ver)
