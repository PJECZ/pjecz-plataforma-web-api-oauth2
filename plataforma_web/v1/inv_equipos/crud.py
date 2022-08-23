"""
Inventarios Equipos v1, CRUD (create, read, update, and delete)
"""
from datetime import date
from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy.sql import func, extract

from lib.exceptions import IsDeletedException, NotExistsException, OutOfRangeException
from lib.safe_string import safe_string

from .models import InvEquipo
from ..inv_custodias.models import InvCustodia
from ..inv_equipos.models import InvEquipo
from ..inv_marcas.models import InvMarca
from ..inv_modelos.models import InvModelo
from ..oficinas.models import Oficina
from ..usuarios.models import Usuario

from ..inv_custodias.crud import get_inv_custodia
from ..inv_modelos.crud import get_inv_modelo
from ..inv_redes.crud import get_inv_red

HOY = date.today()
ANTIGUA_FECHA = date(year=2000, month=1, day=1)


def get_inv_equipos(
    db: Session,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    fecha_fabricacion_desde: date = None,
    fecha_fabricacion_hasta: date = None,
    inv_custodia_id: int = None,
    inv_modelo_id: int = None,
    inv_red_id: int = None,
    tipo: str = None,
) -> Any:
    """Consultar los equipos activos"""
    consulta = db.query(InvEquipo)
    if creado:
        if not ANTIGUA_FECHA <= creado <= HOY:
            raise OutOfRangeException("Creado fuera de rango")
        consulta = consulta.filter(func.date(InvEquipo.creado) == creado)
    else:
        if creado_desde:
            if not ANTIGUA_FECHA <= creado_desde <= HOY:
                raise OutOfRangeException("Creado fuera de rango")
            consulta = consulta.filter(InvEquipo.creado >= creado_desde)
        if creado_hasta:
            if not ANTIGUA_FECHA <= creado_hasta <= HOY:
                raise OutOfRangeException("Creado fuera de rango")
            consulta = consulta.filter(InvEquipo.creado <= creado_hasta)
    if inv_custodia_id:
        inv_custodia = get_inv_custodia(db, inv_custodia_id=inv_custodia_id)
        consulta = consulta.filter(InvEquipo.inv_custodia == inv_custodia)
    if inv_modelo_id:
        inv_modelo = get_inv_modelo(db, inv_modelo_id=inv_modelo_id)
        consulta = consulta.filter(InvEquipo.inv_modelo == inv_modelo)
    if inv_red_id:
        inv_red = get_inv_red(db, inv_red_id=inv_red_id)
        consulta = consulta.filter(InvEquipo.inv_red == inv_red)
    tipo = safe_string(tipo)
    if tipo:
        consulta = consulta.filter_by(tipo=tipo)
    if fecha_fabricacion_desde:
        consulta = consulta.filter(InvEquipo.fecha_fabricacion >= fecha_fabricacion_desde)
    if fecha_fabricacion_hasta:
        consulta = consulta.filter(InvEquipo.fecha_fabricacion <= fecha_fabricacion_hasta)
    return consulta.filter_by(estatus="A").order_by(InvEquipo.id.desc())


def get_inv_equipo(db: Session, inv_equipo_id: int) -> InvEquipo:
    """Consultar un equipo por su id"""
    inv_equipo = db.query(InvEquipo).get(inv_equipo_id)
    if inv_equipo is None:
        raise NotExistsException("No existe ese equipo")
    if inv_equipo.estatus != "A":
        raise IsDeletedException("No es activo ese equipo, está eliminado")
    return inv_equipo


def get_inv_equipos_cantidades_por_oficina_por_tipo(
    db: Session,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
) -> Any:
    """Obtener las cantidades de equipos por oficina y por tipo"""

    # Consultar la oficina, el tipo de equipo y las cantidades
    consulta = (
        db.query(
            Oficina.clave.label("oficina_clave"),
            InvEquipo.tipo.label("inv_equipo_tipo"),
            func.count("*").label("cantidad"),
        )
        .select_from(InvEquipo)
        .join(InvCustodia, Usuario, Oficina)
    )

    # Filtrar por fecha de creación
    if creado:
        if not ANTIGUA_FECHA <= creado <= HOY:
            raise OutOfRangeException("Creado fuera de rango")
        consulta = consulta.filter(func.date(InvEquipo.creado) == creado)
    else:
        if creado_desde:
            if not ANTIGUA_FECHA <= creado_desde <= HOY:
                raise OutOfRangeException("Creado fuera de rango")
            consulta = consulta.filter(InvEquipo.creado >= creado_desde)
        if creado_hasta:
            if not ANTIGUA_FECHA <= creado_hasta <= HOY:
                raise OutOfRangeException("Creado fuera de rango")
            consulta = consulta.filter(InvEquipo.creado <= creado_hasta)

    # Filtrar por estatus
    consulta = consulta.filter(Oficina.estatus == "A")
    consulta = consulta.filter(Usuario.estatus == "A")
    consulta = consulta.filter(InvCustodia.estatus == "A")
    consulta = consulta.filter(InvEquipo.estatus == "A")

    # Ordenar y agrupar
    consulta = consulta.order_by(InvEquipo.tipo).group_by(Oficina.clave, InvEquipo.tipo)

    # Consultar y entregar
    return consulta.all()


def get_inv_equipos_cantidades_por_oficina_por_anio_fabricacion(
    db: Session,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
) -> Any:
    """Obtener las cantidades de equipos por oficina y por año de fabricación"""

    # Consultar el funcionario, el tipo de equipo y las cantidades
    consulta = (
        db.query(
            Oficina.clave.label("oficina_clave"),
            extract("year", InvEquipo.fecha_fabricacion).label("anio_fabricacion"),
            func.count("*").label("cantidad"),
        )
        .select_from(InvEquipo)
        .join(InvCustodia, Usuario, Oficina)
    )

    # Filtrar por los que si tengan fecha de fabricación
    consulta = consulta.filter(InvEquipo.fecha_fabricacion != None)

    # Filtrar por fecha de creación
    if creado:
        if not ANTIGUA_FECHA <= creado <= HOY:
            raise OutOfRangeException("Creado fuera de rango")
        consulta = consulta.filter(func.date(InvEquipo.creado) == creado)
    else:
        if creado_desde:
            if not ANTIGUA_FECHA <= creado_desde <= HOY:
                raise OutOfRangeException("Creado fuera de rango")
            consulta = consulta.filter(InvEquipo.creado >= creado_desde)
        if creado_hasta:
            if not ANTIGUA_FECHA <= creado_hasta <= HOY:
                raise OutOfRangeException("Creado fuera de rango")
            consulta = consulta.filter(InvEquipo.creado <= creado_hasta)

    # Filtrar por estatus
    consulta = consulta.filter(Oficina.estatus == "A")
    consulta = consulta.filter(Usuario.estatus == "A")
    consulta = consulta.filter(InvCustodia.estatus == "A")
    consulta = consulta.filter(InvEquipo.estatus == "A")

    # Ordenar y agrupar
    consulta = consulta.order_by(Oficina.clave).group_by(Oficina.clave, extract("year", InvEquipo.fecha_fabricacion))

    # Consultar y entregar
    return consulta.all()
