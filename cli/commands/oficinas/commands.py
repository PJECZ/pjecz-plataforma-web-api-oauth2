"""
Oficinas Typer Commands
"""
from datetime import datetime

import typer
import rich

from config.settings import LIMIT
from lib.authentication import authorization_header
import lib.exceptions

from .crud import get_oficinas

app = typer.Typer()


@app.command()
def consultar(
    limit: int = LIMIT,
    distrito_id: int = None,
    domicilio_id: int = None,
    es_juridicional: bool = False,
):
    """Consultar oficinas"""
    rich.print("Consultar oficinas...")
    try:
        respuesta = get_oficinas(
            authorization_header=authorization_header(),
            limit=limit,
            distrito_id=distrito_id,
            domicilio_id=domicilio_id,
            es_juridicional=es_juridicional,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Clave", "Descripcion", "Domicilio", "Col", "Col")
    for registro in respuesta["items"]:
        apertura = datetime.strptime(registro["apertura"], "%H:%M:%S")
        cierre = datetime.strptime(registro["cierre"], "%H:%M:%S")
        table.add_row(
            str(registro["id"]),
            registro["clave"],
            registro["descripcion_corta"],
            registro["domicilio_completo"][:24] + "..." if len(registro["domicilio_completo"]) > 24 else registro["domicilio_completo"],
            apertura.strftime("%H:%M"),
            cierre.strftime("%H:%M"),
            str(registro["limite_personas"]),
            "SI" if bool(registro["es_jurisdiccional"]) else "",
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] oficinas")
