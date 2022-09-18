"""
Sentencias v1, rutas (paths)
"""
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PWAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from .crud import get_sentencias, get_sentencia
from .schemas import SentenciaOut, OneSentenciaOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

sentencias = APIRouter(prefix="/v1/sentencias", tags=["sentencias"])


@sentencias.get("", response_model=CustomPage[SentenciaOut])
async def listado_sentencias(
    autoridad_id: int = None,
    autoridad_clave: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    materia_tipo_juicio_id: int = None,
    fecha: date = None,
    fecha_desde: date = None,
    fecha_hasta: date = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de sentencias"""
    if current_user.permissions.get("SENTENCIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_sentencias(
            db,
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            materia_tipo_juicio_id=materia_tipo_juicio_id,
            fecha=fecha,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
        )
    except PWAnyError as error:
        return custom_page_success_false(error)
    return paginate(listado)


@sentencias.get("/{sentencia_id}", response_model=OneSentenciaOut)
async def detalle_sentencia(
    sentencia_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una sentencia a partir de su id"""
    if current_user.permissions.get("SENTENCIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        sentencia = get_sentencia(
            db,
            sentencia_id=sentencia_id,
        )
    except PWAnyError as error:
        return OneSentenciaOut(success=False, message=str(error))
    return OneSentenciaOut.from_orm(sentencia)
