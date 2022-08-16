"""
Inv Custodias Typer Commands
"""
from datetime import datetime

import typer
import rich

from config.settings import LIMIT, LOCAL_HUSO_HORARIO
from lib.authentication import authorization_header
import lib.exceptions

from .crud import get_inv_custodias

app = typer.Typer()


@app.command()
def consultar(
    limit: int = LIMIT,
    usuario_id: int = None,
    usuario_email: str = None,
    fecha_desde: str = None,
    fecha_hasta: str = None,
):
    """Consultar custodias"""
    rich.print("Consultar custodias...")
    try:
        respuesta = get_inv_custodias(
            authorization_header=authorization_header(),
            limit=limit,
            usuario_id=usuario_id,
            usuario_email=usuario_email,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Creado", "e-mail", "Usuario", "Fecha")
    for registro in respuesta["items"]:
        creado = datetime.fromisoformat(registro["creado"])
        table.add_row(
            str(registro["id"]),
            creado.astimezone(LOCAL_HUSO_HORARIO).strftime("%Y-%m-%d %H:%M:%S"),
            registro["usuario_email"],
            registro["usuario_nombre"],
            registro["fecha"],
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] custodias")
