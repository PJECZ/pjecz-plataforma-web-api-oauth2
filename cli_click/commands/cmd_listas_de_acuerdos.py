"""
Listas de Acuerdos
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


def get_listas_de_acuerdos(authorization_header, creado=None, creado_desde=None, creado_hasta=None, fecha=None):
    """Consultar listas de acuerdos"""
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
        columns = ["id", "autoridad_clave", "fecha", "descripcion", "archivo"]
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
    """Listas de Acuerdos"""
    ctx.obj = {}
    ctx.obj["creado"] = creado
    ctx.obj["creado_desde"] = creado_desde
    ctx.obj["creado_hasta"] = creado_hasta
    ctx.obj["fecha"] = fecha


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
        listas_de_acuerdos, columns, total = get_listas_de_acuerdos(
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
        click.echo("No hay listas de acuerdos")
        return

    # Crear archivo XLSX
    hoy_str = datetime.now().strftime("%Y-%m-%d")
    random_hex = "%030x" % random.randrange(16**30)
    archivo_nombre = f"inv-equipos-{hoy_str}-{random_hex}.xlsx"
    archivo_ruta = Path(f"/tmp/{archivo_nombre}")
    listas_de_acuerdos.to_excel(archivo_ruta)

    # Asunto
    subject = "Listas de Acuerdos"
    if ctx.obj["creado"] is not None and ctx.obj["creado"] != "":
        subject += f" creadas en {ctx.obj['creado']}"
    if ctx.obj["creado_desde"] is not None and ctx.obj["creado_desde"] != "":
        subject += f" creadas desde {ctx.obj['creado']}"
    if ctx.obj["creado_hasta"] is not None and ctx.obj["creado_hasta"] != "":
        subject += f" creadas hasta {ctx.obj['creado']}"

    # Contenidos
    elaboracion_fecha_hora_str = datetime.now().strftime("%d/%B/%Y %I:%M%p")
    contenidos = []
    contenidos.append("<h1>PJECZ Plataforma Web</h1>")
    contenidos.append(f"<h2>{subject}</h2>")
    contenidos.append(f"<p>Fecha de elaboración: <b>{elaboracion_fecha_hora_str}.</b></p>")
    contenidos.append(listas_de_acuerdos.to_html())
    contenidos.append("<p>ESTE MENSAJE ES ELABORADO POR UN PROGRAMA. FAVOR DE NO RESPONDER.</p>")

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
@click.option("--output", default="inv_equipos.csv", type=str, help="Archivo CSV a escribir")
@click.pass_context
def guardar(ctx, output):
    """Guardar"""
    total = 0
    try:
        listas_de_acuerdos, columns, total = get_listas_de_acuerdos(
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
        click.echo("No hay listas de acuerdos")
        return
    listas_de_acuerdos.to_excel(output)
    click.echo(f"Listo el archivo {output}")


@click.command()
@click.pass_context
def ver(ctx):
    """Ver listas de acuerdos en la terminal"""
    total = 0
    try:
        listas_de_acuerdos, columns, total = get_listas_de_acuerdos(
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
        click.echo("No hay listas de acuerdos")
        return
    click.echo(tabulate(listas_de_acuerdos, headers=columns))


cli.add_command(enviar)
cli.add_command(guardar)
cli.add_command(ver)
