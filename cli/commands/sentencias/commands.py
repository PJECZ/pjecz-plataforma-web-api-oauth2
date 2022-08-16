"""
Sentencias Typer Commands
"""
from datetime import datetime

import typer
import rich

from config.settings import LIMIT, LOCAL_HUSO_HORARIO
from lib.authentication import authorization_header
import lib.exceptions

from .crud import get_sentencias

app = typer.Typer()


@app.command()
def consultar(
    limit: int = LIMIT,
    autoridad_id: int = None,
    autoridad_clave: str = None,
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
    materia_tipo_juicio_id: int = None,
    fecha: str = None,
    fecha_desde: str = None,
    fecha_hasta: str = None,
):
    """Consultar sentencias"""
    rich.print("Consultar sentencias...")
    try:
        respuesta = get_sentencias(
            authorization_header=authorization_header(),
            limit=limit,
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            materia_tipo_juicio_id=materia_tipo_juicio_id,
            fecha=fecha,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Creado", "Distrito", "Autoridad", "Fecha", "Expediente", "Descripcion", "Materia", "Tipo de Juicio", "P.G.")
    for registro in respuesta["items"]:
        creado = datetime.fromisoformat(registro["creado"])
        table.add_row(
            str(registro["id"]),
            creado.astimezone(LOCAL_HUSO_HORARIO).strftime("%Y-%m-%d %H:%M:%S"),
            registro["distrito_nombre_corto"],
            registro["autoridad_clave"],
            registro["fecha"],
            registro["expediente"],
            registro["descripcion"][:24] if len(registro["descripcion"]) > 24 else registro["descripcion"],
            registro["materia_nombre"],
            registro["materia_tipo_juicio_descripcion"][:24] if len(registro["materia_tipo_juicio_descripcion"]) > 24 else registro["materia_tipo_juicio_descripcion"],
            "SI" if registro["es_perspectiva_genero"] else "",
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] sentencias")
