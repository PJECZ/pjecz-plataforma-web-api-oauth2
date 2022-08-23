"""
Soportes Tickets Typer Commands
"""
from datetime import datetime

import typer
import rich

from config.settings import LIMIT, LOCAL_HUSO_HORARIO
from lib.authentication import authorization_header
import lib.exceptions

from .crud import get_soportes_tickets, get_soportes_tickets_cantidades_por_distrito_por_categoria, get_soportes_tickets_cantidades_por_funcionario_por_estado

app = typer.Typer()


@app.command()
def consultar(
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
    descripcion: str = None,
    estado: str = None,
    limit: int = LIMIT,
    oficina_id: int = None,
    oficina_clave: str = None,
    offset: int = 0,
    soporte_categoria_id: int = None,
    usuario_id: int = None,
    usuario_email: str = None,
):
    """Consultar tickets de soporte"""
    rich.print("Consultar tickets de soporte...")
    try:
        respuesta = get_soportes_tickets(
            authorization_header=authorization_header(),
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            descripcion=descripcion,
            estado=estado,
            limit=limit,
            offset=offset,
            oficina_id=oficina_id,
            oficina_clave=oficina_clave,
            soporte_categoria_id=soporte_categoria_id,
            usuario_id=usuario_id,
            usuario_email=usuario_email,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Creado", "Inicio", "Col", "Col", "Col")
    for registro in respuesta["items"]:
        creado = datetime.fromisoformat(registro["creado"])
        inicio = datetime.strptime(registro["inicio"], "%Y-%m-%dT%H:%M:%S")
        table.add_row(
            str(registro["id"]),
            creado.astimezone(LOCAL_HUSO_HORARIO).strftime("%Y-%m-%d %H:%M:%S"),
            inicio.strftime("%Y-%m-%d %H:%M:%S"),
            registro["col_str"],
            str(registro["col_int"]),
            "YA" if bool(registro["col_bool"]) else "",
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] tickets de soporte")


@app.command()
def cantidades_por_distrito_por_categoria(
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
):
    """Consultar cantidades de tickets de soporte por distrito y categoria"""
    rich.print("Consultar cantidades de tickets de soporte por distrito y categoria...")
    try:
        respuesta = get_soportes_tickets_cantidades_por_distrito_por_categoria(
            authorization_header=authorization_header(),
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("Distrito", "Categoria", "Cantidad")
    for registro in respuesta["items"]:
        table.add_row(
            registro["distrito"],
            registro["categoria"],
            str(registro["cantidad"]),
        )
    console.print(table)
    rich.print("Total: [green]N[/green] tickets de soporte")


@app.command()
def cantidades_por_funcionario_por_estado(
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
):
    """Consultar cantidades de tickets de soporte por funcionario y por estado"""
    rich.print("Consultar cantidades de tickets de soporte por funcionario y por estado...")
    try:
        respuesta = get_soportes_tickets_cantidades_por_funcionario_por_estado(
            authorization_header=authorization_header(),
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("Funcionario", "Estado", "Cantidad")
    for registro in respuesta["items"]:
        table.add_row(
            registro["funcionario"],
            registro["estado"],
            str(registro["cantidad"]),
        )
    console.print(table)
    rich.print("Total: [green]N[/green] tickets de soporte")
