"""
Autoridades v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from plataforma_web.v1.roles.models import Permiso
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInBD

from .crud import get_autoridades, get_autoridad, get_autoridad_from_clave
from .schemas import AutoridadOut

router = APIRouter()


@router.get("", response_model=LimitOffsetPage[AutoridadOut])
async def list_paginate(
    distrito_id: int = None,
    materia_id: int = None,
    organo_jurisdiccional: str = None,
    con_notarias: bool = False,
    para_glosas: bool = False,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado paginado de autoridades"""
    if not current_user.permissions & Permiso.VER_CATALOGOS == Permiso.VER_CATALOGOS:
        raise HTTPException(status_code=403, detail="Forbidden")
    return paginate(
        get_autoridades(
            db,
            distrito_id=distrito_id,
            materia_id=materia_id,
            organo_jurisdiccional=organo_jurisdiccional,
            con_notarias=con_notarias,
            para_glosas=para_glosas,
        )
    )


@router.get("/clave/{clave}", response_model=AutoridadOut)
async def detail_from_clave(
    clave: str,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una autoridad a partir de su clave"""
    if not current_user.permissions & Permiso.VER_CATALOGOS == Permiso.VER_CATALOGOS:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        autoridad = get_autoridad_from_clave(db, clave=clave)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return AutoridadOut(
        id=autoridad.id,
        clave=autoridad.clave,
        distrito_id=autoridad.distrito_id,
        distrito_nombre=autoridad.distrito_nombre,
        distrito_nombre_corto=autoridad.distrito_nombre_corto,
        materia_id=autoridad.materia_id,
        materia_nombre=autoridad.materia_nombre,
        descripcion=autoridad.descripcion,
        descripcion_corta=autoridad.descripcion_corta,
        es_jurisdiccional=autoridad.es_jurisdiccional,
        es_notaria=autoridad.es_notaria,
        organo_jurisdiccional=autoridad.organo_jurisdiccional,
        audiencia_categoria=autoridad.audiencia_categoria,
    )


@router.get("/id/{autoridad_id}", response_model=AutoridadOut)
async def detail(
    autoridad_id: int,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una autoridad a partir de su id"""
    if not current_user.permissions & Permiso.VER_CATALOGOS == Permiso.VER_CATALOGOS:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        autoridad = get_autoridad(db, autoridad_id=autoridad_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    return AutoridadOut(
        id=autoridad.id,
        clave=autoridad.clave,
        distrito_id=autoridad.distrito_id,
        distrito_nombre=autoridad.distrito_nombre,
        distrito_nombre_corto=autoridad.distrito_nombre_corto,
        materia_id=autoridad.materia_id,
        materia_nombre=autoridad.materia_nombre,
        descripcion=autoridad.descripcion,
        descripcion_corta=autoridad.descripcion_corta,
        es_jurisdiccional=autoridad.es_jurisdiccional,
        es_notaria=autoridad.es_notaria,
        organo_jurisdiccional=autoridad.organo_jurisdiccional,
        audiencia_categoria=autoridad.audiencia_categoria,
    )
