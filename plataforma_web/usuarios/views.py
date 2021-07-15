"""
Usuarios, vistas
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from lib.database import get_db

from plataforma_web.roles.models import Permiso
from plataforma_web.usuarios import crud, schemas
from plataforma_web.usuarios.authentications import get_current_active_user


router = APIRouter()


@router.get("", response_model=List[schemas.Usuario])
async def listar_usuarios(current_user: schemas.UsuarioEnBD = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Lista de usuarios"""
    if not current_user.permissions & Permiso.VER_CUENTAS == Permiso.VER_CUENTAS:
        raise HTTPException(status_code=403, detail="Forbidden (no tiene permiso).")
    resultados = []
    for usuario, autoridad, distrito, rol in crud.get_usuarios(db):
        resultados.append(
            schemas.Usuario(
                id=usuario.id,
                distrito_id=distrito.id,
                distrito=autoridad.descripcion,
                autoridad_id=autoridad.id,
                autoridad=autoridad.descripcion,
                rol_id=rol.id,
                rol=rol.nombre,
                email=usuario.email,
                nombres=usuario.nombres,
                apellido_paterno=usuario.apellido_paterno,
                apellido_materno=usuario.apellido_materno,
            )
        )
    return resultados


@router.get("/{usuario_id}", response_model=schemas.Usuario)
async def consultar_un_usuario(usuario_id: int, current_user: schemas.UsuarioEnBD = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Consultar un usuario"""
    if not current_user.permissions & Permiso.VER_CUENTAS == Permiso.VER_CUENTAS:
        raise HTTPException(status_code=403, detail="Forbidden (no tiene permiso).")
    usuario = crud.get_usuario(db, usuario_id=usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Not found (no existe el usuario).")
    return schemas.Usuario(
        id=usuario.id,
        distrito_id=usuario.autoridad.distrito_id,
        distrito=usuario.autoridad.distrito.nombre,
        autoridad_id=usuario.autoridad_id,
        autoridad=usuario.autoridad.descripcion,
        rol_id=usuario.rol_id,
        rol=usuario.rol.nombre,
        email=usuario.email,
        nombres=usuario.nombres,
        apellido_paterno=usuario.apellido_paterno,
        apellido_materno=usuario.apellido_materno,
    )
