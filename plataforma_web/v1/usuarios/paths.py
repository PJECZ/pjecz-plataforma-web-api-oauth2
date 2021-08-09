"""
Usuarios v1.0, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from plataforma_web.v1.roles.models import Permiso
from .authentications import get_current_active_user
from .crud import get_usuarios, get_usuario
from .schemas import UsuarioOut, UsuarioInBD

router = APIRouter()


@router.get("", response_model=LimitOffsetPage[UsuarioOut])
async def list_paginate(
    autoridad_id: int = None,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado paginado de usuarios"""
    if not current_user.permissions & Permiso.VER_CUENTAS == Permiso.VER_CUENTAS:
        raise HTTPException(status_code=403, detail="Forbidden")
    return paginate(get_usuarios(db, autoridad_id=autoridad_id))


@router.get("/id/{usuario_id}", response_model=UsuarioOut)
async def detail(
    usuario_id: int,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de un usuario a partir de su id"""
    if not current_user.permissions & Permiso.VER_CUENTAS == Permiso.VER_CUENTAS:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        usuario = get_usuario(db, usuario_id=usuario_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    return UsuarioOut(
        id=usuario.id,
        rol_id=usuario.rol_id,
        rol_nombre=usuario.rol.nombre,
        distrito_id=usuario.autoridad.distrito_id,
        distrito_nombre=usuario.autoridad.distrito_nombre,
        distrito_nombre_corto=usuario.autoridad.distrito_nombre_corto,
        autoridad_id=usuario.autoridad_id,
        autoridad_descripcion=usuario.autoridad.descripcion,
        autoridad_descripcion_corta=usuario.autoridad.descripcion_corta,
        email=usuario.email,
        nombres=usuario.nombres,
        apellido_paterno=usuario.apellido_paterno,
        apellido_materno=usuario.apellido_materno,
    )
