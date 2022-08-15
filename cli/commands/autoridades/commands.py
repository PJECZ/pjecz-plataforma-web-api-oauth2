"""
Autoridades Typer Commands
"""
import typer
import rich

from config.settings import LIMIT
from lib.authentication import authorization_header
import lib.exceptions

from .crud import get_autoridades

app = typer.Typer()


@app.command()
def consultar(
    limit: int = LIMIT,
    distrito_id: int = None,
    materia_id: int = None,
):
    """Consultar autoridades"""
    rich.print("Consultar autoridades...")
    try:
        respuesta = get_autoridades(
            authorization_header=authorization_header(),
            limit=limit,
            distrito_id=distrito_id,
            materia_id=materia_id,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Clave", "Distrito", "Descripcion", "Materia", "Organo Jurisdiccional")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["clave"],
            registro["distrito_nombre_corto"],
            registro["descripcion_corta"],
            registro["materia_nombre"],
            registro["organo_jurisdiccional"],
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] autoridades")
