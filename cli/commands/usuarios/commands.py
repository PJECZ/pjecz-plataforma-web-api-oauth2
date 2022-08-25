"""
Usuarios Typer Commands
"""
import typer
import rich

from config.settings import LIMIT
from lib.authentication import authorization_header
import lib.exceptions

from .crud import get_usuarios

app = typer.Typer()


@app.command()
def consultar(
    autoridad_id: int = None,
    autoridad_clave: str = None,
    limit: int = LIMIT,
    oficina_id: int = None,
    oficina_clave: str = None,
    offset: int = 0,
):
    """Consultar usuarios"""
    rich.print("Consultar usuarios...")
    try:
        datos = get_usuarios(
            authorization_header=authorization_header(),
            limit=limit,
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            offset=offset,
            oficina_id=oficina_id,
            oficina_clave=oficina_clave,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "e-mail", "Nombres", "A. Paterno", "A. Materno", "Distrito", "Autoridad", "Oficina")
    for dato in datos["items"]:
        table.add_row(
            str(dato["id"]),
            dato["email"],
            dato["nombres"],
            dato["apellido_paterno"],
            dato["apellido_materno"],
            dato["distrito_nombre_corto"],
            dato["autoridad_clave"],
            dato["oficina_clave"],
        )
    console.print(table)
    rich.print(f"Total: [green]{datos['total']}[/green] usuarios")
