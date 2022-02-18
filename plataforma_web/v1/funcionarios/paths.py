"""
Funcionarios v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.fastapi_pagination import LimitOffsetPage

from plataforma_web.v1.funcionarios.crud import get_funcionarios, get_funcionario, get_funcionario_with_curp
from plataforma_web.v1.funcionarios.schemas import FuncionarioOut
from plataforma_web.v1.permisos.models import Permiso
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInBD

router = APIRouter()


@router.get("", response_model=LimitOffsetPage[FuncionarioOut])
async def listado_funcionarios(
    en_funciones: bool = None,
    en_sentencias: bool = None,
    en_soportes: bool = None,
    en_tesis_jurisprudencias: bool = None,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de funcionarios"""
    if not current_user.permissions["FUNCIONARIOS"] >= Permiso.VER:
        raise HTTPException(status_code=403, detail="Forbidden")
    return paginate(get_funcionarios(db, en_funciones, en_sentencias, en_soportes, en_tesis_jurisprudencias))


@router.get("/{funcionario_id}", response_model=FuncionarioOut)
async def detalle_funcionario(
    funcionario_id: int,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una funcionario a partir de su id"""
    if not current_user.permissions["FUNCIONARIOS"] >= Permiso.VER:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        funcionario = get_funcionario(db, funcionario_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return FuncionarioOut.from_orm(funcionario)


@router.get("/curp/{curp}", response_model=FuncionarioOut)
async def detalle_funcionario_con_curp(
    curp: str,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una funcionario a partir de su id"""
    if not current_user.permissions["FUNCIONARIOS"] >= Permiso.VER:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        funcionario = get_funcionario_with_curp(db, curp)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return FuncionarioOut.from_orm(funcionario)
