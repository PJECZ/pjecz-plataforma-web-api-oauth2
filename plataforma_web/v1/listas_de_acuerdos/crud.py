"""
Listas de Acuerdos v1, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime, timedelta
from typing import Any, List

from sqlalchemy.orm import Session
import pytz

from lib.exceptions import PWAlreadyExistsError, PWIsDeletedError, PWNotExistsError, PWNotValidParamError, PWOutOfRangeParamError
from lib.safe_string import safe_string

from .models import ListaDeAcuerdo
from .schemas import ListaDeAcuerdoIn, ListaDeAcuerdoOut
from ..autoridades.crud import get_autoridad, get_autoridades, get_autoridad_from_clave

LIMITE_DIAS = 7


def get_listas_de_acuerdos(
    db: Session,
    autoridad_id: int = None,
    autoridad_clave: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    estatus: str = None,
    fecha: date = None,
    fecha_desde: date = None,
    fecha_hasta: date = None,
) -> Any:
    """Consultar las listas de acuerdos activas"""

    # Huso horario
    servidor_huso_horario = pytz.utc

    # Consultar
    consulta = db.query(ListaDeAcuerdo)

    # Filtrar por autoridad
    if autoridad_id is not None:
        autoridad = get_autoridad(db, autoridad_id)
        consulta = consulta.filter(ListaDeAcuerdo.autoridad == autoridad)
    elif autoridad_clave is not None:
        autoridad = get_autoridad_from_clave(db, autoridad_clave)
        consulta = consulta.filter(ListaDeAcuerdo.autoridad == autoridad)

    # Filtrar por creado
    if creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(ListaDeAcuerdo.creado >= desde_dt).filter(ListaDeAcuerdo.creado <= hasta_dt)
    if creado is None and creado_desde is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        consulta = consulta.filter(ListaDeAcuerdo.creado >= desde_dt)
    if creado is None and creado_hasta is not None:
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(ListaDeAcuerdo.creado <= hasta_dt)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Filtrar por fecha
    if fecha is not None:
        consulta = consulta.filter_by(fecha=fecha)
    if fecha is None and fecha_desde is not None:
        consulta = consulta.filter(ListaDeAcuerdo.fecha >= fecha_desde)
    if fecha is None and fecha_hasta is not None:
        consulta = consulta.filter(ListaDeAcuerdo.fecha <= fecha_hasta)

    # Entregar
    return consulta.order_by(ListaDeAcuerdo.id.desc())


def get_lista_de_acuerdo(
    db: Session,
    lista_de_acuerdo_id: int,
) -> ListaDeAcuerdo:
    """Consultar una lista de acuerdo por su id"""
    lista_de_acuerdo = db.query(ListaDeAcuerdo).get(lista_de_acuerdo_id)
    if lista_de_acuerdo is None:
        raise PWNotExistsError("No exite esa lista de acuerdos")
    if lista_de_acuerdo.estatus != "A":
        raise PWIsDeletedError("No es activa la lista de acuerdos, fue eliminada")
    return lista_de_acuerdo


def insert_lista_de_acuerdo(
    db: Session,
    lista_de_acuerdo: ListaDeAcuerdoIn,
) -> ListaDeAcuerdo:
    """Insertar una lista de acuerdos"""

    # Validar autoridad
    autoridad = get_autoridad(db, lista_de_acuerdo.autoridad_id)
    if not autoridad.distrito.es_distrito_judicial:
        raise PWNotValidParamError("No está la autoridad en un distrito judicial")
    if not autoridad.es_jurisdiccional:
        raise PWNotValidParamError("No es jurisdiccional la autoridad")

    # Validar fecha
    hoy = date.today()
    hoy_dt = datetime(year=hoy.year, month=hoy.month, day=hoy.day)
    limite_dt = hoy_dt + timedelta(days=-LIMITE_DIAS)
    if lista_de_acuerdo.fecha is None:
        fecha = hoy
    else:
        fecha = lista_de_acuerdo.fecha
        if not limite_dt <= datetime(year=fecha.year, month=fecha.month, day=fecha.day) <= hoy_dt:
            raise PWOutOfRangeParamError("Fecha fuera de rango")

    # Si ya existe una lista de acuerdos con esa fecha, se aborta
    existe_esa_lista = db.query(ListaDeAcuerdo).filter_by(autoridad_id=autoridad.id).filter_by(fecha=fecha).filter_by(estatus="A").first()
    if existe_esa_lista:
        raise PWAlreadyExistsError("No se permite otra lista de acuerdos para la autoridad y fechas dadas")

    # Validar descripcion
    if lista_de_acuerdo.descripcion == "":
        descripcion = "LISTA DE ACUERDOS"
    else:
        descripcion = safe_string(lista_de_acuerdo.descripcion)

    # Insertar
    resultado = ListaDeAcuerdo(
        autoridad=autoridad,
        fecha=fecha,
        descripcion=descripcion,
    )
    db.add(resultado)
    db.commit()

    # Entregar
    return resultado


def get_listas_de_acuerdos_sintetizar_por_creado(
    db: Session,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    distrito_id: int = None,
    size: int = 100,
) -> List:
    """Consultar las listas de acuerdos por distrito"""

    # Consultar las autoridades del distrito
    autoridades = get_autoridades(
        db=db,
        distrito_id=distrito_id,
        es_jurisdiccional=True,
        es_notaria=False,
    ).all()

    # Consultar las listas de acuerdos de las autoridades
    listas_de_acuerdos = []
    for autoridad in autoridades:
        existentes = get_listas_de_acuerdos(
            db=db,
            autoridad_id=autoridad.id,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
        ).all()
        if existentes:
            # Si hay listas de acuerdos, se agregan a la lista
            for lista_de_acuerdo in existentes:
                listas_de_acuerdos.append(ListaDeAcuerdoOut.from_orm(lista_de_acuerdo))
        else:
            # Si NO hay listas de acuerdos, se agrega una renglon con ND
            listas_de_acuerdos.append(
                ListaDeAcuerdoOut(
                    id=0,
                    autoridad_id=autoridad.id,
                    autoridad_descripcion=autoridad.descripcion,
                    autoridad_descripcion_corta=autoridad.descripcion_corta,
                    autoridad_clave=autoridad.clave,
                    distrito_id=autoridad.distrito_id,
                    distrito_nombre=autoridad.distrito.nombre,
                    distrito_nombre_corto=autoridad.distrito.nombre_corto,
                    descripcion="ND",
                    fecha=creado,
                    archivo="",
                    url="",
                    creado=datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0),
                )
            )

    # Entregar lista
    return listas_de_acuerdos
