"""
Roles, vistas
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from lib.database import get_db

from plataforma_web.roles.models import Permiso
from plataforma_web.roles import crud, schemas
from plataforma_web.usuarios.authentications import get_current_active_user
from plataforma_web.usuarios.schemas import UsuarioEnBD


router = APIRouter()


@router.get("", response_model=List[schemas.Rol])
async def listar_roles(current_user: UsuarioEnBD = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Lista de roles"""
    if not current_user.permissions & Permiso.VER_CUENTAS == Permiso.VER_CUENTAS:
        raise HTTPException(status_code=403, detail="Forbidden (no tiene permiso).")
    return [schemas.Rol(id=rol.id, rol=rol.nombre) for rol in crud.get_roles(db)]


@router.get("/{rol_id}", response_model=schemas.Rol)
async def consultar_un_rol(rol_id: int, current_user: UsuarioEnBD = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Consultar un rol"""
    if not current_user.permissions & Permiso.VER_CUENTAS == Permiso.VER_CUENTAS:
        raise HTTPException(status_code=403, detail="Forbidden (no tiene permiso).")
    rol = crud.get_rol(db, rol_id=rol_id)
    if rol is None:
        raise HTTPException(status_code=404, detail="Not found (no existe el rol).")
    return schemas.Rol(id=rol.id, rol=rol.nombre)
