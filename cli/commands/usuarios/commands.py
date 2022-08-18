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
    limit: int = LIMIT,
    autoridad_id: int = None,
    autoridad_clave: str = None,
    oficina_id: int = None,
    oficina_clave: str = None,
):
    """Consultar usuarios"""
    rich.print("Consultar usuarios...")
    try:
        respuesta = get_usuarios(
            authorization_header=authorization_header(),
            limit=limit,
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            oficina_id=oficina_id,
            oficina_clave=oficina_clave,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "e-mail", "Nombres", "A. Paterno", "A. Materno", "Distrito", "Autoridad", "Oficina")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["email"],
            registro["nombres"],
            registro["apellido_paterno"],
            registro["apellido_materno"],
            registro["distrito_nombre_corto"],
            registro["autoridad_clave"],
            registro["oficina_clave"],
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] usuarios")
