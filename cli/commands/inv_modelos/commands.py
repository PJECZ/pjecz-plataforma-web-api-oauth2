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
):
    """Consultar modelos"""
    rich.print("Consultar modelos...")
    try:
        respuesta = get_inv_modelos(
            authorization_header=authorization_header(),
            limit=limit,
            inv_marca_id=inv_marca_id,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Marca", "Descripcion")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["inv_marca_nombre"],
            registro["descripcion"],
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] modelos")
