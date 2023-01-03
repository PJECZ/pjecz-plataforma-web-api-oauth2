"""
Materias Tipos Juicios v1, rutas (paths)
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

from .crud import get_materias_tipos_juicios, get_materia_tipo_juicio
from .schemas import MateriaTipoJuicioOut, OneMateriaTipoJuicioOut

materias_tipos_juicios = APIRouter(prefix="/v1/materias_tipos_juicios", tags=["catalogos"])


@materias_tipos_juicios.get("", response_model=CustomPage[MateriaTipoJuicioOut])
async def listado_materias_tipos_juicios(
    estatus: str = None,
    materia_id: int = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de tipos de juicios de las materias"""
    if current_user.permissions.get("MATERIAS TIPOS JUICIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        consulta = get_materias_tipos_juicios(
            db=db,
            estatus=estatus,
            materia_id=materia_id,
        )
    except PWAnyError as error:
        return custom_page_success_false(error)
    return paginate(consulta)


@materias_tipos_juicios.get("/{materia_tipo_juicio_id}", response_model=OneMateriaTipoJuicioOut)
async def detalle_materia_tipo_juicio(
    materia_tipo_juicio_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una materia_tipo_juicio a partir de su id"""
    if current_user.permissions.get("MATERIAS TIPOS JUICIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        materia_tipo_juicio = get_materia_tipo_juicio(
            db=db,
            materia_tipo_juicio_id=materia_tipo_juicio_id,
        )
    except PWAnyError as error:
        return OneMateriaTipoJuicioOut(success=False, message=str(error))
    return OneMateriaTipoJuicioOut.from_orm(materia_tipo_juicio)
