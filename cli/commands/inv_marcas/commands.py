"""
Inv Marcas Typer Commands
"""
import typer
import rich

from config.settings import LIMIT
from lib.authentication import authorization_header
import lib.exceptions

from .crud import get_inv_marcas

app = typer.Typer()


@app.command()
def consultar(
    limit: int = LIMIT,
):
    """Consultar marcas"""
    rich.print("Consultar marcas...")
    try:
        respuesta = get_inv_marcas(
            authorization_header=authorization_header(),
            limit=limit,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Nombre")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["nombre"],
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] marcas")
