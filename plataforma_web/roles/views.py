"""
Roles, vistas
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from plataforma_web.roles import crud, schemas
from lib.database import get_db

router = APIRouter()


@router.get("", response_model=List[schemas.Rol])
async def listar_roles(db: Session = Depends(get_db)):
    """Lista de roles"""
    return [schemas.Rol(id=rol.id, rol=rol.nombre) for rol in crud.get_roles(db)]


@router.get("/{rol_id}", response_model=schemas.Rol)
async def consultar_un_rol(rol_id: int, db: Session = Depends(get_db)):
    """Consultar un rol"""
    rol = crud.get_rol(db, rol_id=rol_id)
    if rol is None:
        raise HTTPException(status_code=400, detail="No existe el rol.")
    return schemas.Rol(id=rol.id, rol=rol.nombre)
