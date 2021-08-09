"""
Listas de Acuerdos v1, rutas (paths)
"""
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from plataforma_web.v1.roles.models import Permiso
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInBD

from .crud import get_listas_de_acuerdos, get_lista_de_acuerdo, insert_lista_de_acuerdo
from .schemas import ListaDeAcuerdoIn, ListaDeAcuerdoOut

router = APIRouter()


@router.get("", response_model=LimitOffsetPage[ListaDeAcuerdoOut])
async def list_paginate(
    autoridad_id: int = None,
    autoridad_clave: str = None,
    fecha: date = None,
    anio: int = None,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado paginado de listas de acuerdos"""
    if not current_user.permissions & Permiso.VER_JUSTICIABLES == Permiso.VER_JUSTICIABLES:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        consulta = get_listas_de_acuerdos(
            db,
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            fecha=fecha,
            anio=anio,
        )
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return paginate(consulta)


@router.get("/id/{lista_de_acuerdo_id}", response_model=ListaDeAcuerdoOut)
async def detail(
    lista_de_acuerdo_id: int,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una lista de acuerdos a partir de su id"""
    if not current_user.permissions & Permiso.VER_JUSTICIABLES == Permiso.VER_JUSTICIABLES:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        consulta = get_lista_de_acuerdo(db, lista_de_acuerdo_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    return ListaDeAcuerdoOut(
        id=consulta.id,
        distrito_id=consulta.distrito_id,
        distrito_nombre=consulta.distrito_nombre,
        distrito_nombre_corto=consulta.distrito_nombre_corto,
        autoridad_id=consulta.autoridad_id,
        autoridad_descripcion=consulta.autoridad_descripcion,
        autoridad_descripcion_corta=consulta.autoridad_descripcion_corta,
        fecha=consulta.fecha,
        descripcion=consulta.descripcion,
        archivo=consulta.archivo,
        url=consulta.url,
    )


@router.post("", response_model=ListaDeAcuerdoOut)
async def new(
    lista_de_acuerdo: ListaDeAcuerdoIn,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Insertar una lista de acuerdos"""
    if not current_user.permissions & Permiso.CREAR_JUSTICIABLES == Permiso.CREAR_JUSTICIABLES:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        resultado = insert_lista_de_acuerdo(db, lista_de_acuerdo)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return ListaDeAcuerdoOut(
        id=resultado.id,
        distrito_id=resultado.distrito_id,
        distrito_nombre=resultado.distrito_nombre,
        distrito_nombre_corto=resultado.distrito_nombre_corto,
        autoridad_id=resultado.autoridad_id,
        autoridad_descripcion=resultado.autoridad_descripcion,
        autoridad_descripcion_corta=resultado.autoridad_descripcion_corta,
        fecha=resultado.fecha,
        descripcion=resultado.descripcion,
        archivo=resultado.archivo,
        url=resultado.url,
    )
