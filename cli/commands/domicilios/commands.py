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
    offset: int = 0,
):
    """Consultar domicilios"""
    rich.print("Consultar domicilios...")
    try:
        datos = get_domicilios(
            authorization_header=authorization_header(),
            limit=limit,
            offset=offset,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Estado", "Municipio", "Calle", "No. Ext.", "No. Int.", "Colonia", "C.P.")
    for dato in datos["items"]:
        table.add_row(
            str(dato["id"]),
            dato["estado"],
            dato["municipio"],
            dato["calle"],
            dato["num_ext"],
            dato["num_int"],
            dato["colonia"],
            str(dato["cp"]),
        )
    console.print(table)
    rich.print(f"Total: [green]{datos['total']}[/green] domicilios")
