"""
Listas de Acuerdos v1, rutas (paths)
"""
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import AlredyExistsError
from plataforma_web.v1.roles.models import Permiso
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInBD

from plataforma_web.v1.listas_de_acuerdos.crud import get_listas_de_acuerdos, get_lista_de_acuerdo, insert_lista_de_acuerdo
from plataforma_web.v1.listas_de_acuerdos.schemas import ListaDeAcuerdoIn, ListaDeAcuerdoOut

v1_listas_de_acuerdos = APIRouter(prefix="/v1/listas_de_acuerdos", tags=["listas de acuerdos"])


@v1_listas_de_acuerdos.get("", response_model=LimitOffsetPage[ListaDeAcuerdoOut])
async def listado_listas_de_acuerdos(
    autoridad_id: int = None,
    autoridad_clave: str = None,
    fecha: date = None,
    anio: int = None,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado paginado de listas de acuerdos"""
    if not current_user.permissions & Permiso.VER_JUSTICIABLES == Permiso.VER_JUSTICIABLES:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        listado = get_listas_de_acuerdos(
            db,
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            fecha=fecha,
            anio=anio,
        )
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@v1_listas_de_acuerdos.post("", response_model=ListaDeAcuerdoOut)
async def nueva_lista_de_acuerdos(
    lista_de_acuerdo: ListaDeAcuerdoIn,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Insertar una lista de acuerdos"""
    if not current_user.permissions & Permiso.CREAR_JUSTICIABLES == Permiso.CREAR_JUSTICIABLES:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        resultado = insert_lista_de_acuerdo(db, lista_de_acuerdo)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    except AlredyExistsError as error:
        raise HTTPException(status_code=409, detail=f"Conflict: {str(error)}") from error
    return ListaDeAcuerdoOut.from_orm(resultado)


@v1_listas_de_acuerdos.get("/{lista_de_acuerdo_id}", response_model=ListaDeAcuerdoOut)
async def detalle_lista_de_acuerdos(
    lista_de_acuerdo_id: int,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una lista de acuerdos a partir de su id"""
    if not current_user.permissions & Permiso.VER_JUSTICIABLES == Permiso.VER_JUSTICIABLES:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        consulta = get_lista_de_acuerdo(db, lista_de_acuerdo_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    return ListaDeAcuerdoOut.from_orm(consulta)
