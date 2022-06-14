"""
Inventarios Equipos v1, CRUD (create, read, update, and delete)
"""
from datetime import date
from typing import Any
from sqlalchemy.orm import Session

from lib.safe_string import safe_string
from .models import InvEquipo
from ..inv_custodias.crud import get_inv_custodia
from ..inv_modelos.crud import get_inv_modelo
from ..inv_redes.crud import get_inv_red


def get_inv_equipos(
    db: Session,
    inv_custodia_id: int = None,
    inv_modelo_id: int = None,
    inv_red_id: int = None,
    tipo: str = None,
    fecha_fabricacion_desde: date = None,
    fecha_fabricacion_hasta: date = None,
) -> Any:
    """Consultar los equipos activos"""
    consulta = db.query(InvEquipo)
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
    return consulta.filter_by(estatus="A").order_by(InvEquipo.id)


def get_inv_equipo(db: Session, inv_equipo_id: int) -> InvEquipo:
    """Consultar un equipo por su id"""
    inv_equipo = db.query(InvEquipo).get(inv_equipo_id)
    if inv_equipo is None:
        raise IndexError("No existe ese equipo")
    if inv_equipo.estatus != "A":
        raise ValueError("No es activo ese equipo, está eliminado")
    return inv_equipo
