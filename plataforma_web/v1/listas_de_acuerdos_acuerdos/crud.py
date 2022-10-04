"""
Listas de Acuerdos, Acuerdos v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import PWAlreadyExistsError, PWIsDeletedError, PWNotExistsError
from lib.safe_string import safe_string

from plataforma_web.v1.listas_de_acuerdos.crud import get_lista_de_acuerdo
from plataforma_web.v1.listas_de_acuerdos.models import ListaDeAcuerdo
from plataforma_web.v1.listas_de_acuerdos_acuerdos.models import ListaDeAcuerdoAcuerdo
from plataforma_web.v1.listas_de_acuerdos_acuerdos.schemas import ListaDeAcuerdoAcuerdoIn


def get_acuerdos(
    db: Session,
    lista_de_acuerdo_id: int,
    estatus: str = None,
) -> Any:
    """Consultar los acuerdos activos"""

    # Consultar
    consulta = db.query(ListaDeAcuerdoAcuerdo)

    # Filtrar por lista de acuerdos
    lista_de_acuerdo = get_lista_de_acuerdo(db, lista_de_acuerdo_id)
    consulta = consulta.filter(ListaDeAcuerdoAcuerdo.lista_de_acuerdo == lista_de_acuerdo)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Entregar
    return consulta.order_by(ListaDeAcuerdoAcuerdo.id.desc())


def get_acuerdo(db: Session, lista_de_acuerdo_acuerdo_id: int) -> ListaDeAcuerdoAcuerdo:
    """Consultar un acuerdo por su id"""
    lista_de_acuerdo_acuerdo = db.query(ListaDeAcuerdoAcuerdo).get(lista_de_acuerdo_acuerdo_id)
    if lista_de_acuerdo_acuerdo is None:
        raise PWNotExistsError("No existe ese acuerdo")
    if lista_de_acuerdo_acuerdo.estatus != "A":
        raise PWIsDeletedError("No es activo el acuerdo, está eliminado")
    return lista_de_acuerdo_acuerdo


def insert_acuerdo(db: Session, acuerdo: ListaDeAcuerdoAcuerdoIn) -> ListaDeAcuerdoAcuerdo:
    """Insertar un acuerdo"""

    # Validar lista de acuerdos
    lista_de_acuerdo = get_lista_de_acuerdo(db, acuerdo.lista_de_acuerdo_id)

    # Evitar la duplicidad, en la misma autoridad no deben repetirse las referencias
    existe_acuerdos = db.query(ListaDeAcuerdoAcuerdo, ListaDeAcuerdo).join(ListaDeAcuerdo).filter(ListaDeAcuerdo.autoridad_id == lista_de_acuerdo.autoridad_id).filter(ListaDeAcuerdoAcuerdo.referencia == acuerdo.referencia).filter_by(estatus="A").first()
    if existe_acuerdos is not None:
        raise PWAlreadyExistsError("No se permite insertar el acuerdo porque la autoridad ya tiene uno con esa referencia")

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

    # Entregar
    return resultado
