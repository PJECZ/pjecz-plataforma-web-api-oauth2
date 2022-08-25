"""
Sentencias Typer Commands
"""
from datetime import datetime

import typer
import rich

from config.settings import LIMIT, LOCAL_HUSO_HORARIO, SERVIDOR_HUSO_HORARIO
from lib.authentication import authorization_header
import lib.exceptions

from .crud import get_sentencias

app = typer.Typer()


@app.command()
def consultar(
    autoridad_id: int = None,
    autoridad_clave: str = None,
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
    fecha: str = None,
    fecha_desde: str = None,
    fecha_hasta: str = None,
    limit: int = LIMIT,
    materia_tipo_juicio_id: int = None,
    offset: int = 0,
):
    """Consultar sentencias"""
    rich.print("Consultar sentencias...")
    try:
        datos = get_sentencias(
            authorization_header=authorization_header(),
            limit=limit,
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            fecha=fecha,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            materia_tipo_juicio_id=materia_tipo_juicio_id,
            offset=offset,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Creado", "Autoridad", "Fecha", "Expediente", "Materia", "Tipo de Juicio", "P.G.", "Archivo")
    for dato in datos["items"]:
        creado = datetime.fromisoformat(dato["creado"]).replace(tzinfo=SERVIDOR_HUSO_HORARIO)
        table.add_row(
            str(dato["id"]),
            creado.astimezone(LOCAL_HUSO_HORARIO).strftime("%Y-%m-%d %H:%M"),
            dato["autoridad_clave"],
            dato["fecha"],
            dato["expediente"],
            dato["materia_nombre"],
            dato["materia_tipo_juicio_descripcion"],
            "SI" if dato["es_perspectiva_genero"] else "",
            dato["archivo"],
        )
    console.print(table)
    rich.print(f"Total: [green]{datos['total']}[/green] sentencias")
