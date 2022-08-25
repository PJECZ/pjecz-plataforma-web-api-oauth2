"""
Distritos Typer Commands
"""
import typer
import rich

from config.settings import LIMIT
from lib.authentication import authorization_header
import lib.exceptions

from .crud import get_distritos

app = typer.Typer()


@app.command()
def consultar(
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar distritos"""
    rich.print("Consultar distritos...")
    try:
        datos = get_distritos(
            authorization_header=authorization_header(),
            limit=limit,
            offset=offset,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Nombre", "Nombre Corto", "Es D.J.")
    for dato in datos["items"]:
        table.add_row(
            str(dato["id"]),
            dato["nombre"],
            dato["nombre_corto"],
            "SI" if dato["es_distrito_judicial"] else "",
        )
    console.print(table)
    rich.print(f"Total: [green]{datos['total']}[/green] distritos")
