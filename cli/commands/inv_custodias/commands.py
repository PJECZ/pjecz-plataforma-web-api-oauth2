"""
Inv Custodias Typer Commands
"""
from datetime import datetime

import typer
import rich

from config.settings import LIMIT, LOCAL_HUSO_HORARIO, SERVIDOR_HUSO_HORARIO
from lib.authentication import authorization_header
import lib.exceptions

from .crud import get_inv_custodias

app = typer.Typer()


@app.command()
def consultar(
    fecha_desde: str = None,
    fecha_hasta: str = None,
    limit: int = LIMIT,
    offset: int = 0,
    usuario_id: int = None,
    usuario_email: str = None,
):
    """Consultar custodias"""
    rich.print("Consultar custodias...")
    try:
        datos = get_inv_custodias(
            authorization_header=authorization_header(),
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            limit=limit,
            offset=offset,
            usuario_id=usuario_id,
            usuario_email=usuario_email,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Creado", "Usuario", "e-mail", "Fecha")
    for dato in datos["items"]:
        creado = datetime.fromisoformat(dato["creado"]).replace(tzinfo=SERVIDOR_HUSO_HORARIO)
        table.add_row(
            str(dato["id"]),
            creado.astimezone(LOCAL_HUSO_HORARIO).strftime("%Y-%m-%d %H:%M"),
            dato["usuario_nombre"],
            dato["usuario_email"],
            dato["fecha"],
        )
    console.print(table)
    rich.print(f"Total: [green]{datos['total']}[/green] custodias")
