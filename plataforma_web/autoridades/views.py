"""
Autoriades, vistas
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from lib.database import get_db

from fastapi_pagination import LimitOffsetPage, Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate

from plataforma_web.autoridades import crud, schemas
from plataforma_web.roles.models import Permiso
from plataforma_web.usuarios.authentications import get_current_active_user
from plataforma_web.usuarios.schemas import UsuarioEnBD


router = APIRouter()


@router.get("", response_model=Page[schemas.Autoridad])
async def listar_autoridades(
    distrito_id: int = None,
    materia_id: int = None,
    organo_jurisdiccional: str = None,
    con_notarias: bool = False,
    para_glosas: bool = False,
    current_user: UsuarioEnBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Lista de Autoridades"""
    if not current_user.permissions & Permiso.VER_CATALOGOS == Permiso.VER_CATALOGOS:
        raise HTTPException(status_code=403, detail="Forbidden (no tiene permiso).")
    resultados = []
    for autoridad, distrito, materia in crud.get_autoridades(db, distrito_id=distrito_id, materia_id=materia_id, organo_jurisdiccional=organo_jurisdiccional, con_notarias=con_notarias, para_glosas=para_glosas):
        resultados.append(
            schemas.Autoridad(
                id=autoridad.id,
                distrito_id=autoridad.distrito_id,
                distrito=distrito.nombre,
                materia_id=autoridad.materia_id,
                materia=materia.nombre,
                autoridad=autoridad.descripcion,
                autoridad_corta=autoridad.descripcion_corta,
                clave=autoridad.clave,
                organo_jurisdiccional=autoridad.organo_jurisdiccional,
                audiencia_categoria=autoridad.audiencia_categoria,
            )
        )
    return paginate(resultados)


@router.get("/{autoridad_id}", response_model=schemas.Autoridad)
async def consultar_una_autoridad(autoridad_id: int, current_user: UsuarioEnBD = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Consultar una Autoridad"""
    if not current_user.permissions & Permiso.VER_CATALOGOS == Permiso.VER_CATALOGOS:
        raise HTTPException(status_code=403, detail="Forbidden (no tiene permiso).")
    autoridad = crud.get_autoridad(db, autoridad_id=autoridad_id)
    if autoridad is None:
        raise HTTPException(status_code=404, detail="Not Found (no existe la autoridad).")
    return schemas.Autoridad(
        id=autoridad.id,
        distrito_id=autoridad.distrito_id,
        distrito=autoridad.distrito.nombre,
        materia_id=autoridad.materia_id,
        materia=autoridad.materia.nombre,
        autoridad=autoridad.descripcion,
        autoridad_corta=autoridad.descripcion_corta,
        clave=autoridad.clave,
        organo_jurisdiccional=autoridad.organo_jurisdiccional,
        audiencia_categoria=autoridad.audiencia_categoria,
    )


@router.get("/clave/{clave}", response_model=schemas.Autoridad)
async def consultar_una_autoridad_con_clave(clave: str, current_user: UsuarioEnBD = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Consultar una Autoridad con su clave"""
    if not current_user.permissions & Permiso.VER_CATALOGOS == Permiso.VER_CATALOGOS:
        raise HTTPException(status_code=403, detail="Forbidden (no tiene permiso).")
    try:
        autoridad = crud.get_autoridad_from_clave(db, clave=clave)
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not Acceptable ({str(error)})") from error
    if autoridad is None:
        raise HTTPException(status_code=404, detail="Not Found (no existe la autoridad).")
    return schemas.Autoridad(
        id=autoridad.id,
        distrito_id=autoridad.distrito_id,
        distrito=autoridad.distrito.nombre,
        materia_id=autoridad.materia_id,
        materia=autoridad.materia.nombre,
        autoridad=autoridad.descripcion,
        autoridad_corta=autoridad.descripcion_corta,
        clave=autoridad.clave,
        organo_jurisdiccional=autoridad.organo_jurisdiccional,
        audiencia_categoria=autoridad.audiencia_categoria,
    )
