"""
Inventarios Componentes v1, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import PWIsDeletedError, PWNotExistsError
from lib.safe_string import safe_string

from ...core.inv_componentes.models import InvComponente
from ..inv_categorias.crud import get_inv_categoria
from ..inv_equipos.crud import get_inv_equipo


def get_inv_componentes(
    db: Session,
    estatus: str = None,
    inv_categoria_id: int = None,
    inv_equipo_id: int = None,
    generacion: str = None,
) -> Any:
    """Consultar los componentes"""

    # Consultar
    consulta = db.query(InvComponente)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Filtrar por categoría
    if inv_categoria_id is not None:
        inv_categoria = get_inv_categoria(db, inv_categoria_id=inv_categoria_id)
        consulta = consulta.filter(InvComponente.inv_categoria == inv_categoria)

    # Filtrar por equipo
    if inv_equipo_id is not None:
        inv_equipo = get_inv_equipo(db, inv_equipo_id=inv_equipo_id)
        consulta = consulta.filter(InvComponente.inv_equipo == inv_equipo)

    # Filtrar por generación
    if generacion is not None:
        generacion = safe_string(generacion)
        if generacion != "":
            consulta = consulta.filter_by(generacion=generacion)

    # Entregar
    return consulta.order_by(InvComponente.id.desc())


def get_inv_componente(db: Session, inv_componente_id: int) -> InvComponente:
    """Consultar un componente por su id"""
    inv_componente = db.query(InvComponente).get(inv_componente_id)
    if inv_componente is None:
        raise PWNotExistsError("No existe ese componente")
    if inv_componente.estatus != "A":
        raise PWIsDeletedError("No es activo ese componente, está eliminado")
    return inv_componente
