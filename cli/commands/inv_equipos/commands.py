"""
Inv Equipos Typer Commands
"""
from datetime import datetime

import pandas as pd
import typer
import rich

from config.settings import LIMIT, LOCAL_HUSO_HORARIO
from lib.authentication import authorization_header
import lib.exceptions
from lib.formats import df_to_table

from .crud import get_inv_equipos, get_inv_equipos_cantidades_por_oficina_por_tipo, get_inv_equipos_cantidades_por_oficina_por_anio_fabricacion

app = typer.Typer()


@app.command()
def consultar(
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
    fecha_fabricacion_desde: str = None,
    fecha_fabricacion_hasta: str = None,
    inv_custodia_id: int = None,
    inv_modelo_id: int = None,
    inv_red_id: int = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar equipos"""
    rich.print("Consultar equipos...")
    try:
        respuesta = get_inv_equipos(
            authorization_header=authorization_header(),
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            fecha_fabricacion_desde=fecha_fabricacion_desde,
            fecha_fabricacion_hasta=fecha_fabricacion_hasta,
            inv_custodia_id=inv_custodia_id,
            inv_modelo_id=inv_modelo_id,
            inv_red_id=inv_red_id,
            limit=limit,
            offset=offset,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Creado", "Descripcion", "Tipo", "Custodia", "Marca", "Modelo", "Red", "F. Fab.")
    for registro in respuesta["items"]:
        creado = datetime.fromisoformat(registro["creado"])
        table.add_row(
            str(registro["id"]),
            creado.astimezone(LOCAL_HUSO_HORARIO).strftime("%Y-%m-%d %H:%M:%S"),
            registro["descripcion"],
            registro["tipo"],
            str(registro["inv_custodia_id"]),
            registro["inv_marca_nombre"],
            registro["inv_modelo_descripcion"],
            registro["inv_red_nombre"],
            registro["fecha_fabricacion"],
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] equipos")


@app.command()
def cantidades_por_oficina_por_tipo(
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
):
    """Consultar cantidades de equipos por oficina y por tipo"""
    rich.print("Consultar cantidades de equipos por oficina y por tipo...")

    # Solicitar datos a la API
    try:
        respuesta = get_inv_equipos_cantidades_por_oficina_por_tipo(
            authorization_header=authorization_header(),
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Crear dataframe
    dataframe = pd.DataFrame(respuesta)
    dataframe.oficina_clave = dataframe.oficina_clave.astype("category")
    dataframe.inv_equipo_tipo = dataframe.inv_equipo_tipo.astype("category")

    # Crear pivot table
    pivot_table = dataframe.pivot_table(
        index="oficina_clave",
        columns="inv_equipo_tipo",
        values="cantidad",
        aggfunc="sum",
    )

    # Mostrar la tabla
    tabla = rich.table.Table(show_lines=False)
    tabla = df_to_table(pivot_table, tabla, "Oficinas")
    console = rich.console.Console()
    console.print(tabla)

    # Mostrar el total
    rich.print("Total: [green]XXX[/green] equipos")


@app.command()
def cantidades_por_oficina_por_anio_fabricacion(
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
):
    """Consultar cantidades de equipos por oficina y por año de fabricacion"""
    rich.print("Consultar cantidades de equipos por oficina y por año de fabricacion...")

    # Solicitar datos a la API
    try:
        respuesta = get_inv_equipos_cantidades_por_oficina_por_anio_fabricacion(
            authorization_header=authorization_header(),
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
        )
    except lib.exceptions.CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Crear dataframe
    dataframe = pd.DataFrame(respuesta)
    dataframe.oficina_clave = dataframe.oficina_clave.astype("category")
    dataframe.anio_fabricacion = dataframe.anio_fabricacion.astype("int")

    # Crear pivot table
    pivot_table = dataframe.pivot_table(
        index="oficina_clave",
        columns="anio_fabricacion",
        values="cantidad",
        aggfunc="sum",
    )

    # Mostrar la tabla
    tabla = rich.table.Table(show_lines=False)
    tabla = df_to_table(pivot_table, tabla, "Oficinas")
    console = rich.console.Console()
    console.print(tabla)

    # Mostrar el total
    rich.print("Total: [green]XXX[/green] equipos")
