"""
Soportes Tickets v1, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime
from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy.sql import func
import pytz

from lib.exceptions import PWIsDeletedError, PWNotExistsError, PWNotValidParamError
from lib.safe_string import safe_string

from .models import SoporteTicket
from ..funcionarios.models import Funcionario
from ..oficinas.crud import get_oficina, get_oficina_from_clave
from ..oficinas.models import Oficina
from ..soportes_categorias.crud import get_soporte_categoria
from ..soportes_categorias.models import SoporteCategoria
from ..usuarios.crud import get_usuario, get_usuario_from_email
from ..usuarios.models import Usuario


def get_soportes_tickets(
    db: Session,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    descripcion: str = None,
    estado: str = None,
    estatus: str = None,
    oficina_id: int = None,
    oficina_clave: str = None,
    soporte_categoria_id: int = None,
    usuario_id: int = None,
    usuario_email: str = None,
) -> Any:
    """Consultar los tickets"""

    # Huso horario
    servidor_huso_horario = pytz.utc

    # Consultar
    oficina = None
    if oficina_id is not None:
        oficina = get_oficina(db, oficina_id)
    elif oficina_clave is not None:
        oficina = get_oficina_from_clave(db, oficina_clave)
    if oficina is not None:
        consulta = db.query(SoporteTicket).join(Usuario).filter(Usuario.oficina_id == oficina.id)
    else:
        consulta = db.query(SoporteTicket)

    # Filtrar por creado
    if creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(SoporteTicket.creado >= desde_dt).filter(SoporteTicket.creado <= hasta_dt)
    if creado is None and creado_desde is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        consulta = consulta.filter(SoporteTicket.creado >= desde_dt)
    if creado is None and creado_hasta is not None:
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(SoporteTicket.creado <= hasta_dt)

    # Filtrar por categoria
    if soporte_categoria_id is not None:
        soporte_categoria = get_soporte_categoria(db, soporte_categoria_id)
        consulta = consulta.filter(SoporteTicket.soporte_categoria == soporte_categoria)

    # Filtrar por descripcion
    if descripcion is not None:
        descripcion = safe_string(descripcion)
        if descripcion != "":
            consulta = consulta.filter(SoporteTicket.descripcion.contains(descripcion))

    # Filtrar por estado
    if estado is not None:
        estado = safe_string(estado)
        if estado != "":
            if estado not in SoporteTicket.ESTADOS:
                raise PWNotValidParamError("Estado incorrecto")
            consulta = consulta.filter(SoporteTicket.estado == estado)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Filtrar por usuario
    if usuario_id is not None:
        usuario = get_usuario(db, usuario_id)
        consulta = consulta.filter(SoporteTicket.usuario == usuario)
    elif usuario_email is not None:
        usuario = get_usuario_from_email(db, usuario_email)
        consulta = consulta.filter(SoporteTicket.usuario == usuario)

    # Entregar
    return consulta.order_by(SoporteTicket.id.desc())


def get_soporte_ticket(db: Session, soporte_ticket_id: int) -> SoporteTicket:
    """Consultar un ticket por su id"""
    soporte_ticket = db.query(SoporteTicket).get(soporte_ticket_id)
    if soporte_ticket is None:
        raise PWNotExistsError("No existe ese ticket")
    if soporte_ticket.estatus != "A":
        raise PWIsDeletedError("No es activo ese ticket, está eliminado")
    return soporte_ticket


def get_cantidades_por_distrito_por_categoria(
    db: Session,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    size: int = 100,
) -> Any:
    """Consultar totales de tickets por oficina y por categoria"""

    # Huso horario
    servidor_huso_horario = pytz.utc

    # Consultar
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

    # Filtrar por creado
    if creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(SoporteTicket.creado >= desde_dt).filter(SoporteTicket.creado <= hasta_dt)
    if creado is None and creado_desde is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        consulta = consulta.filter(SoporteTicket.creado >= desde_dt)
    if creado is None and creado_hasta is not None:
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(SoporteTicket.creado <= hasta_dt)

    # Ordenar y agrupar
    consulta = consulta.order_by("distrito_clave", "soporte_categoria_nombre")
    consulta = consulta.group_by("distrito_clave", "soporte_categoria_nombre")

    # Entregar
    return consulta


def get_cantidades_por_funcionario_por_estado(
    db: Session,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    size: int = 100,
) -> Any:
    """Consultar totales de tickets por oficina y por categoria"""

    # Huso horario
    servidor_huso_horario = pytz.utc

    # Consultar
    consulta = (
        db.query(
            Funcionario.nombre.label("tecnico"),
            SoporteTicket.estado.label("estado"),
            func.count("*").label("cantidad"),
        )
        .select_from(SoporteTicket)
        .join(Funcionario)
    )

    # Filtrar por creado
    if creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(SoporteTicket.creado >= desde_dt).filter(SoporteTicket.creado <= hasta_dt)
    if creado is None and creado_desde is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        consulta = consulta.filter(SoporteTicket.creado >= desde_dt)
    if creado is None and creado_hasta is not None:
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(SoporteTicket.creado <= hasta_dt)

    # Ordenar y agrupar
    consulta = consulta.order_by("distrito_clave", "soporte_categoria_nombre")
    consulta = consulta.group_by("distrito_clave", "soporte_categoria_nombre")

    # Entregar
    return consulta
