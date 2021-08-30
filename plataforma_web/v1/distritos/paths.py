"""
Distritos v1.0, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from plataforma_web.v1.roles.models import Permiso
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInBD

from plataforma_web.v1.distritos.crud import get_distritos, get_distrito
from plataforma_web.v1.distritos.schemas import DistritoOut
from plataforma_web.v1.autoridades.crud import get_autoridades
from plataforma_web.v1.autoridades.schemas import AutoridadOut

v1_distritos = APIRouter(prefix="/v1/distritos", tags=["distritos"])


@v1_distritos.get("", response_model=LimitOffsetPage[DistritoOut])
async def listado_distritos(
    solo_distritos: bool = False,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de distritos"""
    if not current_user.permissions & Permiso.VER_CATALOGOS == Permiso.VER_CATALOGOS:
        raise HTTPException(status_code=403, detail="Forbidden")
    return paginate(get_distritos(db, solo_distritos=solo_distritos))


@v1_distritos.get("/{distrito_id}", response_model=DistritoOut)
async def detalle_distrito(
    distrito_id: int,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de un distrito"""
    if not current_user.permissions & Permiso.VER_CATALOGOS == Permiso.VER_CATALOGOS:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        distrito = get_distrito(db, distrito_id=distrito_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    return DistritoOut.from_orm(distrito)


@v1_distritos.get("/{distrito_id}/autoridades", response_model=LimitOffsetPage[AutoridadOut])
async def listado_autoridades_del_distrito(
    distrito_id: int,
    materia_id: int = None,
    organo_jurisdiccional: str = None,
    con_notarias: bool = False,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de autoridades del distrito"""
    if not current_user.permissions & Permiso.VER_CATALOGOS == Permiso.VER_CATALOGOS:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        listado = get_autoridades(
            db,
            distrito_id=distrito_id,
            materia_id=materia_id,
            organo_jurisdiccional=organo_jurisdiccional,
            con_notarias=con_notarias,
        )
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)
