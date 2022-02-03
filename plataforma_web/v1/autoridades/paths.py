"""
Autoridades v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInBD

from plataforma_web.v1.autoridades.crud import get_autoridades, get_autoridad, get_autoridad_from_clave
from plataforma_web.v1.autoridades.schemas import AutoridadOut
from plataforma_web.v1.listas_de_acuerdos.crud import get_listas_de_acuerdos
from plataforma_web.v1.listas_de_acuerdos.schemas import ListaDeAcuerdoOut
from plataforma_web.v1.sentencias.crud import get_sentencias
from plataforma_web.v1.sentencias.schemas import SentenciaOut
from plataforma_web.v1.usuarios.crud import get_usuarios
from plataforma_web.v1.usuarios.schemas import UsuarioOut

MODULO = "AUTORIDADES"

autoridades = APIRouter(prefix="/v1/autoridades", tags=["autoridades"])


@autoridades.get("", response_model=LimitOffsetPage[AutoridadOut])
async def listado_autoridades(
    distrito_id: int = None,
    materia_id: int = None,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de autoridades"""
    if not current_user.can_view(MODULO):
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        listado = get_autoridades(
            db,
            distrito_id=distrito_id,
            materia_id=materia_id,
        )
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@autoridades.get("/clave/{clave}", response_model=AutoridadOut)
async def detalle_autoridad_con_clave(
    clave: str,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una autoridad a partir de su clave"""
    if not current_user.can_view(MODULO):
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        autoridad = get_autoridad_from_clave(db, clave=clave)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return AutoridadOut.from_orm(autoridad)


@autoridades.get("/{autoridad_id}", response_model=AutoridadOut)
async def detalle_autoridad(
    autoridad_id: int,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una autoridad a partir de su id"""
    if not current_user.can_view(MODULO):
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        autoridad = get_autoridad(db, autoridad_id=autoridad_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return AutoridadOut.from_orm(autoridad)


@autoridades.get("/{autoridad_id}/listas_de_acuerdos", response_model=LimitOffsetPage[ListaDeAcuerdoOut])
async def listado_listas_de_acuerdos_de_autoridad(
    autoridad_id: int,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de listas de acuerdos de una autoridad"""
    if not current_user.can_view("LISTAS DE ACUERDOS"):
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        listado = get_listas_de_acuerdos(db, autoridad_id=autoridad_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@autoridades.get("/{autoridad_id}/sentencias", response_model=LimitOffsetPage[SentenciaOut])
async def listado_sentencias_de_autoridad(
    autoridad_id: int,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de sentencias de una autoridad"""
    if not current_user.can_view("LISTAS DE ACUERDOS ACUERDOS"):
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        listado = get_sentencias(db, autoridad_id=autoridad_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@autoridades.get("/{autoridad_id}/usuarios", response_model=LimitOffsetPage[UsuarioOut])
async def listado_usuarios_de_autoridad(
    autoridad_id: int,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de usuarios de una autoridad"""
    if not current_user.can_view("USUARIOS"):
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        listado = get_usuarios(db, autoridad_id=autoridad_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)
