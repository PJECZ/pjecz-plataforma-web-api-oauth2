#!/usr/bin/env python3
"""
CLI Typer main application
"""
import typer

from commands.materias.commands import app as materias_app

app = typer.Typer()
app.add_typer(materias_app, name="materias")

if __name__ == "__main__":
    app()
