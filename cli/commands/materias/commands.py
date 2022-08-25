"""
Materias Typer Commands
"""
import typer
import rich

from config.settings import LIMIT
from lib.authentication import authorization_header
import lib.exceptions

from .crud import get_materias

app = typer.Typer()


@app.command()
def consultar(
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar materias"""
    rich.print("Consultar materias...")
    try:
        datos = get_materias(
            authorization_header=authorization_header(),
            limit=limit,
            offset=offset,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Nombre")
    for dato in datos["items"]:
        table.add_row(
            str(dato["id"]),
            dato["nombre"],
        )
    console.print(table)
    rich.print(f"Total: [green]{datos['total']}[/green] materias")
