"""
Inventarios Equipos v1, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime
from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy.sql import func, extract
import pytz

from lib.exceptions import PWIsDeletedError, PWNotExistsError
from lib.safe_string import safe_string

from ...core.inv_equipos.models import InvEquipo
from ...core.inv_custodias.models import InvCustodia
from ...core.oficinas.models import Oficina
from ...core.usuarios.models import Usuario

from ..inv_custodias.crud import get_inv_custodia
from ..inv_modelos.crud import get_inv_modelo
from ..inv_redes.crud import get_inv_red
from ..oficinas.crud import get_oficina, get_oficina_from_clave


def get_inv_equipos(
    db: Session,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    estatus: str = None,
    fecha_fabricacion_desde: date = None,
    fecha_fabricacion_hasta: date = None,
    inv_custodia_id: int = None,
    inv_modelo_id: int = None,
    inv_red_id: int = None,
    oficina_id: int = None,
    oficina_clave: str = None,
    tipo: str = None,
) -> Any:
    """Consultar los equipos"""

    # Huso horario
    servidor_huso_horario = pytz.utc

    # Consultar
    consulta = db.query(InvEquipo)

    # Filtrar por oficina
    if oficina_id is not None:
        oficina = get_oficina(db, oficina_id=oficina_id)
        consulta = consulta.join(InvCustodia, Usuario)
        consulta = consulta.filter(Usuario.oficina == oficina)
    elif oficina_clave is not None:
        oficina = get_oficina_from_clave(db, oficina_clave=oficina_clave)
        consulta = consulta.join(InvCustodia, Usuario)
        consulta = consulta.filter(Usuario.oficina == oficina)

    # Filtrar por creado
    if creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(InvEquipo.creado >= desde_dt).filter(InvEquipo.creado <= hasta_dt)
    if creado is None and creado_desde is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        consulta = consulta.filter(InvEquipo.creado >= desde_dt)
    if creado is None and creado_hasta is not None:
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(InvEquipo.creado <= hasta_dt)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Filtrar por fecha de fabricacion
    if fecha_fabricacion_desde is not None:
        consulta = consulta.filter(InvEquipo.fecha_fabricacion >= fecha_fabricacion_desde)
    if fecha_fabricacion_hasta is not None:
        consulta = consulta.filter(InvEquipo.fecha_fabricacion <= fecha_fabricacion_hasta)

    # Filtrar por custodia
    if inv_custodia_id is not None:
        inv_custodia = get_inv_custodia(db, inv_custodia_id=inv_custodia_id)
        consulta = consulta.filter(InvEquipo.inv_custodia == inv_custodia)

    # Filtrar por modelo
    if inv_modelo_id is not None:
        inv_modelo = get_inv_modelo(db, inv_modelo_id=inv_modelo_id)
        consulta = consulta.filter(InvEquipo.inv_modelo == inv_modelo)

    # Filtrar por red
    if inv_red_id is not None:
        inv_red = get_inv_red(db, inv_red_id=inv_red_id)
        consulta = consulta.filter(InvEquipo.inv_red == inv_red)

    # Filtrar por tipo
    if tipo is not None:
        tipo = safe_string(tipo)
        if tipo in InvEquipo.TIPOS:
            consulta = consulta.filter(InvEquipo.tipo == tipo)

    # Entregar
    return consulta.order_by(InvEquipo.id.desc())


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
    size: int = 100,
) -> Any:
    """Obtener las cantidades de equipos por oficina y por tipo"""

    # Huso horario
    servidor_huso_horario = pytz.utc

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
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(InvEquipo.creado >= desde_dt).filter(InvEquipo.creado <= hasta_dt)
    else:
        if creado_desde:
            desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
            consulta = consulta.filter(InvEquipo.creado >= desde_dt)
        if creado_hasta:
            hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
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
    size: int = 100,
) -> Any:
    """Obtener las cantidades de equipos por oficina y por año de fabricación"""

    # Huso horario
    servidor_huso_horario = pytz.utc

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
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(InvEquipo.creado >= desde_dt).filter(InvEquipo.creado <= hasta_dt)
    else:
        if creado_desde:
            desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
            consulta = consulta.filter(InvEquipo.creado >= desde_dt)
        if creado_hasta:
            hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
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
