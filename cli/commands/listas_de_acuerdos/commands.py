"""
Listas de Acuerdos Typer Commands
"""
from datetime import datetime

import typer
import rich
import sendgrid
from sendgrid.helpers.mail import Email, To, Content, Mail
from tabulate import tabulate

from config.settings import LIMIT, LOCAL_HUSO_HORARIO, SERVIDOR_HUSO_HORARIO, SENDGRID_API_KEY, SENDGRID_FROM_EMAIL
from lib.authentication import authorization_header
import lib.exceptions

from .crud import get_listas_de_acuerdos, get_listas_de_acuerdos_sintetizar_por_creado

app = typer.Typer()


@app.command()
def consultar(
    autoridad_id: int = None,
    autoridad_clave: str = None,
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
    fecha: str = None,
    fecha_desde: str = None,
    fecha_hasta: str = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar listas de acuerdos"""
    rich.print("Consultar listas de acuerdos...")
    try:
        datos = get_listas_de_acuerdos(
            authorization_header=authorization_header(),
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            fecha=fecha,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            limit=limit,
            offset=offset,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Creado", "Autoridad", "Fecha", "Archivo")
    for dato in datos["items"]:
        creado = datetime.fromisoformat(dato["creado"]).replace(tzinfo=SERVIDOR_HUSO_HORARIO)
        table.add_row(
            str(dato["id"]),
            creado.astimezone(LOCAL_HUSO_HORARIO).strftime("%Y-%m-%d %H:%M"),
            dato["autoridad_clave"],
            dato["fecha"],
            dato["archivo"],
        )
    console.print(table)
    rich.print(f"Total: [green]{datos['total']}[/green] listas de acuerdos")


@app.command()
def consultar_creadas(
    creado: str = None,
    distrito_id: int = None,
):
    """Consultar listas de acuerdos creadas en un día"""
    rich.print("Consultar listas de acuerdos creadas en un día...")

    # Solicitar datos a la API
    try:
        datos = get_listas_de_acuerdos_sintetizar_por_creado(
            authorization_header=authorization_header(),
            creado=creado,
            distrito_id=distrito_id,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Mostrar tabla
    console = rich.console.Console()
    table = rich.table.Table("A. Clave", "Distrito", "Autoridad", "ID", "Fecha", "Creado", "Archivo")
    contador = 0
    for dato in datos:
        if dato["id"] == 0:
            table.add_row(
                dato["autoridad_clave"],
                dato["distrito_nombre_corto"],
                dato["autoridad_descripcion_corta"],
                "ND",
                "ND",
                "ND",
                "ND",
            )
            continue
        creado = datetime.fromisoformat(dato["creado"]).replace(tzinfo=SERVIDOR_HUSO_HORARIO)
        table.add_row(
            dato["autoridad_clave"],
            dato["distrito_nombre_corto"],
            dato["autoridad_descripcion_corta"],
            str(dato["id"]),
            dato["fecha"],
            creado.astimezone(LOCAL_HUSO_HORARIO).strftime("%Y-%m-%d %H:%M"),
            dato["archivo"],
        )
        contador += 1
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{contador}[/green] listas de acuerdos")


@app.command()
def enviar_creadas(
    email: str,
    creado: str = None,
    test: bool = True,
):
    """Enviar mensaje con listas de acuerdos creadas en un día"""
    rich.print("Enviar mensaje con listas de acuerdos creadas en un día...")

    # Si test es falso, entonces se va a usar SendGrid
    sendgrid_client = None
    from_email = None
    if test is False:
        # Validar variables de entorno
        try:
            if SENDGRID_API_KEY == "":
                raise lib.exceptions.CLIConfigurationError("Falta SENDGRID_API_KEY")
            if SENDGRID_FROM_EMAIL == "":
                raise lib.exceptions.CLIConfigurationError("Falta SENDGRID_FROM_EMAIL")
        except lib.exceptions.CLIAnyError as error:
            typer.secho(str(error), fg=typer.colors.RED)
            raise typer.Exit()
        # Inicializar SendGrid
        sendgrid_client = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        from_email = Email(SENDGRID_FROM_EMAIL)

    # Solicitar datos a la API
    try:
        datos = get_listas_de_acuerdos_sintetizar_por_creado(
            authorization_header=authorization_header(),
            creado=creado,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Definir el asunto
    asunto = f"Listas de acuerdos creadas el {creado}"

    # Definir encabezados y renglones de la tabla
    encabezados = ["A. Clave", "Distrito", "Autoridad", "ID", "Fecha", "Creado", "Archivo"]
    renglones = []
    for dato in datos:
        if dato["id"] == 0:
            renglones.append(
                [
                    dato["autoridad_clave"],
                    dato["distrito_nombre_corto"],
                    dato["autoridad_descripcion_corta"],
                    "ND",
                    "ND",
                    "ND",
                    "ND",
                ]
            )
            continue
        creado_dt = datetime.fromisoformat(dato["creado"])
        renglones.append(
            [
                dato["autoridad_clave"],
                dato["distrito_nombre_corto"],
                dato["autoridad_descripcion_corta"],
                dato["id"],
                dato["fecha"],
                creado_dt.astimezone(LOCAL_HUSO_HORARIO).strftime("%Y-%m-%d %H:%M"),
                dato["archivo"] if test else f"<a href=\"{dato['url']}\">{dato['archivo']}</a>",
            ]
        )

    # Mostrar tabla 'simple' si test es verdadero y terminar
    if test is True:
        tabla = tabulate(renglones, headers=encabezados, tablefmt="simple")
        print(asunto)
        print(tabla)
        rich.print("[yellow]No se envio el mensaje porque esta en modo de prueba.[/yellow]")
        return

    # Crear tabla HTML
    tabla_html = tabulate(renglones, headers=encabezados, tablefmt="unsafehtml")
    tabla_html = tabla_html.replace("<table>", '<table border="1" style="width:100%; border: 1px solid black; border-collapse: collapse;">')
    tabla_html = tabla_html.replace('<td style="', '<td style="padding: 4px;')
    tabla_html = tabla_html.replace("<td>", '<td style="padding: 4px;">')

    # Crear el cuerpo del mensaje
    elaboracion_fecha_hora_str = datetime.now().strftime("%d/%B/%Y %I:%M%p")
    contenidos = []
    contenidos.append("<style> td {border:2px black solid !important} </style>")
    contenidos.append("<h1>PJECZ Plataforma Web</h1>")
    contenidos.append(f"<h2>{asunto}</h2>")
    contenidos.append(tabla_html)
    contenidos.append(f"<p>Fecha de elaboración: <b>{elaboracion_fecha_hora_str}.</b></p>")
    contenidos.append("<p>ESTE MENSAJE ES ELABORADO POR UN PROGRAMA. FAVOR DE NO RESPONDER.</p>")

    # Enviar el mensaje
    to_email = To(email)
    content = Content("text/html", "<br>".join(contenidos))
    mail = Mail(from_email=from_email, to_emails=to_email, subject=asunto, html_content=content)
    try:
        sendgrid_client.client.mail.send.post(request_body=mail.get())
    except Exception as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Mostrar mensaje final
    rich.print(f"Se ha enviado [green]{asunto}[/green] a [blue]{email}[/blue].")
