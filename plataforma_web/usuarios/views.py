"""
Usuarios, vistas
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from plataforma_web.usuarios import crud, schemas
from lib.database import get_db

router = APIRouter()


@router.get("", response_model=List[schemas.Usuario])
async def listar_usuarios(db: Session = Depends(get_db)):
    """Lista de usuarios"""
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
async def consultar_un_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Consultar un usuario"""
    usuario = crud.get_usuario(db, usuario_id=usuario_id)
    if usuario is None:
        raise HTTPException(status_code=400, detail="No existe el usuario.")
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
