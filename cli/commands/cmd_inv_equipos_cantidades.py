"""
Inventarios Equipos
"""
import base64
from datetime import datetime
import locale
import os
from pathlib import Path
import random

import click
from dotenv import load_dotenv
import openpyxl
import pandas as pd
import requests
import sendgrid
from sendgrid.helpers.mail import Attachment, ContentId, Disposition, Email, FileContent, FileName, FileType, To, Content, Mail
from tabulate import tabulate

from cli.commands.autentificar import autentificar, BASE_URL

# Regionalizacion del tiempo
locale.setlocale(locale.LC_TIME, "es_MX.utf8")

# Variables de entorno
load_dotenv()
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL")
SENDGRID_TO_EMAIL = os.getenv("SENDGRID_TO_EMAIL")


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

    # Validar configuracion
    if SENDGRID_API_KEY is None or SENDGRID_API_KEY == "":
        raise Exception("Error de configuracion: Falta SENDGRID_API_KEY")
    if SENDGRID_FROM_EMAIL is None or SENDGRID_FROM_EMAIL == "":
        raise Exception("Error de configuracion: Falta SENDGRID_FROM_EMAIL")
    if SENDGRID_TO_EMAIL is None or SENDGRID_TO_EMAIL == "":
        raise Exception("Error de configuracion: Falta SENDGRID_TO_EMAIL")

    # Consultar
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
        return
    if total == 0:
        click.echo("No hay equipos")
        return

    # Archivo XLSX
    hoy_str = datetime.now().strftime("%Y-%m-%d")
    random_hex = "%030x" % random.randrange(16**30)
    archivo_nombre = f"inv-equipos-cantidades-{hoy_str}-{random_hex}.xlsx"
    archivo_ruta = Path(f"/tmp/{archivo_nombre}")
    cantidades_oficina_tipo.to_excel(archivo_ruta)

    # Asunto
    momento_str = datetime.now().strftime("%d/%B/%Y %I:%M%p")
    subject = "Cantidades de equipos en inventarios por oficina y tipo"

    # Contenidos
    contenidos = [
        "<h1>PJECZ Plataforma Web</h1>",
        f"<h2>{subject}</h2>",
        f"<p>Fecha de elaboración: {momento_str}.<br>",
        "ESTE MENSAJE ES ELABORADO POR UN PROGRAMA. FAVOR DE NO RESPONDER.</p>",
    ]

    # Enviar el mensaje con el archivo adjunto via SendGrid
    sendgrid_client = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    from_email = Email(SENDGRID_FROM_EMAIL)
    to_email = To(SENDGRID_TO_EMAIL)
    content = Content("text/html", "<br>".join(contenidos))
    mail = Mail(from_email, to_email, subject, content)
    attachment = Attachment()
    attachment.content_id = ContentId(archivo_nombre)
    attachment.disposition = Disposition("attachment")
    with open(archivo_ruta, "rb") as puntero:
        attachment.file_content = FileContent(base64.b64encode(puntero.read()).decode())
    attachment.file_name = FileName(archivo_nombre)
    attachment.file_type = FileType("application/vnd.ms-excel")
    mail.attachment = attachment
    sendgrid_client.client.mail.send.post(request_body=mail.get())

    # Eliminar el archivo
    archivo_ruta.unlink(missing_ok=True)


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
        return
    if total == 0:
        click.echo("No hay equipos")
        return
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
        return
    if total == 0:
        click.echo("No hay equipos")
        return
    click.echo(tabulate(cantidades_oficina_tipo, headers=columns))


cli.add_command(enviar)
cli.add_command(guardar)
cli.add_command(ver)
