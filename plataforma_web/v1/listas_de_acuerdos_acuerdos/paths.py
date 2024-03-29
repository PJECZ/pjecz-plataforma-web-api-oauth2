"""
Listas de Acuerdos, Acuerdos v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PWAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from ...core.permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

from .crud import get_acuerdos, get_acuerdo, insert_acuerdo
from .schemas import ListaDeAcuerdoAcuerdoIn, ListaDeAcuerdoAcuerdoOut, OneListaDeAcuerdoAcuerdoOut

listas_de_acuerdos_acuerdos = APIRouter(prefix="/v1/listas_de_acuerdos", tags=["listas de acuerdos"])


@listas_de_acuerdos_acuerdos.get("/{lista_de_acuerdo_id}/acuerdos", response_model=CustomPage[ListaDeAcuerdoAcuerdoOut])
async def listado_acuerdos(
    lista_de_acuerdo_id: int,
    estatus: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de Acuerdos de una Lista de Acuerdos"""
    if current_user.permissions.get("LISTAS DE ACUERDOS ACUERDOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        consulta = get_acuerdos(
            db=db,
            estatus=estatus,
            lista_de_acuerdo_id=lista_de_acuerdo_id,
        )
    except PWAnyError as error:
        return custom_page_success_false(error)
    return paginate(consulta)


# @listas_de_acuerdos_acuerdos.post("/{lista_de_acuerdo_id}/acuerdos", response_model=OneListaDeAcuerdoAcuerdoOut)
# async def nuevo_acuerdo(
#     acuerdo: ListaDeAcuerdoAcuerdoIn,
#     current_user: UsuarioInDB = Depends(get_current_active_user),
#     db: Session = Depends(get_db),
# ):
#     """Insertar un acuerdo"""
#     if current_user.permissions.get("LISTAS DE ACUERDOS ACUERDOS", 0) < Permiso.CREAR:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
#     try:
#         acuerdo = insert_acuerdo(
#             db=db,
#             acuerdo=acuerdo,
#         )
#     except PWAnyError as error:
#         return OneListaDeAcuerdoAcuerdoOut(success=False, message=str(error))
#     return OneListaDeAcuerdoAcuerdoOut.from_orm(acuerdo)


@listas_de_acuerdos_acuerdos.get("/{lista_de_acuerdo_id}/acuerdos/{lista_de_acuerdo_acuerdo_id}", response_model=OneListaDeAcuerdoAcuerdoOut)
async def detalle_acuerdo(
    lista_de_acuerdo_acuerdo_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una acuerdo a partir de su id"""
    if current_user.permissions.get("LISTAS DE ACUERDOS ACUERDOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        acuerdo = get_acuerdo(
            db=db,
            lista_de_acuerdo_acuerdo_id=lista_de_acuerdo_acuerdo_id,
        )
    except PWAnyError as error:
        return OneListaDeAcuerdoAcuerdoOut(success=False, message=str(error))
    return OneListaDeAcuerdoAcuerdoOut.from_orm(acuerdo)
