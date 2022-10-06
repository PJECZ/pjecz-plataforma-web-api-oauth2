"""
Listas de Acuerdos v1, rutas (paths)
"""
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PWAnyError
from lib.fastapi_pagination_custom_list import CustomList, ListResult, custom_list_success_false
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from .crud import get_listas_de_acuerdos, get_listas_de_acuerdos_sintetizar_por_creado, get_lista_de_acuerdo, insert_lista_de_acuerdo
from .schemas import ListaDeAcuerdoIn, ListaDeAcuerdoOut, OneListaDeAcuerdoOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

listas_de_acuerdos = APIRouter(prefix="/v1/listas_de_acuerdos", tags=["listas de acuerdos"])


@listas_de_acuerdos.get("", response_model=CustomPage[ListaDeAcuerdoOut])
async def listado_listas_de_acuerdos(
    autoridad_id: int = None,
    autoridad_clave: str = None,
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
        consulta = get_listas_de_acuerdos(
            db=db,
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            fecha=fecha,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
        )
    except PWAnyError as error:
        return custom_page_success_false(error)
    return paginate(consulta)


@listas_de_acuerdos.get("/sintetizar_por_creado", response_model=CustomList[ListaDeAcuerdoOut])
async def sintetizar_por_creado(
    creado: date,
    distrito_id: int = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    size: int = 100,
):
    """Listado de listas de acuerdos por distrito y creado"""
    if current_user.permissions.get("LISTAS DE ACUERDOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_listas_de_acuerdos_sintetizar_por_creado(
            db=db,
            creado=creado,
            distrito_id=distrito_id,
            size=size,
        )
    except PWAnyError as error:
        return custom_list_success_false(error)
    total = len(resultados)
    result = ListResult(total=total, items=resultados, size=size)
    return CustomList(result=result)


@listas_de_acuerdos.post("", response_model=OneListaDeAcuerdoOut)
async def nueva_lista_de_acuerdos(
    lista_de_acuerdo: ListaDeAcuerdoIn,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Insertar una lista de acuerdos"""
    if current_user.permissions.get("LISTAS DE ACUERDOS", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        lista_de_acuerdo = insert_lista_de_acuerdo(
            db=db,
            lista_de_acuerdo=lista_de_acuerdo,
        )
    except PWAnyError as error:
        return OneListaDeAcuerdoOut(success=False, message=str(error))
    return OneListaDeAcuerdoOut.from_orm(lista_de_acuerdo)


@listas_de_acuerdos.get("/{lista_de_acuerdo_id}", response_model=OneListaDeAcuerdoOut)
async def detalle_lista_de_acuerdos(
    lista_de_acuerdo_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una lista de acuerdos a partir de su id"""
    if current_user.permissions.get("LISTAS DE ACUERDOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        lista_de_acuerdo = get_lista_de_acuerdo(
            db=db,
            lista_de_acuerdo_id=lista_de_acuerdo_id,
        )
    except PWAnyError as error:
        return OneListaDeAcuerdoOut(success=False, message=str(error))
    return OneListaDeAcuerdoOut.from_orm(lista_de_acuerdo)
