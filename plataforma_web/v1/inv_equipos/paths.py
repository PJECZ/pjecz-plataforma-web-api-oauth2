"""
Inventarios Equipos v1, rutas (paths)
"""
from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.fastapi_pagination import LimitOffsetPage

from plataforma_web.v1.inv_equipos.crud import get_inv_equipos, get_inv_equipo, get_matriz, get_cantidades_oficina_tipo
from plataforma_web.v1.inv_equipos.schemas import InvEquipoOut, MatrizOut, CantidadesOficinaTipoOut
from plataforma_web.v1.permisos.models import Permiso
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInDB

inv_equipos = APIRouter(prefix="/v1/inv_equipos", tags=["inventarios"])


@inv_equipos.get("", response_model=LimitOffsetPage[InvEquipoOut])
async def listado_inv_equipos(
    inv_custodia_id: int = None,
    inv_modelo_id: int = None,
    inv_red_id: int = None,
    tipo: str = None,
    fecha_fabricacion_desde: date = None,
    fecha_fabricacion_hasta: date = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de inventarios"""
    if "INV EQUIPOS" not in current_user.permissions or current_user.permissions["INV EQUIPOS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_inv_equipos(
            db,
            inv_custodia_id=inv_custodia_id,
            inv_modelo_id=inv_modelo_id,
            inv_red_id=inv_red_id,
            tipo=tipo,
            fecha_fabricacion_desde=fecha_fabricacion_desde,
            fecha_fabricacion_hasta=fecha_fabricacion_hasta,
        )
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@inv_equipos.get("/matriz", response_model=List[MatrizOut])
async def matriz(
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Matriz de equipos"""
    if "INV EQUIPOS" not in current_user.permissions or current_user.permissions["INV EQUIPOS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        consulta = get_matriz(db)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return consulta.all()


@inv_equipos.get("/cantidades_oficina_tipo", response_model=List[CantidadesOficinaTipoOut])
async def listado_cantidades_oficina_tipo(
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Cantidades de equipos por oficina y tipo"""
    if "INV EQUIPOS" not in current_user.permissions or current_user.permissions["INV EQUIPOS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        consulta = get_cantidades_oficina_tipo(
            db,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
        )
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return consulta.all()


@inv_equipos.get("/{inv_equipo_id}", response_model=InvEquipoOut)
async def detalle_inv_equipo(
    inv_equipo_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una inventarios a partir de su id"""
    if "INV EQUIPOS" not in current_user.permissions or current_user.permissions["INV EQUIPOS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        inv_equipo = get_inv_equipo(db, inv_equipo_id=inv_equipo_id)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return InvEquipoOut.from_orm(inv_equipo)
