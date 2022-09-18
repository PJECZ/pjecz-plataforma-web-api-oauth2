"""
Inventarios Equipos v1, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime
from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy.sql import func, extract

from config.settings import SERVIDOR_HUSO_HORARIO
from lib.exceptions import PWIsDeletedError, PWNotExistsError
from lib.safe_string import safe_string

from .models import InvEquipo
from ..inv_custodias.models import InvCustodia
from ..inv_equipos.models import InvEquipo
from ..oficinas.models import Oficina
from ..usuarios.models import Usuario

from ..inv_custodias.crud import get_inv_custodia
from ..inv_modelos.crud import get_inv_modelo
from ..inv_redes.crud import get_inv_red
from ..oficinas.crud import get_oficina, get_oficina_from_clave


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
    oficina_id: int = None,
    oficina_clave: str = None,
    tipo: str = None,
) -> Any:
    """Consultar los equipos activos"""
    consulta = db.query(InvEquipo)
    if oficina_id:
        oficina = get_oficina(db, oficina_id=oficina_id)
        consulta = consulta.join(InvCustodia, Usuario)
        consulta = consulta.filter(Usuario.oficina == oficina)
    elif oficina_clave:
        oficina = get_oficina_from_clave(db, oficina_clave=oficina_clave)
        consulta = consulta.join(InvCustodia, Usuario)
        consulta = consulta.filter(Usuario.oficina == oficina)
    if creado:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(SERVIDOR_HUSO_HORARIO)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(SERVIDOR_HUSO_HORARIO)
        consulta = consulta.filter(InvEquipo.creado >= desde_dt).filter(InvEquipo.creado <= hasta_dt)
    else:
        if creado_desde:
            desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(SERVIDOR_HUSO_HORARIO)
            consulta = consulta.filter(InvEquipo.creado >= desde_dt)
        if creado_hasta:
            hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(SERVIDOR_HUSO_HORARIO)
            consulta = consulta.filter(InvEquipo.creado <= hasta_dt)
    if fecha_fabricacion_desde:
        consulta = consulta.filter(InvEquipo.fecha_fabricacion >= fecha_fabricacion_desde)
    if fecha_fabricacion_hasta:
        consulta = consulta.filter(InvEquipo.fecha_fabricacion <= fecha_fabricacion_hasta)
    if inv_custodia_id:
        inv_custodia = get_inv_custodia(db, inv_custodia_id=inv_custodia_id)
        consulta = consulta.filter(InvEquipo.inv_custodia == inv_custodia)
    if inv_modelo_id:
        inv_modelo = get_inv_modelo(db, inv_modelo_id=inv_modelo_id)
        consulta = consulta.filter(InvEquipo.inv_modelo == inv_modelo)
    if inv_red_id:
        inv_red = get_inv_red(db, inv_red_id=inv_red_id)
        consulta = consulta.filter(InvEquipo.inv_red == inv_red)
    if tipo:
        tipo = safe_string(tipo)
        if tipo in InvEquipo.TIPOS:
            consulta = consulta.filter(InvEquipo.tipo == tipo)
    return consulta.filter_by(estatus="A").order_by(InvEquipo.id.desc())


def get_inv_equipo(db: Session, inv_equipo_id: int) -> InvEquipo:
    """Consultar un equipo por su id"""
    inv_equipo = db.query(InvEquipo).get(inv_equipo_id)
    if inv_equipo is None:
        raise PWNotExistsError("No existe ese equipo")
    if inv_equipo.estatus != "A":
        raise PWIsDeletedError("No es activo ese equipo, está eliminado")
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
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(SERVIDOR_HUSO_HORARIO)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(SERVIDOR_HUSO_HORARIO)
        consulta = consulta.filter(InvEquipo.creado >= desde_dt).filter(InvEquipo.creado <= hasta_dt)
    else:
        if creado_desde:
            desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(SERVIDOR_HUSO_HORARIO)
            consulta = consulta.filter(InvEquipo.creado >= desde_dt)
        if creado_hasta:
            hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(SERVIDOR_HUSO_HORARIO)
            consulta = consulta.filter(InvEquipo.creado <= hasta_dt)

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
    distrito_id: int = None,
    tipo: str = None,
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
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(SERVIDOR_HUSO_HORARIO)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(SERVIDOR_HUSO_HORARIO)
        consulta = consulta.filter(InvEquipo.creado >= desde_dt).filter(InvEquipo.creado <= hasta_dt)
    else:
        if creado_desde:
            desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(SERVIDOR_HUSO_HORARIO)
            consulta = consulta.filter(InvEquipo.creado >= desde_dt)
        if creado_hasta:
            hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(SERVIDOR_HUSO_HORARIO)
            consulta = consulta.filter(InvEquipo.creado <= hasta_dt)

    # Filtrar por distrito
    if distrito_id:
        consulta = consulta.filter(Oficina.distrito_id == distrito_id)

    # Filtrar por tipo de equipo
    if tipo:
        tipo = safe_string(tipo)
        if tipo in InvEquipo.TIPOS:
            consulta = consulta.filter(InvEquipo.tipo == tipo)

    # Filtrar por estatus
    consulta = consulta.filter(Oficina.estatus == "A")
    consulta = consulta.filter(Usuario.estatus == "A")
    consulta = consulta.filter(InvCustodia.estatus == "A")
    consulta = consulta.filter(InvEquipo.estatus == "A")

    # Ordenar y agrupar
    consulta = consulta.order_by(Oficina.clave).group_by(Oficina.clave, extract("year", InvEquipo.fecha_fabricacion))

    # Consultar y entregar
    return consulta.all()
