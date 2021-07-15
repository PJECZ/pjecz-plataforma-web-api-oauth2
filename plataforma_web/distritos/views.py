"""
Distritos, vistas
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from lib.database import get_db

from plataforma_web.distritos import crud, schemas
from plataforma_web.roles.models import Permiso
from plataforma_web.usuarios.authentications import get_current_active_user
from plataforma_web.usuarios.schemas import UsuarioEnBD


router = APIRouter()


@router.get("", response_model=List[schemas.Distrito])
async def listar_distritos(solo_distritos: bool = False, current_user: UsuarioEnBD = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Lista de Distritos"""
    if not current_user.permissions & Permiso.VER_CATALOGOS == Permiso.VER_CATALOGOS:
        raise HTTPException(status_code=403, detail="Forbidden (no tiene permiso).")
    resultados = []
    for distrito in crud.get_distritos(db, solo_distritos=solo_distritos):
        resultados.append(
            schemas.Distrito(
                id=distrito.id,
                distrito=distrito.nombre,
                distrito_corto=distrito.nombre_corto,
            )
        )
    return resultados


@router.get("/{distrito_id}", response_model=schemas.Distrito)
async def consultar_un_distrito(distrito_id: int, current_user: UsuarioEnBD = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Consultar un Distrito"""
    if not current_user.permissions & Permiso.VER_CATALOGOS == Permiso.VER_CATALOGOS:
        raise HTTPException(status_code=403, detail="Forbidden (no tiene permiso).")
    distrito = crud.get_distrito(db, distrito_id=distrito_id)
    if distrito is None:
        raise HTTPException(status_code=404, detail="Not found (no existe el distrito).")
    return schemas.Distrito(
        id=distrito.id,
        distrito=distrito.nombre,
        distrito_corto=distrito.nombre_corto,
    )
