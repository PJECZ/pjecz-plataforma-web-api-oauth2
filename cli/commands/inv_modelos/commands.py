"""
Inv Modelos Typer Commands
"""
import typer
import rich

from config.settings import LIMIT
from lib.authentication import authorization_header
import lib.exceptions

from .crud import get_inv_modelos

app = typer.Typer()


@app.command()
def consultar(
    limit: int = LIMIT,
    inv_marca_id: int = None,
    offset: int = 0,
):
    """Consultar modelos"""
    rich.print("Consultar modelos...")
    try:
        datos = get_inv_modelos(
            authorization_header=authorization_header(),
            limit=limit,
            inv_marca_id=inv_marca_id,
            offset=offset,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Marca", "Descripcion")
    for dato in datos["items"]:
        table.add_row(
            str(dato["id"]),
            dato["inv_marca_nombre"],
            dato["descripcion"],
        )
    console.print(table)
    rich.print(f"Total: [green]{datos['total']}[/green] modelos")
