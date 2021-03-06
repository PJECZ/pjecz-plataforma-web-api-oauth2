"""
Listas de Acuerdos v1, rutas (paths)
"""
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import AlredyExistsException, IsDeletedException, NotExistsException
from lib.fastapi_pagination import LimitOffsetPage

from plataforma_web.v1.listas_de_acuerdos.crud import get_listas_de_acuerdos, get_lista_de_acuerdo, insert_lista_de_acuerdo
from plataforma_web.v1.listas_de_acuerdos.schemas import ListaDeAcuerdoIn, ListaDeAcuerdoOut
from plataforma_web.v1.permisos.models import Permiso
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInDB

listas_de_acuerdos = APIRouter(prefix="/v1/listas_de_acuerdos", tags=["listas de acuerdos"])


@listas_de_acuerdos.get("", response_model=LimitOffsetPage[ListaDeAcuerdoOut])
async def listado_listas_de_acuerdos(
    autoridad_id: int = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    fecha: date = None,
    fecha_desde: date = None,
    fecha_hasta: date = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de listas de acuerdos"""
    if current_user.permissions.get("LISTAS DE ACUERDOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_listas_de_acuerdos(
            db,
            autoridad_id=autoridad_id,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            fecha=fecha,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
        )
    except (IsDeletedException, NotExistsException) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@listas_de_acuerdos.post("", response_model=ListaDeAcuerdoOut)
async def nueva_lista_de_acuerdos(
    lista_de_acuerdo: ListaDeAcuerdoIn,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Insertar una lista de acuerdos"""
    if current_user.permissions.get("LISTAS DE ACUERDOS", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultado = insert_lista_de_acuerdo(
            db,
            lista_de_acuerdo=lista_de_acuerdo,
        )
    except (IsDeletedException, NotExistsException) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    except AlredyExistsException as error:
        raise HTTPException(status_code=409, detail=f"Conflict: {str(error)}") from error
    return ListaDeAcuerdoOut.from_orm(resultado)


@listas_de_acuerdos.get("/{lista_de_acuerdo_id}", response_model=ListaDeAcuerdoOut)
async def detalle_lista_de_acuerdos(
    lista_de_acuerdo_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una lista de acuerdos a partir de su id"""
    if current_user.permissions.get("LISTAS DE ACUERDOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        consulta = get_lista_de_acuerdo(
            db,
            lista_de_acuerdo_id=lista_de_acuerdo_id,
        )
    except (IsDeletedException, NotExistsException) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return ListaDeAcuerdoOut.from_orm(consulta)
