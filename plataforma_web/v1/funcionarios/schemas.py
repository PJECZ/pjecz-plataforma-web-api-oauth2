"""
Funcionarios v1, esquemas de pydantic
"""
from datetime import date
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class FuncionarioOut(BaseModel):
    """Esquema para entregar funcionario"""

    id: int | None
    nombres: str | None
    apellido_paterno: str | None
    apellido_materno: str | None
    curp: str | None
    email: str | None
    puesto: str | None
    en_funciones: bool | None
    en_soportes: bool | None
    telefono: str | None
    extension: str | None
    domicilio_oficial: str | None
    ingreso_fecha: date | None
    puesto_clave: str | None
    fotografia_url: str | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneFuncionarioOut(FuncionarioOut, OneBaseOut):
    """Esquema para entregar un funcionario"""
