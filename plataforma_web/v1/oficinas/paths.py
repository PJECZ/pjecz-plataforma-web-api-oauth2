"""
Oficinas v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.fastapi_pagination import LimitOffsetPage

from plataforma_web.v1.oficinas.crud import get_oficinas, get_oficina
from plataforma_web.v1.oficinas.schemas import OficinaOut
from plataforma_web.v1.permisos.models import Permiso
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInDB

oficinas = APIRouter(prefix="/v1/oficinas", tags=["oficinas"])


@oficinas.get("", response_model=LimitOffsetPage[OficinaOut])
async def listado_oficinas(
    distrito_id: int = None,
    domicilio_id: int = None,
    es_juridicional: bool = False,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de oficinas"""
    if "OFICINAS" not in current_user.permissions or current_user.permissions["OFICINAS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_oficinas(db, distrito_id=distrito_id, domicilio_id=domicilio_id, es_jurisdiccional=es_juridicional)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@oficinas.get("/{oficina_id}", response_model=OficinaOut)
async def detalle_oficina(
    oficina_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una oficina a partir de su id"""
    if "OFICINAS" not in current_user.permissions or current_user.permissions["OFICINAS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        oficina = get_oficina(db, oficina_id=oficina_id)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return OficinaOut.from_orm(oficina)
