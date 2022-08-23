"""
Inventarios Equipos v1, rutas (paths)
"""
from datetime import date
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PlataformaWebAnyError
from lib.fastapi_pagination import LimitOffsetPage

from .crud import get_inv_equipos, get_inv_equipo, get_inv_equipos_cantidades_por_oficina_por_tipo
from .schemas import InvEquipoOut, CantidadesOficinaTipoOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

inv_equipos = APIRouter(prefix="/v1/inv_equipos", tags=["inventarios"])


@inv_equipos.get("", response_model=LimitOffsetPage[InvEquipoOut])
async def listado_inv_equipos(
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    fecha_fabricacion_desde: date = None,
    fecha_fabricacion_hasta: date = None,
    inv_custodia_id: int = None,
    inv_modelo_id: int = None,
    inv_red_id: int = None,
    tipo: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de inventarios"""
    if current_user.permissions.get("INV EQUIPOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_inv_equipos(
            db,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            fecha_fabricacion_desde=fecha_fabricacion_desde,
            fecha_fabricacion_hasta=fecha_fabricacion_hasta,
            inv_custodia_id=inv_custodia_id,
            inv_modelo_id=inv_modelo_id,
            inv_red_id=inv_red_id,
            tipo=tipo,
        )
    except PlataformaWebAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@inv_equipos.get("/cantidades_por_oficina_por_tipo", response_model=List[CantidadesOficinaTipoOut])
async def cantidades_por_oficina_por_tipo(
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Cantidades de equipos por oficina y tipo"""
    if current_user.permissions.get("INV EQUIPOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_inv_equipos_cantidades_por_oficina_por_tipo(
            db,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
        )
    except PlataformaWebAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return resultados


@inv_equipos.get("/{inv_equipo_id}", response_model=InvEquipoOut)
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
            db,
            inv_equipo_id=inv_equipo_id,
        )
    except PlataformaWebAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return InvEquipoOut.from_orm(inv_equipo)
