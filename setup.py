"""
Comandos Click
"""
from setuptools import setup


setup(
    name="plataforma_web",
    version="0.1",
    packages=["plataforma_web"],
    install_requires=["click", "pandas", "requests", "sendgrid", "tabulate"],
    entry_points={
        "console_scripts": [
            "plataforma_web = cli.cli:cli",
        ],
    },
)