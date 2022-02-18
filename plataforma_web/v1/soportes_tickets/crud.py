"""
Soportes Tickets v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.safe_string import safe_string
from plataforma_web.v1.soportes_tickets.models import SoporteTicket


def get_soportes_tickets(
    db: Session,
    soporte_categoria_id: int = None,
    usuario_id: int = None,
    estado: str = None,
) -> Any:
    """ Consultar los soportes_tickets activos """
    consulta = db.query(SoporteTicket)
    if soporte_categoria_id:
        consulta = consulta.filter_by(soporte_categoria_id=soporte_categoria_id)
    if usuario_id:
        consulta = consulta.filter_by(usuario_id=usuario_id)
    estado = safe_string(estado)
    if estado:
        consulta = consulta.filter_by(estado=estado)
    return consulta.filter_by(estatus="A").order_by(SoporteTicket.id)


def get_soporte_ticket(db: Session, soporte_ticket_id: int) -> SoporteTicket:
    """ Consultar un soporte_ticket por su id """
    soporte_ticket = db.query(SoporteTicket).get(soporte_ticket_id)
    if soporte_ticket is None:
        raise IndexError("No existe ese ticket")
    if soporte_ticket.estatus != "A":
        raise ValueError("No es activo ese ticket, está eliminado")
    return soporte_ticket
