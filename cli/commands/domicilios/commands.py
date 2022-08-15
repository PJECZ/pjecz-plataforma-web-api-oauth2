"""
Domicilios Typer Commands
"""
import typer
import rich

from config.settings import LIMIT
from lib.authentication import authorization_header
import lib.exceptions

from .crud import get_domicilios

app = typer.Typer()


@app.command()
def consultar(
    limit: int = LIMIT,
):
    """Consultar domicilios"""
    rich.print("Consultar domicilios...")
    try:
        respuesta = get_domicilios(
            authorization_header=authorization_header(),
            limit=limit,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Estado", "Municipio", "Calle", "No. Ext.", "No. Int.", "Colonia", "C.P.")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["estado"],
            registro["municipio"],
            registro["calle"],
            registro["num_ext"],
            registro["num_int"],
            registro["colonia"],
            str(registro["cp"]),
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] domicilios")
