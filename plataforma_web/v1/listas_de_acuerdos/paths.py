"""
Listas de Acuerdos v1, rutas (paths)
"""
from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PlataformaWebAnyError
from lib.fastapi_pagination import LimitOffsetPage

from .crud import get_listas_de_acuerdos, get_listas_de_acuerdos_por_distrito_por_creado, get_lista_de_acuerdo, insert_lista_de_acuerdo
from .schemas import ListaDeAcuerdoIn, ListaDeAcuerdoOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

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
    except PlataformaWebAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@listas_de_acuerdos.get("/por_distrito_por_creado", response_model=List)
async def listado_listas_de_acuerdos_por_distrito_por_creado(
    creado: date,
    distrito_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de listas de acuerdos por distrito y creado"""
    if current_user.permissions.get("LISTAS DE ACUERDOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_listas_de_acuerdos_por_distrito_por_creado(
            db=db,
            creado=creado,
            distrito_id=distrito_id,
        )
    except PlataformaWebAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return listado


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
    except PlataformaWebAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
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
    except PlataformaWebAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return ListaDeAcuerdoOut.from_orm(consulta)
