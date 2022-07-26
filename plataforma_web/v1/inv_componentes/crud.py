"""
Inventarios Componentes v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import IsDeletedException, NotExistsException
from lib.safe_string import safe_string

from .models import InvComponente
from ..inv_categorias.crud import get_inv_categoria
from ..inv_equipos.crud import get_inv_equipo


def get_inv_componentes(
    db: Session,
    inv_categoria_id: int = None,
    inv_equipo_id: int = None,
    generacion: str = False,
) -> Any:
    """Consultar los componentes activos"""
    consulta = db.query(InvComponente)
    if inv_categoria_id:
        inv_categoria = get_inv_categoria(db, inv_categoria_id=inv_categoria_id)
        consulta = consulta.filter(InvComponente.inv_categoria == inv_categoria)
    if inv_equipo_id:
        inv_equipo = get_inv_equipo(db, inv_equipo_id=inv_equipo_id)
        consulta = consulta.filter(InvComponente.inv_equipo == inv_equipo)
    generacion = safe_string(generacion)
    if generacion:
        consulta = consulta.filter_by(generacion=generacion)
    return consulta.filter_by(estatus="A").order_by(InvComponente.id.desc())


def get_inv_componente(db: Session, inv_componente_id: int) -> InvComponente:
    """Consultar un componente por su id"""
    inv_componente = db.query(InvComponente).get(inv_componente_id)
    if inv_componente is None:
        raise IndexError("No existe ese componente")
    if inv_componente.estatus != "A":
        raise ValueError("No es activo ese componente, está eliminado")
    return inv_componente
