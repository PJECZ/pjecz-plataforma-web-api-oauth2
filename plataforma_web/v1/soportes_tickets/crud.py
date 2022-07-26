"""
Soportes Tickets v1, CRUD (create, read, update, and delete)
"""
from datetime import date
from typing import Any
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from lib.exceptions import IsDeletedException, NotExistsException
from lib.safe_string import safe_string

from .models import SoporteTicket
from ..oficinas.crud import get_oficina, get_oficina_from_clave
from ..oficinas.models import Oficina
from ..soportes_categorias.crud import get_soporte_categoria
from ..soportes_categorias.models import SoporteCategoria
from ..usuarios.crud import get_usuario, get_usuario_from_email
from ..usuarios.models import Usuario

HOY = date.today()
ANTIGUA_FECHA = date(year=2000, month=1, day=1)


def get_soportes_tickets(
    db: Session,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    descripcion: str = None,
    estado: str = None,
    oficina_id: int = None,
    oficina_clave: str = None,
    soporte_categoria_id: int = None,
    usuario_id: int = None,
    usuario_email: str = None,
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
    if creado:
        if not ANTIGUA_FECHA <= creado <= HOY:
            raise ValueError("Creado fuera de rango")
        consulta = consulta.filter(func.date(SoporteTicket.creado) == creado)
    else:
        if creado_desde:
            if not ANTIGUA_FECHA <= creado_desde <= HOY:
                raise ValueError("Creado fuera de rango")
            consulta = consulta.filter(SoporteTicket.creado >= creado_desde)
        if creado_hasta:
            if not ANTIGUA_FECHA <= creado_hasta <= HOY:
                raise ValueError("Creado fuera de rango")
            consulta = consulta.filter(SoporteTicket.creado <= creado_hasta)
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
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    estado: str = None,
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
    if creado:
        if not ANTIGUA_FECHA <= creado <= HOY:
            raise ValueError("Creado fuera de rango")
        consulta = consulta.filter(func.date(SoporteTicket.creado) == creado)
    else:
        if creado_desde:
            if not ANTIGUA_FECHA <= creado_desde <= HOY:
                raise ValueError("Creado fuera de rango")
            consulta = consulta.filter(SoporteTicket.creado >= creado_desde)
        if creado_hasta:
            if not ANTIGUA_FECHA <= creado_hasta <= HOY:
                raise ValueError("Creado fuera de rango")
            consulta = consulta.filter(SoporteTicket.creado <= creado_hasta)
    estado = safe_string(estado)
    if estado:
        estado = safe_string(estado)
        if estado != "":
            if estado not in SoporteTicket.ESTADOS:
                raise ValueError("Estado incorrecto")
            consulta = consulta.filter(SoporteTicket.estado == estado)
    return consulta.order_by("distrito_clave", "soporte_categoria_nombre").group_by("distrito_clave", "soporte_categoria_nombre")
