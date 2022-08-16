#!/usr/bin/env python3
"""
CLI Typer main application
"""
import typer

from commands.autoridades.commands import app as autoridades_app
from commands.distritos.commands import app as distritos_app
from commands.domicilios.commands import app as domicilios_app
from commands.listas_de_acuerdos.commands import app as listas_de_acuerdos_app
from commands.materias.commands import app as materias_app
from commands.modulos.commands import app as modulos_app
from commands.oficinas.commands import app as oficinas_app
from commands.roles.commands import app as roles_app
from commands.usuarios.commands import app as usuarios_app

app = typer.Typer()
app.add_typer(autoridades_app, name="autoridades")
app.add_typer(distritos_app, name="distritos")
app.add_typer(domicilios_app, name="domicilios")
app.add_typer(listas_de_acuerdos_app, name="listas_de_acuerdos")
app.add_typer(materias_app, name="materias")
app.add_typer(modulos_app, name="modulos")
app.add_typer(oficinas_app, name="oficinas")
app.add_typer(roles_app, name="roles")
app.add_typer(usuarios_app, name="usuarios")

if __name__ == "__main__":
    app()
