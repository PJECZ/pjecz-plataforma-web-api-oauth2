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
    distrito_id: int = None,
    es_jurisdiccional: bool = None,
    es_notaria: bool = None,
    limit: int = LIMIT,
    materia_id: int = None,
    offset: int = 0,
):
    """Consultar autoridades"""
    rich.print("Consultar autoridades...")
    try:
        datos = get_autoridades(
            authorization_header=authorization_header(),
            limit=limit,
            distrito_id=distrito_id,
            es_jurisdiccional=es_jurisdiccional,
            es_notaria=es_notaria,
            materia_id=materia_id,
            offset=offset,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Clave", "Distrito", "Descripcion", "Materia", "Organo Jurisdiccional", "Es J.", "Es N.")
    for dato in datos["items"]:
        table.add_row(
            str(dato["id"]),
            dato["clave"],
            dato["distrito_nombre_corto"],
            dato["descripcion_corta"],
            dato["materia_nombre"],
            dato["organo_jurisdiccional"],
            "Jurisdiccional" if dato["es_jurisdiccional"] else "",
            "Notaría" if dato["es_notaria"] else "",
        )
    console.print(table)
    rich.print(f"Total: [green]{datos['total']}[/green] autoridades")
