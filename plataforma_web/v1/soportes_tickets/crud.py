"""
Soportes Tickets v1, CRUD (create, read, update, and delete)
"""
from datetime import date
from typing import Any
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from lib.safe_string import safe_string

from plataforma_web.v1.oficinas.crud import get_oficina, get_oficina_from_clave
from plataforma_web.v1.oficinas.models import Oficina
from plataforma_web.v1.soportes_categorias.crud import get_soporte_categoria
from plataforma_web.v1.soportes_categorias.models import SoporteCategoria
from plataforma_web.v1.soportes_tickets.models import SoporteTicket
from plataforma_web.v1.usuarios.crud import get_usuario, get_usuario_from_email
from plataforma_web.v1.usuarios.models import Usuario


def get_soportes_tickets(
    db: Session,
    soporte_categoria_id: int = None,
    usuario_id: int = None,
    usuario_email: str = None,
    oficina_id: int = None,
    oficina_clave: str = None,
    estado: str = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    descripcion: str = None,
) -> Any:
    """Consultar los soportes_tickets activos"""
    oficina = None
    if oficina_id:
        oficina = get_oficina(db, oficina_id)
    elif oficina_clave:
        oficina = get_oficina_from_clave(db, oficina_clave)
    if oficina:
        consulta = db.query(SoporteTicket).join(Usuario).filter(Usuario.oficina_id == oficina.id)
    else:
        consulta = db.query(SoporteTicket)
    if soporte_categoria_id:
        soporte_categoria = get_soporte_categoria(db, soporte_categoria_id)
        consulta = consulta.filter(SoporteTicket.soporte_categoria == soporte_categoria)
    if usuario_id:
        usuario = get_usuario(db, usuario_id)
        consulta = consulta.filter(SoporteTicket.usuario == usuario)
    elif usuario_email:
        usuario = get_usuario_from_email(db, usuario_email)
        consulta = consulta.filter(SoporteTicket.usuario == usuario)
    estado = safe_string(estado)
    if estado:
        if estado not in SoporteTicket.ESTADOS:
            raise ValueError("Estado incorrecto")
        consulta = consulta.filter(SoporteTicket.estado == estado)
    if creado_desde:
        if not date(year=2000, month=1, day=1) <= creado_desde <= date.today():
            raise ValueError("Fecha fuera de rango")
        consulta = consulta.filter(SoporteTicket.creado >= creado_desde)
    if creado_hasta:
        if not date(year=2000, month=1, day=1) <= creado_hasta <= date.today():
            raise ValueError("Fecha fuera de rango")
        consulta = consulta.filter(SoporteTicket.creado <= creado_hasta)
    descripcion = safe_string(descripcion)
    if descripcion:
        consulta = consulta.filter(SoporteTicket.descripcion.contains(descripcion))
    return consulta.filter_by(estatus="A").order_by(SoporteTicket.id.desc())


def get_soporte_ticket(db: Session, soporte_ticket_id: int) -> SoporteTicket:
    """Consultar un soporte_ticket por su id"""
    soporte_ticket = db.query(SoporteTicket).get(soporte_ticket_id)
    if soporte_ticket is None:
        raise IndexError("No existe ese ticket")
    if soporte_ticket.estatus != "A":
        raise ValueError("No es activo ese ticket, está eliminado")
    return soporte_ticket


def get_cantidades_distrito_categoria(
    db: Session,
    estado: str = None,
    creado_desde: date = None,
    creado_hasta: date = None,
) -> Any:
    """Consultar totales de tickets por oficina y por categoria"""
    consulta = (
        db.query(
            func.substring(Oficina.clave, 1, 4).label("distrito_clave"),
            SoporteCategoria.nombre.label("soporte_categoria_nombre"),
            func.count("*").label("cantidad"),
        )
        .select_from(SoporteTicket)
        .join(Usuario)
        .join(Oficina)
        .join(SoporteCategoria)
    )
    estado = safe_string(estado)
    if estado:
        estado = safe_string(estado)
        if estado != "":
            if estado not in SoporteTicket.ESTADOS:
                raise ValueError("Estado incorrecto")
            consulta = consulta.filter(SoporteTicket.estado == estado)
    if creado_desde:
        if not date(year=2000, month=1, day=1) <= creado_desde <= date.today():
            raise ValueError("Fecha fuera de rango")
        consulta = consulta.filter(SoporteTicket.creado >= creado_desde)
    if creado_hasta:
        if not date(year=2000, month=1, day=1) <= creado_hasta <= date.today():
            raise ValueError("Fecha fuera de rango")
        consulta = consulta.filter(SoporteTicket.creado <= creado_hasta)
    return consulta.order_by("distrito_clave", "soporte_categoria_nombre").group_by("distrito_clave", "soporte_categoria_nombre")
