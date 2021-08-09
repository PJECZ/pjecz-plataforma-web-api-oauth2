"""
Listas de Acuerdos, Acuerdos v1, CRUD (create, read, update, and delete)
"""
from plataforma_web.v1.listas_de_acuerdos.models import ListaDeAcuerdo
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import AlredyExistsError
from lib.safe_string import safe_string
from .models import ListaDeAcuerdoAcuerdo
from .schemas import ListaDeAcuerdoAcuerdoIn
from ..listas_de_acuerdos.crud import get_lista_de_acuerdo


def get_acuerdos(
    db: Session,
    lista_de_acuerdo_id: int = None,
) -> Any:
    """Consultar los acuerdos activos"""
    consulta = db.query(ListaDeAcuerdoAcuerdo)
    if lista_de_acuerdo_id:
        lista_de_acuerdo = get_lista_de_acuerdo(db, lista_de_acuerdo_id)  # Si no se encuentra provoca una excepción
        consulta = consulta.filter(ListaDeAcuerdoAcuerdo.lista_de_acuerdo == lista_de_acuerdo)
    return consulta.filter_by(estatus="A").order_by(ListaDeAcuerdoAcuerdo.folio)


def get_acuerdo(db: Session, lista_de_acuerdo_acuerdo_id: int) -> ListaDeAcuerdoAcuerdo:
    """Consultar un acuerdo por su id"""
    lista_de_acuerdo_acuerdo = db.query(ListaDeAcuerdoAcuerdo).get(lista_de_acuerdo_acuerdo_id)
    if lista_de_acuerdo_acuerdo is None:
        raise IndexError
    return lista_de_acuerdo_acuerdo


def insert_acuerdo(db: Session, acuerdo: ListaDeAcuerdoAcuerdoIn) -> ListaDeAcuerdoAcuerdo:
    """Insertar un acuerdo"""
    # Validar lista de acuerdos
    lista_de_acuerdo = get_lista_de_acuerdo(db, acuerdo.lista_de_acuerdo_id)  # Si no se encuentra provoca una excepción
    if lista_de_acuerdo.estatus != "A":
        raise ValueError("No es activa la lista de acuerdos, fue eliminada")
    # Evitar la duplicidad, en la misma autoridad no deben repetirse las referencias
    existe_ese_acuerdo = db.query(ListaDeAcuerdoAcuerdo).filter(ListaDeAcuerdoAcuerdo.lista_de_acuerdo.autoridad == lista_de_acuerdo.autoridad).filter_by(referencia=acuerdo.referencia).first()
    if existe_ese_acuerdo:
        raise AlredyExistsError("No se permite insertar el acuerdo porque la autoridad ya tiene uno con esa referencia")
    # Insertar
    resultado = ListaDeAcuerdoAcuerdo(
        lista_de_acuerdo=lista_de_acuerdo,
        folio=acuerdo.folio,
        expediente=acuerdo.expediente,
        actor=safe_string(acuerdo.actor),
        demandado=safe_string(acuerdo.demandado),
        tipo_acuerdo=safe_string(acuerdo.tipo_acuerdo),
        tipo_juicio=safe_string(acuerdo.tipo_juicio),
        referencia=acuerdo.referencia,
    )
    db.add(resultado)
    db.commit()
    return resultado
