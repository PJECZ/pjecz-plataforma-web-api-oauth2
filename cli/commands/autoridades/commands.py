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
    es_jurisdiccional: bool = None,
    es_notaria: bool = None,
    materia_id: int = None,
):
    """Consultar autoridades"""
    rich.print("Consultar autoridades...")
    try:
        respuesta = get_autoridades(
            authorization_header=authorization_header(),
            limit=limit,
            distrito_id=distrito_id,
            es_jurisdiccional=es_jurisdiccional,
            es_notaria=es_notaria,
            materia_id=materia_id,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Clave", "Distrito", "Descripcion", "Materia", "Organo Jurisdiccional", "Es J.", "Es N.")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["clave"],
            registro["distrito_nombre_corto"],
            registro["descripcion_corta"],
            registro["materia_nombre"],
            registro["organo_jurisdiccional"],
            "Jurisdiccional" if registro["es_jurisdiccional"] else "",
            "Notaría" if registro["es_notaria"] else "",
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] autoridades")
