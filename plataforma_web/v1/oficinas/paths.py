"""
Oficinas v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.fastapi_pagination import LimitOffsetPage

from plataforma_web.v1.oficinas.crud import get_oficinas, get_oficina, get_oficina_from_clave
from plataforma_web.v1.oficinas.schemas import OficinaOut
from plataforma_web.v1.permisos.models import Permiso
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInDB

oficinas = APIRouter(prefix="/v1/oficinas", tags=["inventarios"])


@oficinas.get("", response_model=LimitOffsetPage[OficinaOut])
async def listado_oficinas(
    domicilio_id: int = None,
    es_juridicional: bool = False,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de oficinas"""
    if "OFICINAS" not in current_user.permissions or current_user.permissions["OFICINAS"] < Permiso.VER:
        raise HTTPException(status_code=403, detail="Forbidden")
    return paginate(get_oficinas(db, domicilio_id, es_juridicional))


@oficinas.get("/clave/{oficina_clave}", response_model=OficinaOut)
async def detalle_oficina_con_clave(
    oficina_clave: str,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una oficina a partir de su id"""
    if "OFICINAS" not in current_user.permissions or current_user.permissions["OFICINAS"] < Permiso.VER:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        oficina = get_oficina_from_clave(db, oficina_clave)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return OficinaOut.from_orm(oficina)


@oficinas.get("/{oficina_id}", response_model=OficinaOut)
async def detalle_oficina(
    oficina_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una oficina a partir de su id"""
    if "OFICINAS" not in current_user.permissions or current_user.permissions["OFICINAS"] < Permiso.VER:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        oficina = get_oficina(db, oficina_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return OficinaOut.from_orm(oficina)