"""
Listas de Acuerdos, Acuerdos v1, CRUD (create, read, update, and delete)
"""
from plataforma_web.v1.listas_de_acuerdos.models import ListaDeAcuerdo
from typing import Any
from sqlalchemy.orm import Session

from .models import ListaDeAcuerdoAcuerdo
from ..listas_de_acuerdos.crud import get_lista_de_acuerdo


def get_acuerdos(
    db: Session,
    lista_de_acuerdo_id: int = None,
) -> Any:
    """ Consultar los acuerdos activos """
    consulta = db.query(ListaDeAcuerdoAcuerdo)
    if lista_de_acuerdo_id:
        lista_de_acuerdo = get_lista_de_acuerdo(db, lista_de_acuerdo_id)  # Si no se encuentra provoca una excepción
        consulta = consulta.filter(ListaDeAcuerdoAcuerdo.lista_de_acuerdo == lista_de_acuerdo)
    return consulta.filter_by(estatus="A").order_by(ListaDeAcuerdoAcuerdo.ninguno)


def get_acuerdo(db: Session, lista_de_acuerdo_acuerdo_id: int) -> ListaDeAcuerdoAcuerdo:
    """ Consultar un acuerdo por su id """
    lista_de_acuerdo_acuerdo = db.query(ListaDeAcuerdoAcuerdo).get(lista_de_acuerdo_acuerdo_id)
    if lista_de_acuerdo_acuerdo is None:
        raise IndexError
    return lista_de_acuerdo_acuerdo
