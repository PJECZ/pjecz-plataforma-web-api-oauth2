"""
Centros de Trabajo Typer Commands
"""
import typer
import rich

from config.settings import LIMIT
from lib.authentication import authorization_header
import lib.exceptions

from .crud import get_centros_trabajos

app = typer.Typer()


@app.command()
def consultar(
    limit: int = LIMIT,
    distrito_id: int = None,
    domicilio_id: int = None,
    offset: int = 0,
):
    """Consultar centros de trabajo"""
    rich.print("Consultar centros de trabajo...")
    try:
        datos = get_centros_trabajos(
            authorization_header=authorization_header(),
            limit=limit,
            distrito_id=distrito_id,
            domicilio_id=domicilio_id,
            offset=offset,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Clave", "Nombre", "Distrito", "Domicilio", "Telefono")
    for dato in datos["items"]:
        table.add_row(
            str(dato["id"]),
            dato["clave"],
            dato["nombre"],
            dato["distrito_nombre_corto"],
            dato["domicilio_completo"],
            dato["telefono"],
        )
    console.print(table)
    rich.print(f"Total: [green]{datos['total']}[/green] centros de trabajo")
