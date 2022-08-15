"""
Sentencias
"""
import click
import pandas as pd
import requests
from tabulate import tabulate

from cli.commands.autentificar import autentificar, BASE_URL


def get_sentencias(authorization_header, creado=None, creado_desde=None, creado_hasta=None, fecha=None):
    """Consultar sentencias"""
    params = {"limit": 1000}
    if creado is not None and creado != "":
        params["creado"] = creado
    if creado_desde is not None and creado_desde != "":
        params["creado_desde"] = creado_desde
    if creado_hasta is not None and creado_hasta != "":
        params["creado_hasta"] = creado_hasta
    if fecha is not None and fecha != "":
        params["fecha"] = fecha
    try:
        response = requests.get(
            f"{BASE_URL}/v1/sentencias",
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
        columns = ["id", "autoridad_clave", "materia_tipo_juicio_descripcion", "sentencia", "sentencia_fecha", "fecha", "expediente", "es_perspectiva_genero"]
        dataframe = dataframe[columns]
        return dataframe, columns, total
    return None, None, total


@click.group()
@click.option("--creado", default="", type=str, help="Fecha de creacion")
@click.option("--creado-desde", default="", type=str, help="Fecha desde")
@click.option("--creado-hasta", default="", type=str, help="Fecha hasta")
@click.option("--fecha", default="", type=str, help="Fecha a consultar")
@click.pass_context
def cli(ctx, creado, creado_desde, creado_hasta, fecha):
    """Sentencias"""
    ctx.obj = {}
    ctx.obj["creado"] = creado
    ctx.obj["creado_desde"] = creado_desde
    ctx.obj["creado_hasta"] = creado_hasta
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
    total = 0
    try:
        sentencias, columns, total = get_sentencias(
            autentificar(),
            creado=ctx.obj["creado"],
            creado_desde=ctx.obj["creado_desde"],
            creado_hasta=ctx.obj["creado_hasta"],
            fecha=ctx.obj["fecha"],
        )
    except requests.HTTPError as error:
        click.echo("Error de comunicacion " + str(error))
        return
    if total == 0:
        click.echo("No hay sentencias")
        return
    sentencias.to_excel(output)
    click.echo(f"Listo el archivo {output}")


@click.command()
@click.pass_context
def ver(ctx):
    """Ver sentencias en la terminal"""
    total = 0
    try:
        sentencias, columns, total = get_sentencias(
            autentificar(),
            creado=ctx.obj["creado"],
            creado_desde=ctx.obj["creado_desde"],
            creado_hasta=ctx.obj["creado_hasta"],
            fecha=ctx.obj["fecha"],
        )
    except requests.HTTPError as error:
        click.echo("Error de comunicacion " + str(error))
        return
    if total == 0:
        click.echo("No hay sentencias")
        return
    click.echo(tabulate(sentencias, headers=columns))


cli.add_command(enviar)
cli.add_command(guardar)
cli.add_command(ver)
