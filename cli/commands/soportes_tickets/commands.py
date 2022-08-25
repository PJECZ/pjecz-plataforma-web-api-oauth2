"""
Soportes Tickets Typer Commands
"""
from datetime import datetime

import typer
import rich

from config.settings import LIMIT, LOCAL_HUSO_HORARIO, SERVIDOR_HUSO_HORARIO
from lib.authentication import authorization_header
import lib.exceptions

from .crud import (
    get_soportes_tickets,
    get_soportes_tickets_cantidades_por_distrito_por_categoria,
    get_soportes_tickets_cantidades_por_funcionario_por_estado,
)

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
        datos = get_soportes_tickets(
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
    table = rich.table.Table("ID", "Creado", "Usuario", "Oficina", "Categoria")
    for dato in datos["items"]:
        creado = datetime.fromisoformat(dato["creado"]).replace(tzinfo=SERVIDOR_HUSO_HORARIO)
        table.add_row(
            str(dato["id"]),
            creado.astimezone(LOCAL_HUSO_HORARIO).strftime("%Y-%m-%d %H:%M"),
            dato["usuario_nombre"],
            dato["usuario_oficina_clave"],
            dato["soporte_categoria_nombre"],
        )
    console.print(table)
    rich.print(f"Total: [green]{datos['total']}[/green] tickets de soporte")


@app.command()
def cantidades_por_distrito_por_categoria(
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
):
    """Consultar cantidades de tickets de soporte por distrito y categoria"""
    rich.print("Consultar cantidades de tickets de soporte por distrito y categoria...")
    try:
        datos = get_soportes_tickets_cantidades_por_distrito_por_categoria(
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
    for dato in datos["items"]:
        table.add_row(
            dato["distrito"],
            dato["categoria"],
            str(dato["cantidad"]),
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
        datos = get_soportes_tickets_cantidades_por_funcionario_por_estado(
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
    for dato in datos["items"]:
        table.add_row(
            dato["funcionario"],
            dato["estado"],
            str(dato["cantidad"]),
        )
    console.print(table)
    rich.print("Total: [green]N[/green] tickets de soporte")
