"""
Soportes Tickets v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.fastapi_pagination import LimitOffsetPage

from plataforma_web.v1.permisos.models import Permiso
from plataforma_web.v1.soportes_tickets.crud import get_soportes_tickets, get_soporte_ticket
from plataforma_web.v1.soportes_tickets.schemas import SoporteTicketOut
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInDB

soportes_tickets = APIRouter(prefix="/v1/soportes_tickets", tags=["soportes"])


@soportes_tickets.get("", response_model=LimitOffsetPage[SoporteTicketOut])
async def listado_soportes_tickets(
    soporte_categoria_id: int = None,
    usuario_id: int = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de tickets de soporte"""
    if "SOPORTE TICKETS" not in current_user.permissions or current_user.permissions["SOPORTE TICKETS"] < Permiso.VER:
        raise HTTPException(status_code=403, detail="Forbidden")
    return paginate(get_soportes_tickets(db, soporte_categoria_id, usuario_id))


@soportes_tickets.get("/{soporte_ticket_id}", response_model=SoporteTicketOut)
async def detalle_soporte_ticket(
    soporte_ticket_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una ticket a partir de su id"""
    if not current_user.can_view("SOPORTE TICKETS"):
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        soporte_ticket = get_soporte_ticket(db, soporte_ticket_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return SoporteTicketOut.from_orm(soporte_ticket)