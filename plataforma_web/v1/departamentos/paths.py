"""
Departamentos v1.0, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from plataforma_web.v1.roles.models import Permiso
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInBD

from plataforma_web.v1.departamentos.crud import get_departamentos, get_departamento
from plataforma_web.v1.departamentos.schemas import DepartamentoOut
from plataforma_web.v1.autoridades.crud import get_autoridades
from plataforma_web.v1.autoridades.schemas import AutoridadOut

departamentos = APIRouter(prefix="/v1/departamentos", tags=["departamentos"])


@departamentos.get("", response_model=LimitOffsetPage[DepartamentoOut])
async def listado_departamentos(
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de departamentos"""
    if not current_user.permissions & Permiso.VER_CATALOGOS == Permiso.VER_CATALOGOS:
        raise HTTPException(status_code=403, detail="Forbidden")
    return paginate(get_departamentos(db))


@departamentos.get("/{departamento_id}", response_model=DepartamentoOut)
async def detalle_departamento(
    departamento_id: int,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de un departamento"""
    if not current_user.permissions & Permiso.VER_CATALOGOS == Permiso.VER_CATALOGOS:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        distrito = get_departamento(db, departamento_id=departamento_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    return DepartamentoOut.from_orm(distrito)


@departamentos.get("/{departamento_id}/autoridades", response_model=LimitOffsetPage[AutoridadOut])
async def listado_autoridades_del_departamento(
    departamento_id: int,
    materia_id: int = None,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de departamentos del distrito"""
    if not current_user.permissions & Permiso.VER_CATALOGOS == Permiso.VER_CATALOGOS:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        listado = get_autoridades(
            db,
            distrito_id=departamento_id,
            materia_id=materia_id,
        )
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)
