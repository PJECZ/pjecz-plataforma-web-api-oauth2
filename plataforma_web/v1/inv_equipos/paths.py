"""
Inventarios Equipos v1, rutas (paths)
"""
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PWAnyError
from lib.fastapi_pagination_custom_list import CustomList, ListResult, custom_list_success_false
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from ...core.permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

from .crud import (
    get_inv_equipos,
    get_inv_equipo,
    get_inv_equipos_cantidades_por_oficina_por_tipo,
    get_inv_equipos_cantidades_por_oficina_por_anio_fabricacion,
)
from .schemas import (
    InvEquipoOut,
    OneInvEquipoOut,
    CantidadesOficinaTipoOut,
    CantidadesOficinaAnioFabricacionOut,
)

inv_equipos = APIRouter(prefix="/v1/inv_equipos", tags=["inventarios"])


@inv_equipos.get("", response_model=CustomPage[InvEquipoOut])
async def listado_inv_equipos(
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    estatus: str = None,
    fecha_fabricacion_desde: date = None,
    fecha_fabricacion_hasta: date = None,
    inv_custodia_id: int = None,
    inv_modelo_id: int = None,
    inv_red_id: int = None,
    oficina_id: int = None,
    oficina_clave: str = None,
    tipo: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de inventarios"""
    if current_user.permissions.get("INV EQUIPOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        consulta = get_inv_equipos(
            db=db,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            estatus=estatus,
            fecha_fabricacion_desde=fecha_fabricacion_desde,
            fecha_fabricacion_hasta=fecha_fabricacion_hasta,
            inv_custodia_id=inv_custodia_id,
            inv_modelo_id=inv_modelo_id,
            inv_red_id=inv_red_id,
            oficina_id=oficina_id,
            oficina_clave=oficina_clave,
            tipo=tipo,
        )
    except PWAnyError as error:
        return custom_page_success_false(error)
    return paginate(consulta)


@inv_equipos.get("/cantidades_por_oficina_por_tipo", response_model=CustomList[CantidadesOficinaTipoOut])
async def cantidades_por_oficina_por_tipo(
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    size: int = 100,
):
    """Cantidades de equipos por oficina y tipo"""
    if current_user.permissions.get("INV EQUIPOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_inv_equipos_cantidades_por_oficina_por_tipo(
            db=db,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            size=size,
        )
    except PWAnyError as error:
        return custom_list_success_false(error)
    items = []
    for oficina_clave, inv_equipo_tipo, cantidad in resultados.all():
        items.append(CantidadesOficinaTipoOut(oficina_clave=oficina_clave, inv_equipo_tipo=inv_equipo_tipo, cantidad=cantidad))
    total = sum(item.cantidad for item in items)
    result = ListResult(total=total, items=items, size=size)
    return CustomList(result=result)


@inv_equipos.get("/cantidades_por_oficina_por_anio_fabricacion", response_model=CustomList[CantidadesOficinaAnioFabricacionOut])
async def cantidades_por_oficina_por_anio_fabricacion(
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    distrito_id: int = None,
    tipo: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    size: int = 100,
):
    """Cantidades de equipos por oficina y año de fabricación"""
    if current_user.permissions.get("INV EQUIPOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_inv_equipos_cantidades_por_oficina_por_anio_fabricacion(
            db=db,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            distrito_id=distrito_id,
            tipo=tipo,
            size=size,
        )
    except PWAnyError as error:
        return custom_list_success_false(error)
    items = []
    for oficina_clave, anio_fabricacion, cantidad in resultados.all():
        items.append(CantidadesOficinaAnioFabricacionOut(oficina_clave=oficina_clave, anio_fabricacion=anio_fabricacion, cantidad=cantidad))
    total = sum(item.cantidad for item in items)
    result = ListResult(total=total, items=items, size=size)
    return CustomList(result=result)


@inv_equipos.get("/{inv_equipo_id}", response_model=OneInvEquipoOut)
async def detalle_inv_equipo(
    inv_equipo_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una inventarios a partir de su id"""
    if current_user.permissions.get("INV EQUIPOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        inv_equipo = get_inv_equipo(
            db=db,
            inv_equipo_id=inv_equipo_id,
        )
    except PWAnyError as error:
        return OneInvEquipoOut(success=False, message=str(error))
    return OneInvEquipoOut.from_orm(inv_equipo)
