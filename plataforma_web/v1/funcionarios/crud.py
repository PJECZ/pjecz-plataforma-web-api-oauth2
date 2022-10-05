"""
Funcionarios v1, CRUD (create, read, update, and delete)
"""
import re
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import PWIsDeletedError, PWNotExistsError, PWNotValidParamError
from lib.safe_string import CURP_REGEXP

from .models import Funcionario


def get_funcionarios(
    db: Session,
    estatus: str = None,
    en_funciones: bool = False,
    en_soportes: bool = False,
) -> Any:
    """Consultar los funcionarios"""

    # Consultar
    consulta = db.query(Funcionario)

    # Filtrar por en funciones
    if en_funciones is True:
        consulta = consulta.filetr_by(en_funciones=True)

    # Filtrar por en soportes
    if en_soportes is True:
        consulta = consulta.filetr_by(en_soportes=True)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Entregar
    return consulta.order_by(Funcionario.curp)


def get_funcionario(db: Session, funcionario_id: int) -> Funcionario:
    """Consultar un funcionario por su id"""
    funcionario = db.query(Funcionario).get(funcionario_id)
    if funcionario is None:
        raise PWNotExistsError("No existe ese funcionario")
    if funcionario.estatus != "A":
        raise PWIsDeletedError("No es activo ese funcionario, está eliminado")
    return funcionario


def get_funcionario_with_curp(db: Session, curp: str) -> Funcionario:
    """Consultar un funcionario por su id"""
    if re.match(CURP_REGEXP, curp) is None:
        raise PWNotValidParamError("El CURP es incorrecto")
    funcionario = db.query(Funcionario).filter_by(curp=curp).first()
    if funcionario is None:
        raise PWNotExistsError("No existe ese funcionario")
    if funcionario.estatus != "A":
        raise PWIsDeletedError("No es activo ese funcionario, está eliminado")
    return funcionario
