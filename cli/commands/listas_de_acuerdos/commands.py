"""
Listas de Acuerdos Typer Commands
"""
from datetime import datetime

import typer
import rich

from config.settings import LIMIT, LOCAL_HUSO_HORARIO
from lib.authentication import authorization_header
import lib.exceptions

from .crud import get_listas_de_acuerdos, get_listas_de_acuerdos_por_distrito_por_creado

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
):
    """Consultar listas de acuerdos"""
    rich.print("Consultar listas de acuerdos...")
    try:
        respuesta = get_listas_de_acuerdos(
            authorization_header=authorization_header(),
            limit=limit,
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            fecha=fecha,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Distrito", "Autoridad", "Fecha", "Creado")
    for registro in respuesta["items"]:
        creado = datetime.fromisoformat(registro["creado"])
        fecha = datetime.strptime(registro["fecha"], "%Y-%m-%d")
        table.add_row(
            str(registro["id"]),
            registro["distrito_nombre_corto"],
            registro["autoridad_clave"],
            fecha.strftime("%Y-%m-%d"),
            creado.astimezone(LOCAL_HUSO_HORARIO).strftime("%Y-%m-%d %H:%M:%S"),
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] listas de acuerdos")


@app.command()
def consultar_por_distrito_por_creado(
    creado: str,
    distrito_id: int,
    limit: int = LIMIT,
):
    """Consultar listas de acuerdos por distrito y creado"""
    rich.print("Consultar listas de acuerdos por distrito y creado...")
    try:
        respuesta = get_listas_de_acuerdos_por_distrito_por_creado(
            authorization_header=authorization_header(),
            creado=creado,
            distrito_id=distrito_id,
            limit=limit,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Autoridad", "Fecha", "Creado", "Archivo")
    for registro in respuesta:
        creado = datetime.fromisoformat(registro["creado"])
        fecha = datetime.strptime(registro["fecha"], "%Y-%m-%d")
        table.add_row(
            str(registro["id"]),
            registro["autoridad_clave"],
            fecha.strftime("%Y-%m-%d"),
            creado.astimezone(LOCAL_HUSO_HORARIO).strftime("%Y-%m-%d %H:%M:%S"),
            registro["archivo"],
        )
    console.print(table)
    rich.print("Total: [green]PENDIENTE[/green] listas de acuerdos")
