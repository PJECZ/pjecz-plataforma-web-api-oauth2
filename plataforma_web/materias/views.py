"""
Materias, vistas
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from lib.database import get_db

from plataforma_web.materias import crud, schemas
from plataforma_web.usuarios.authentications import oauth2_scheme

router = APIRouter()


@router.get("", response_model=List[schemas.Materia])
async def listar_materias(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Lista de materias"""
    return [schemas.Materia(id=materia.id, materia=materia.nombre) for materia in crud.get_materias(db)]


@router.get("/{materia_id}", response_model=schemas.Materia)
async def consultar_un_materia(materia_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Consultar un materia"""
    materia = crud.get_materia(db, materia_id=materia_id)
    if materia is None:
        raise HTTPException(status_code=400, detail="No existe el materia.")
    return schemas.Materia(id=materia.id, materia=materia.nombre)
