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
    distrito_id: int = None,
    domicilio_id: int = None,
    es_juridicional: bool = False,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar oficinas"""
    rich.print("Consultar oficinas...")
    try:
        datos = get_oficinas(
            authorization_header=authorization_header(),
            distrito_id=distrito_id,
            domicilio_id=domicilio_id,
            es_juridicional=es_juridicional,
            limit=limit,
            offset=offset,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Clave", "Descripcion", "Domicilio", "Col", "Col")
    for dato in datos["items"]:
        apertura = datetime.strptime(dato["apertura"], "%H:%M:%S")
        cierre = datetime.strptime(dato["cierre"], "%H:%M:%S")
        table.add_row(
            str(dato["id"]),
            dato["clave"],
            dato["descripcion_corta"],
            dato["domicilio_completo"],
            apertura.strftime("%H:%M"),
            cierre.strftime("%H:%M"),
            str(dato["limite_personas"]),
            "SI" if bool(dato["es_jurisdiccional"]) else "",
        )
    console.print(table)
    rich.print(f"Total: [green]{datos['total']}[/green] oficinas")
