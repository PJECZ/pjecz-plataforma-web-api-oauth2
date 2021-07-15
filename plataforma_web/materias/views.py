"""
Materias, vistas
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from lib.database import get_db

from plataforma_web.materias import crud, schemas
from plataforma_web.roles.models import Permiso
from plataforma_web.usuarios.authentications import get_current_active_user
from plataforma_web.usuarios.schemas import UsuarioEnBD


router = APIRouter()


@router.get("", response_model=List[schemas.Materia])
async def listar_materias(current_user: UsuarioEnBD = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Lista de materias"""
    if not current_user.permissions & Permiso.VER_CATALOGOS == Permiso.VER_CATALOGOS:
        raise HTTPException(status_code=403, detail="Forbidden (no tiene permiso).")
    return [schemas.Materia(id=materia.id, materia=materia.nombre) for materia in crud.get_materias(db)]


@router.get("/{materia_id}", response_model=schemas.Materia)
async def consultar_un_materia(materia_id: int, current_user: UsuarioEnBD = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Consultar un materia"""
    if not current_user.permissions & Permiso.VER_CATALOGOS == Permiso.VER_CATALOGOS:
        raise HTTPException(status_code=403, detail="Forbidden (no tiene permiso).")
    materia = crud.get_materia(db, materia_id=materia_id)
    if materia is None:
        raise HTTPException(status_code=404, detail="Not found (no existe la materia).")
    return schemas.Materia(id=materia.id, materia=materia.nombre)
