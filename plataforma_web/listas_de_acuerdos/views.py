"""
Listas de Acuerdos, vistas
"""
from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from lib.database import get_db

from plataforma_web.autoridades.crud import get_autoridad
from plataforma_web.listas_de_acuerdos import crud, schemas
from plataforma_web.roles.models import Permiso
from plataforma_web.usuarios.authentications import get_current_active_user
from plataforma_web.usuarios.schemas import UsuarioEnBD


router = APIRouter()


@router.get("", response_model=List[schemas.ListaDeAcuerdo])
async def listar_listas_de_acuerdos(autoridad_id: int, fecha: date = None, ano: int = None, current_user: UsuarioEnBD = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Lista de Listas de Acuerdos"""
    if not current_user.permissions & Permiso.VER_JUSTICIABLES == Permiso.VER_JUSTICIABLES:
        raise HTTPException(status_code=403, detail="Forbidden (no tiene permiso).")
    autoridad = get_autoridad(db, autoridad_id=autoridad_id)
    if autoridad is None:
        raise HTTPException(status_code=404, detail="Not found (no existe la autoridad).")
    resultados = []
    for lista_de_acuerdo, autoridad, distrito in crud.get_listas_de_acuerdos(db, autoridad_id=autoridad_id, fecha=fecha, ano=ano):
        resultados.append(
            schemas.ListaDeAcuerdo(
                id=lista_de_acuerdo.id,
                distrito_id=distrito.id,
                distrito=distrito.nombre,
                autoridad_id=autoridad.id,
                autoridad=autoridad.descripcion,
                fecha=lista_de_acuerdo.fecha,
                descripcion=lista_de_acuerdo.descripcion,
                archivo=lista_de_acuerdo.archivo,
                url=lista_de_acuerdo.url,
            )
        )
    return resultados


@router.get("/{lista_de_acuerdo_id}", response_model=schemas.ListaDeAcuerdo)
async def consultar_una_lista_de_acuerdos(lista_de_acuerdo_id: int, current_user: UsuarioEnBD = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Consultar una Lista de Acuerdos"""
    if not current_user.permissions & Permiso.VER_JUSTICIABLES == Permiso.VER_JUSTICIABLES:
        raise HTTPException(status_code=403, detail="Forbidden (no tiene permiso).")
    lista_de_acuerdo = crud.get_lista_de_acuerdo(db, lista_de_acuerdo_id=lista_de_acuerdo_id)
    if lista_de_acuerdo is None:
        raise HTTPException(status_code=404, detail="Not found (no existe la lista de acuerdos).")
    return schemas.ListaDeAcuerdo(
        id=lista_de_acuerdo.id,
        distrito_id=lista_de_acuerdo.autoridad.distrito_id,
        distrito=lista_de_acuerdo.autoridad.distrito.nombre,
        autoridad_id=lista_de_acuerdo.autoridad_id,
        autoridad=lista_de_acuerdo.autoridad.descripcion,
        fecha=lista_de_acuerdo.fecha,
        descripcion=lista_de_acuerdo.descripcion,
        archivo=lista_de_acuerdo.archivo,
        url=lista_de_acuerdo.url,
    )


@router.post("", response_model=schemas.ListaDeAcuerdo)
async def insertar_lista_de_acuerdos(lista_de_acuerdo: schemas.ListaDeAcuerdoNew, current_user: UsuarioEnBD = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Insertar una Lista de Acuerdos"""
    if not current_user.permissions & Permiso.CREAR_JUSTICIABLES == Permiso.CREAR_JUSTICIABLES:
        raise HTTPException(status_code=403, detail="Forbidden (no tiene permiso).")
    try:
        resultado = crud.insert_lista_de_acuerdo(db, lista_de_acuerdo)
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not Acceptable ({str(error)})") from error
    if resultado is not None:
        return schemas.ListaDeAcuerdo(
            id=resultado.id,
            distrito_id=resultado.autoridad.distrito_id,
            distrito=resultado.autoridad.distrito.nombre,
            autoridad_id=resultado.autoridad_id,
            autoridad=resultado.autoridad.descripcion,
            fecha=resultado.fecha,
            descripcion=resultado.descripcion,
            archivo=resultado.archivo,
            url=resultado.url,
        )
