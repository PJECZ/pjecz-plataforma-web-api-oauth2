"""
Listas de Acuerdos, Acuerdos v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import AlredyExistsError
from lib.fastapi_pagination import LimitOffsetPage

from plataforma_web.v1.listas_de_acuerdos_acuerdos.crud import get_acuerdos, get_acuerdo, insert_acuerdo
from plataforma_web.v1.listas_de_acuerdos_acuerdos.schemas import ListaDeAcuerdoAcuerdoIn, ListaDeAcuerdoAcuerdoOut
from plataforma_web.v1.permisos.models import Permiso
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInDB

listas_de_acuerdos_acuerdos = APIRouter(prefix="/v1/listas_de_acuerdos", tags=["listas de acuerdos"])


@listas_de_acuerdos_acuerdos.get("/{lista_de_acuerdo_id}/acuerdos", response_model=LimitOffsetPage[ListaDeAcuerdoAcuerdoOut])
async def listado_acuerdos(
    lista_de_acuerdo_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de Acuerdos de una Lista de Acuerdos"""
    if "LISTAS DE ACUERDOS ACUERDOS" not in current_user.permissions or current_user.permissions["LISTAS DE ACUERDOS ACUERDOS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_acuerdos(db, lista_de_acuerdo_id=lista_de_acuerdo_id)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@listas_de_acuerdos_acuerdos.post("/{lista_de_acuerdo_id}/acuerdos", response_model=ListaDeAcuerdoAcuerdoOut)
async def nuevo_acuerdo(
    acuerdo: ListaDeAcuerdoAcuerdoIn,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Insertar un acuerdo"""
    if "LISTAS DE ACUERDOS ACUERDOS" not in current_user.permissions or current_user.permissions["LISTAS DE ACUERDOS ACUERDOS"] < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = insert_acuerdo(db, acuerdo)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    except AlredyExistsError as error:
        raise HTTPException(status_code=409, detail=f"Conflict: {str(error)}") from error
    return ListaDeAcuerdoAcuerdoOut.from_orm(listado)


@listas_de_acuerdos_acuerdos.get("/{lista_de_acuerdo_id}/acuerdos/{lista_de_acuerdo_acuerdo_id}", response_model=ListaDeAcuerdoAcuerdoOut)
async def detalle_acuerdo(
    lista_de_acuerdo_acuerdo_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una acuerdo a partir de su id"""
    if "LISTAS DE ACUERDOS ACUERDOS" not in current_user.permissions or current_user.permissions["LISTAS DE ACUERDOS ACUERDOS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        acuerdo = get_acuerdo(db, lista_de_acuerdo_acuerdo_id=lista_de_acuerdo_acuerdo_id)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    return ListaDeAcuerdoAcuerdoOut.from_orm(acuerdo)
