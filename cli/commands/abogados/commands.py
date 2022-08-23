"""
Abogados Typer Commands
"""
import typer
import rich

from config.settings import LIMIT
from lib.authentication import authorization_header
import lib.exceptions

from .crud import get_abogados

app = typer.Typer()


@app.command()
def consultar(
    anio_desde: int = None,
    anio_hasta: int = None,
    limit: int = LIMIT,
    nombre: str = None,
    offset: int = 0,
):
    """Consultar abogados"""
    rich.print("Consultar abogados...")
    try:
        respuesta = get_abogados(
            authorization_header=authorization_header(),
            anio_desde=anio_desde,
            anio_hasta=anio_hasta,
            limit=limit,
            nombre=nombre,
            offset=offset,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Fecha", "Libro", "Numero", "Nombre")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            str(registro["fecha"]),
            registro["libro"],
            registro["numero"],
            registro["nombre"],
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] abogados")
