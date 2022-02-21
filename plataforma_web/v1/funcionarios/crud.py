"""
Funcionarios v1, CRUD (create, read, update, and delete)
"""
import re
from typing import Any
from sqlalchemy.orm import Session

from lib.safe_string import CURP_REGEXP

from plataforma_web.v1.funcionarios.models import Funcionario


def get_funcionarios(
    db: Session,
    en_funciones: bool = False,
    en_sentencias: bool = False,
    en_soportes: bool = False,
    en_tesis_jurisprudencias: bool = False,
) -> Any:
    """Consultar los funcionarios activos"""
    consulta = db.query(Funcionario)
    if en_funciones is True:
        consulta = consulta.filetr_by(en_funciones=True)
    if en_sentencias is True:
        consulta = consulta.filetr_by(en_sentencias=True)
    if en_soportes is True:
        consulta = consulta.filetr_by(en_soportes=True)
    if en_tesis_jurisprudencias is True:
        consulta = consulta.filetr_by(en_tesis_jurisprudencias=True)
    return consulta.filter_by(estatus="A").order_by(Funcionario.id.desc())


def get_funcionario(db: Session, funcionario_id: int) -> Funcionario:
    """Consultar un funcionario por su id"""
    funcionario = db.query(Funcionario).get(funcionario_id)
    if funcionario is None:
        raise IndexError("No existe ese funcionario")
    if funcionario.estatus != "A":
        raise ValueError("No es activo ese funcionario, está eliminado")
    return funcionario


def get_funcionario_with_curp(db: Session, curp: str) -> Funcionario:
    """Consultar un funcionario por su id"""
    if re.match(CURP_REGEXP, curp) is None:
        raise ValueError("El CURP es incorrecto")
    funcionario = db.query(Funcionario).filter_by(curp=curp).first()
    if funcionario is None:
        raise IndexError("No existe ese funcionario")
    if funcionario.estatus != "A":
        raise ValueError("No es activo ese funcionario, está eliminado")
    return funcionario
