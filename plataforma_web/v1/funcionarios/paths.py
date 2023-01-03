"""
Funcionarios v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PWAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from ...core.permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

from .crud import get_funcionarios, get_funcionario
from .schemas import FuncionarioOut, OneFuncionarioOut

funcionarios = APIRouter(prefix="/v1/funcionarios", tags=["funcionarios"])


@funcionarios.get("", response_model=CustomPage[FuncionarioOut])
async def listado_funcionarios(
    en_funciones: bool = None,
    en_soportes: bool = None,
    estatus: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de funcionarios"""
    if current_user.permissions.get("FUNCIONARIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        consulta = get_funcionarios(
            db=db,
            en_funciones=en_funciones,
            en_soportes=en_soportes,
            estatus=estatus,
        )
    except PWAnyError as error:
        return custom_page_success_false(error)
    return paginate(consulta)


@funcionarios.get("/{funcionario_id}", response_model=OneFuncionarioOut)
async def detalle_funcionario(
    funcionario_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una funcionario a partir de su id"""
    if current_user.permissions.get("FUNCIONARIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        funcionario = get_funcionario(
            db=db,
            funcionario_id=funcionario_id,
        )
    except PWAnyError as error:
        return OneFuncionarioOut(success=False, message=str(error))
    return OneFuncionarioOut.from_orm(funcionario)
