#!/usr/bin/env python3
"""
CLI Typer main application
"""
import typer

from commands.autoridades.commands import app as autoridades_app
from commands.distritos.commands import app as distritos_app
from commands.domicilios.commands import app as domicilios_app
from commands.materias.commands import app as materias_app
from commands.modulos.commands import app as modulos_app
from commands.roles.commands import app as roles_app

app = typer.Typer()
app.add_typer(autoridades_app, name="autoridades")
app.add_typer(distritos_app, name="distritos")
app.add_typer(domicilios_app, name="domicilios")
app.add_typer(materias_app, name="materias")
app.add_typer(modulos_app, name="modulos")
app.add_typer(roles_app, name="roles")

if __name__ == "__main__":
    app()
