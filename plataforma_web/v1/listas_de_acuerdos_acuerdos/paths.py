"""
Listas de Acuerdos, Acuerdos v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from plataforma_web.v1.roles.models import Permiso
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInBD

from .crud import get_acuerdos, get_acuerdo
from .schemas import ListaDeAcuerdoAcuerdoOut

router = APIRouter()


@router.get("", response_model=LimitOffsetPage[ListaDeAcuerdoAcuerdoOut])
async def list_paginate(
    lista_de_acuerdo_id: int,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado paginado de acuerdos"""
    if not current_user.permissions & Permiso.VER_JUSTICIABLES == Permiso.VER_JUSTICIABLES:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        consulta = get_acuerdos(db, lista_de_acuerdo_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return paginate(consulta)


@router.get("/id/{lista_de_acuerdo_acuerdo_id}", response_model=ListaDeAcuerdoAcuerdoOut)
async def detail(
    lista_de_acuerdo_acuerdo_id: int,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una acuerdo a partir de su id"""
    if not current_user.permissions & Permiso.VER_JUSTICIABLES == Permiso.VER_JUSTICIABLES:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        acuerdo = get_acuerdo(db, lista_de_acuerdo_acuerdo_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    return ListaDeAcuerdoAcuerdoOut(
        id=acuerdo.id,
        lista_de_acuerdo_id=acuerdo.lista_de_acuerdo_id,
        folio=acuerdo.folio,
        expediente=acuerdo.expediente,
        actor=acuerdo.actor,
        demandado=acuerdo.demandado,
        tipo_acuerdo=acuerdo.tipo_acuerdo,
        tipo_juicio=acuerdo.tipo_juicio,
        referencia=acuerdo.referencia,
        fecha=acuerdo.fecha,
    )
