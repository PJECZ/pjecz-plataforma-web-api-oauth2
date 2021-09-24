"""
Sentencias v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from plataforma_web.v1.roles.models import Permiso
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInBD

from plataforma_web.v1.sentencias.crud import get_sentencias, get_sentencia
from plataforma_web.v1.sentencias.schemas import SentenciaOut

sentencias = APIRouter(prefix="/v1/sentencias", tags=["sentencias"])


@sentencias.get("", response_model=LimitOffsetPage[SentenciaOut])
async def listado_sentencias(
    autoridad_id: int = None,
    materia_tipo_juicio_id: int = None,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de sentencias"""
    if not current_user.permissions & Permiso.VER_JUSTICIABLES == Permiso.VER_JUSTICIABLES:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        listado = get_sentencias(
            db,
            autoridad_id=autoridad_id,
            materia_tipo_juicio_id=materia_tipo_juicio_id,
        )
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@sentencias.get("/{sentencia_id}", response_model=SentenciaOut)
async def detalle_sentencia(
    sentencia_id: int,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una sentencia a partir de su id"""
    if not current_user.permissions & Permiso.VER_JUSTICIABLES == Permiso.VER_JUSTICIABLES:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        sentencia = get_sentencia(db, sentencia_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return SentenciaOut.from_orm(sentencia)
