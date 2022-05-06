"""
Funcionarios v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.fastapi_pagination import LimitOffsetPage

from plataforma_web.v1.funcionarios.crud import get_funcionarios, get_funcionario, get_funcionario_with_curp
from plataforma_web.v1.funcionarios.schemas import FuncionarioOut
from plataforma_web.v1.permisos.models import Permiso
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInDB

funcionarios = APIRouter(prefix="/v1/funcionarios", tags=["funcionarios"])


@funcionarios.get("", response_model=LimitOffsetPage[FuncionarioOut])
async def listado_funcionarios(
    en_funciones: bool = None,
    en_soportes: bool = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de funcionarios"""
    if "FUNCIONARIOS" not in current_user.permissions or current_user.permissions["FUNCIONARIOS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return paginate(get_funcionarios(db, en_funciones, en_soportes))


@funcionarios.get("/{curp}", response_model=FuncionarioOut)
async def detalle_funcionario_con_curp(
    curp: str,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una funcionario a partir de su id"""
    if "FUNCIONARIOS" not in current_user.permissions or current_user.permissions["FUNCIONARIOS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        funcionario = get_funcionario_with_curp(db, curp)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return FuncionarioOut.from_orm(funcionario)
