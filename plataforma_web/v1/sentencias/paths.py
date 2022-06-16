"""
Sentencias v1, rutas (paths)
"""
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.fastapi_pagination import LimitOffsetPage

from plataforma_web.v1.permisos.models import Permiso
from plataforma_web.v1.sentencias.crud import get_sentencias, get_sentencia
from plataforma_web.v1.sentencias.schemas import SentenciaOut
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInDB

sentencias = APIRouter(prefix="/v1/sentencias", tags=["sentencias"])


@sentencias.get("", response_model=LimitOffsetPage[SentenciaOut])
async def listado_sentencias(
    autoridad_id: int = None,
    materia_tipo_juicio_id: int = None,
    fecha: date = None,
    fecha_desde: date = None,
    fecha_hasta: date = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de sentencias"""
    if "SENTENCIAS" not in current_user.permissions or current_user.permissions["SENTENCIAS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_sentencias(
            db,
            autoridad_id=autoridad_id,
            materia_tipo_juicio_id=materia_tipo_juicio_id,
            fecha=fecha,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
        )
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@sentencias.get("/{sentencia_id}", response_model=SentenciaOut)
async def detalle_sentencia(
    sentencia_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una sentencia a partir de su id"""
    if "SENTENCIAS" not in current_user.permissions or current_user.permissions["SENTENCIAS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        sentencia = get_sentencia(db, sentencia_id=sentencia_id)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return SentenciaOut.from_orm(sentencia)
