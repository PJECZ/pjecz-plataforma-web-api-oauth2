"""
Soportes Tickets v1, rutas (paths)
"""
from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import IsDeletedException, NotExistsException
from lib.fastapi_pagination import LimitOffsetPage

from plataforma_web.v1.permisos.models import Permiso
from plataforma_web.v1.soportes_tickets.crud import get_soportes_tickets, get_soporte_ticket, get_cantidades_distrito_categoria
from plataforma_web.v1.soportes_tickets.schemas import SoporteTicketOut, SoporteTicketTotalOut
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInDB

soportes_tickets = APIRouter(prefix="/v1/soportes_tickets", tags=["soportes"])


@soportes_tickets.get("", response_model=LimitOffsetPage[SoporteTicketOut])
async def listado_soportes_tickets(
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    descripcion: str = None,
    estado: str = None,
    soporte_categoria_id: int = None,
    oficina_id: int = None,
    oficina_clave: str = None,
    usuario_id: int = None,
    usuario_email: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de tickets de soporte"""
    if "SOPORTES TICKETS" not in current_user.permissions or current_user.permissions["SOPORTES TICKETS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_soportes_tickets(
            db,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            descripcion=descripcion,
            estado=estado,
            soporte_categoria_id=soporte_categoria_id,
            oficina_id=oficina_id,
            oficina_clave=oficina_clave,
            usuario_id=usuario_id,
            usuario_email=usuario_email,
        )
    except (IsDeletedException, NotExistsException) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@soportes_tickets.get("/cantidades_distrito_categoria", response_model=List[SoporteTicketTotalOut])
async def listado_cantidades_distrito_categoria(
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    estado: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de totales de tickets por oficina y por categoria"""
    if "SOPORTES TICKETS" not in current_user.permissions or current_user.permissions["SOPORTES TICKETS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        consulta = get_cantidades_distrito_categoria(
            db,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            estado=estado,
        )
    except (IsDeletedException, NotExistsException) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return consulta.all()


@soportes_tickets.get("/{soporte_ticket_id}", response_model=SoporteTicketOut)
async def detalle_soporte_ticket(
    soporte_ticket_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una ticket a partir de su id"""
    if "SOPORTES TICKETS" not in current_user.permissions or current_user.permissions["SOPORTES TICKETS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        soporte_ticket = get_soporte_ticket(
            db,
            soporte_ticket_id=soporte_ticket_id,
        )
    except (IsDeletedException, NotExistsException) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return SoporteTicketOut.from_orm(soporte_ticket)
