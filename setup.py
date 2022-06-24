"""
Comandos Click
"""
from setuptools import setup


setup(
    name="plataforma_web",
    version="0.1",
    packages=["plataforma_web"],
    install_requires=["click", "openpyxl", "pandas", "python-dotenv", "requests", "sendgrid", "tabulate"],
    entry_points={
        "console_scripts": [
            "plataforma_web = cli.cli:cli",
        ],
    },
)
