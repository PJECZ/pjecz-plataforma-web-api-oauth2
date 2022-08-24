"""
Inv Equipos Typer Commands
"""
from datetime import datetime

import pandas as pd
import typer
import rich
import sendgrid
from sendgrid.helpers.mail import Email, To, Content, Mail
from tabulate import tabulate

from config.settings import LIMIT, LOCAL_HUSO_HORARIO, SENDGRID_API_KEY, SENDGRID_FROM_EMAIL
from lib.authentication import authorization_header
import lib.exceptions
from lib.formats import df_to_table

from .crud import get_inv_equipos, get_inv_equipos_cantidades_por_oficina_por_tipo, get_inv_equipos_cantidades_por_oficina_por_anio_fabricacion

app = typer.Typer()


@app.command()
def consultar(
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
    fecha_fabricacion_desde: str = None,
    fecha_fabricacion_hasta: str = None,
    inv_custodia_id: int = None,
    inv_modelo_id: int = None,
    inv_red_id: int = None,
    limit: int = LIMIT,
    offset: int = 0,
    oficina_id: int = None,
    oficina_clave: str = None,
    tipo: str = None,
):
    """Consultar equipos"""
    rich.print("Consultar equipos...")
    try:
        datos = get_inv_equipos(
            authorization_header=authorization_header(),
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            fecha_fabricacion_desde=fecha_fabricacion_desde,
            fecha_fabricacion_hasta=fecha_fabricacion_hasta,
            inv_custodia_id=inv_custodia_id,
            inv_modelo_id=inv_modelo_id,
            inv_red_id=inv_red_id,
            limit=limit,
            offset=offset,
            oficina_id=oficina_id,
            oficina_clave=oficina_clave,
            tipo=tipo,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Creado", "Descripcion", "Tipo", "Custodia", "Marca", "Modelo", "Red", "F. Fab.")
    for dato in datos["items"]:
        creado = datetime.fromisoformat(dato["creado"])
        table.add_row(
            str(dato["id"]),
            creado.astimezone(LOCAL_HUSO_HORARIO).strftime("%Y-%m-%d %H:%M:%S"),
            dato["descripcion"],
            dato["tipo"],
            str(dato["inv_custodia_id"]),
            dato["inv_marca_nombre"],
            dato["inv_modelo_descripcion"],
            dato["inv_red_nombre"],
            dato["fecha_fabricacion"],
        )
    console.print(table)
    rich.print(f"Total: [green]{datos['total']}[/green] equipos")


@app.command()
def consultar_cantidades_por_tipo(
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
):
    """Consultar cantidades de equipos por oficina y por tipo"""
    rich.print("Consultar cantidades de equipos por oficina y por tipo...")

    # Solicitar datos a la API
    try:
        datos = get_inv_equipos_cantidades_por_oficina_por_tipo(
            authorization_header=authorization_header(),
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Crear dataframe
    dataframe = pd.DataFrame(datos)
    dataframe.oficina_clave = dataframe.oficina_clave.astype("category")
    dataframe.inv_equipo_tipo = dataframe.inv_equipo_tipo.astype("category")

    # Crear pivot table
    pivot_table = dataframe.pivot_table(
        index="oficina_clave",
        columns="inv_equipo_tipo",
        values="cantidad",
        aggfunc="sum",
    )

    # Mostrar la tabla
    tabla = rich.table.Table(show_lines=False)
    tabla = df_to_table(pivot_table, tabla, "Oficinas")
    console = rich.console.Console()
    console.print(tabla)

    # Mostrar el total
    rich.print("Total: [green]XXX[/green] equipos")


@app.command()
def enviar_cantidades_por_tipo(
    email: str,
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
    test: bool = True,
):
    """Enviar mensaje con cantidades de equipos por oficina y por tipo"""
    rich.print("Enviar mensaje con cantidades de equipos por oficina y por tipo...")

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
        datos = get_inv_equipos_cantidades_por_oficina_por_tipo(
            authorization_header=authorization_header(),
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Crear dataframe
    dataframe = pd.DataFrame(datos)
    dataframe.oficina_clave = dataframe.oficina_clave.astype("category")
    dataframe.inv_equipo_tipo = dataframe.inv_equipo_tipo.astype("category")

    # Crear pivot table
    pivot_table = dataframe.pivot_table(
        index="oficina_clave",
        columns="inv_equipo_tipo",
        values="cantidad",
        aggfunc="sum",
    )

    # Definir el asunto
    asunto = "Cantidades de equipos por oficina y por tipo creados"
    if creado is not None:
        asunto += f" el {creado}"
    if creado_desde is not None:
        asunto += f" desde el {creado_desde}"
    if creado_hasta is not None:
        asunto += f" hasta el {creado_hasta}"

    # Definir encabezados de la tabla
    encabezados = ["Oficinas"]
    encabezados.extend(pivot_table.columns.tolist())

    # Mostrar tabla 'simple' si test es verdadero y terminar
    if test is True:
        tabla = tabulate(pivot_table, headers=encabezados, tablefmt="simple")
        print(asunto)
        print(tabla)
        rich.print("[yellow]No se envio el mensaje porque esta en modo de prueba.[/yellow]")
        return

    # Crear tabla HTML
    tabla_html = tabulate(pivot_table, headers=encabezados, tablefmt="html")
    tabla_html = tabla_html.replace("<table>", '<table border="1" style="width:100%; border: 1px solid black; border-collapse: collapse;">')
    tabla_html = tabla_html.replace('<td style="', '<td style="padding: 4px;')
    tabla_html = tabla_html.replace("<td>", '<td style="padding: 4px;">')
    tabla_html = tabla_html.replace("0</td>", "&nbsp;</td>")

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


@app.command()
def consultar_cantidades_por_anio_fabricacion(
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
    distrito_id: int = None,
    tipo: str = None,
):
    """Consultar cantidades de equipos por oficina y por año de fabricacion"""
    rich.print("Consultar cantidades de equipos por oficina y por año de fabricacion...")

    # Solicitar datos a la API
    try:
        datos = get_inv_equipos_cantidades_por_oficina_por_anio_fabricacion(
            authorization_header=authorization_header(),
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            distrito_id=distrito_id,
            tipo=tipo,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Crear dataframe
    dataframe = pd.DataFrame(datos)
    dataframe.oficina_clave = dataframe.oficina_clave.astype("category")
    dataframe.anio_fabricacion = dataframe.anio_fabricacion.astype("int")

    # Crear pivot table
    pivot_table = dataframe.pivot_table(
        index="oficina_clave",
        columns="anio_fabricacion",
        values="cantidad",
        aggfunc="sum",
    )

    # Mostrar la tabla
    tabla = rich.table.Table(show_lines=False)
    tabla = df_to_table(pivot_table, tabla, "Oficinas")
    console = rich.console.Console()
    console.print(tabla)

    # Mostrar el total
    rich.print("Total: [green]XXX[/green] equipos")


@app.command()
def enviar_cantidades_por_anio_fabricacion(
    email: str,
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
    distrito_id: int = None,
    test: bool = True,
    tipo: str = None,
):
    """Enviar mensaje con cantidades de equipos por oficina y por año de fabricacion"""
    rich.print("Enviar mensaje con cantidades de equipos por oficina y por año de fabricacion...")

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
        datos = get_inv_equipos_cantidades_por_oficina_por_anio_fabricacion(
            authorization_header=authorization_header(),
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            distrito_id=distrito_id,
            tipo=tipo,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Crear dataframe
    dataframe = pd.DataFrame(datos)
    dataframe.oficina_clave = dataframe.oficina_clave.astype("category")
    dataframe.anio_fabricacion = dataframe.anio_fabricacion.astype("int")

    # Crear pivot table
    pivot_table = dataframe.pivot_table(
        index="oficina_clave",
        columns="anio_fabricacion",
        values="cantidad",
        aggfunc="sum",
    )

    # Definir el asunto
    asunto = "Cantidades de equipos por oficina y por año de fabricacion"
    if creado is not None:
        asunto += f" el {creado}"
    if creado_desde is not None:
        asunto += f" desde el {creado_desde}"
    if creado_hasta is not None:
        asunto += f" hasta el {creado_hasta}"

    # Definir encabezados de la tabla
    encabezados = ["Oficinas"]
    encabezados.extend(pivot_table.columns.tolist())

    # Mostrar tabla 'simple' si test es verdadero y terminar
    if test is True:
        tabla = tabulate(pivot_table, headers=encabezados, tablefmt="simple")
        print(asunto)
        print(tabla)
        rich.print("[yellow]No se envio el mensaje porque esta en modo de prueba.[/yellow]")
        return

    # Crear tabla HTML
    tabla_html = tabulate(pivot_table, headers=encabezados, tablefmt="html")
    tabla_html = tabla_html.replace("<table>", '<table border="1" style="width:100%; border: 1px solid black; border-collapse: collapse;">')
    tabla_html = tabla_html.replace('<td style="', '<td style="padding: 4px;')
    tabla_html = tabla_html.replace("<td>", '<td style="padding: 4px;">')
    tabla_html = tabla_html.replace("0</td>", "&nbsp;</td>")

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
