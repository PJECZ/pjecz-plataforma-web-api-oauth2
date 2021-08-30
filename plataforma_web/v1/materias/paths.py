"""
Materias v1.0, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from plataforma_web.v1.roles.models import Permiso
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInBD

from plataforma_web.v1.materias.crud import get_materias, get_materia
from plataforma_web.v1.materias.schemas import MateriaOut

v1_materias = APIRouter(prefix="/v1/materias", tags=["materias"])


@v1_materias.get("", response_model=LimitOffsetPage[MateriaOut])
async def listado_materias(
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado paginado de materias"""
    if not current_user.permissions & Permiso.VER_CATALOGOS == Permiso.VER_CATALOGOS:
        raise HTTPException(status_code=403, detail="Forbidden")
    return paginate(get_materias(db))


@v1_materias.get("/id/{materia_id}", response_model=MateriaOut)
async def detalle_materia(
    materia_id: int,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una materia a partir de su id"""
    if not current_user.permissions & Permiso.VER_CATALOGOS == Permiso.VER_CATALOGOS:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        materia = get_materia(db, materia_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    return MateriaOut.from_orm(materia)
