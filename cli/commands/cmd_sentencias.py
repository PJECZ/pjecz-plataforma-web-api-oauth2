"""
Sentencias
"""
import click
import pandas as pd
import requests
from tabulate import tabulate

from cli.commands.autentificar import autentificar, BASE_URL


@click.group()
@click.option("--fecha", default="", type=str, help="Fecha a consultar")
@click.pass_context
def cli(fecha):
    """Sentencias"""


@click.command()
def enviar():
    """Enviar mensaje"""


@click.command()
@click.option("--output", default="inv_equipos.csv", type=str, help="Archivo CSV a escribir")
def guardar(output):
    """Enviar mensaje"""


@click.command()
def ver():
    """Enviar mensaje"""


cli.add_command(enviar)
cli.add_command(ver)
