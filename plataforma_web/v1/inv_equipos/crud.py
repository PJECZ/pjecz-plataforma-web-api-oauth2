"""
Inventarios Equipos v1, CRUD (create, read, update, and delete)
"""
from datetime import date
from typing import Any
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

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


def get_matriz(db: Session) -> Any:
    """Matriz con oficinas, usuarios, custodias, equipos, tipos, modelos y marcas"""
    return (
        db.query(
            Oficina.clave.label("oficina_clave"),
            Usuario.email.label("usuario_email"),
            InvCustodia.id.label("inv_custodia_id"),
            InvCustodia.nombre_completo.label("inv_custodia_nombre_completo"),
            InvEquipo.id.label("inv_equipo_id"),
            InvEquipo.tipo.label("inv_equipo_tipo"),
            InvMarca.nombre.label("inv_marca_nombre"),
            InvModelo.descripcion.label("inv_modelo_descripcion"),
            InvEquipo.descripcion.label("inv_equipo_descripcion"),
            InvEquipo.fecha_fabricacion.label("inv_equipo_fecha_fabricacion"),
        )
        .select_from(Oficina)
        .join(Usuario, InvCustodia, InvEquipo, InvModelo, InvMarca)
        .filter(Oficina.estatus == "A")
        .filter(Usuario.estatus == "A")
        .filter(InvCustodia.estatus == "A")
        .filter(InvEquipo.estatus == "A")
        .order_by(InvCustodia.id, InvEquipo.id)
    )


def get_cantidades_oficina_tipo(db: Session) -> Any:
    """Obtener las cantidades de equipos por oficina y por tipo"""
    return (
        db.query(
            Oficina.clave.label("oficina_clave"),
            InvEquipo.tipo.label("inv_equipo_tipo"),
            func.count("*").label("cantidad"),
        )
        .select_from(Oficina)
        .join(Usuario, InvCustodia, InvEquipo)
        .filter(Oficina.estatus == "A")
        .filter(Usuario.estatus == "A")
        .filter(InvCustodia.estatus == "A")
        .filter(InvEquipo.estatus == "A")
        .order_by(InvEquipo.tipo)
        .group_by(Oficina.clave, InvEquipo.tipo)
    )
