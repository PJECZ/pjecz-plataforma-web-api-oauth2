"""
Materias Tipos Juicios v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.fastapi_pagination import LimitOffsetPage

from plataforma_web.v1.materias_tipos_juicios.crud import get_materias_tipos_juicios, get_materia_tipo_juicio
from plataforma_web.v1.materias_tipos_juicios.schemas import MateriaTipoJuicioOut
from plataforma_web.v1.permisos.models import Permiso
from plataforma_web.v1.sentencias.crud import get_sentencias
from plataforma_web.v1.sentencias.schemas import SentenciaOut
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInDB

materias_tipos_juicios = APIRouter(prefix="/v1/materias", tags=["materias"])


@materias_tipos_juicios.get("/{materia_id}/tipos_juicios", response_model=LimitOffsetPage[MateriaTipoJuicioOut])
async def listado_materias_tipos_juicios(
    materia_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de tipos de juicios de una materia"""
    if "MATERIAS TIPOS JUICIOS" not in current_user.permissions or current_user.permissions["MATERIAS TIPOS JUICIOS"] < Permiso.VER:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        listado = get_materias_tipos_juicios(db, materia_id=materia_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@materias_tipos_juicios.get("/{materia_id}/tipos_juicios/{tipo_juicio_id}", response_model=MateriaTipoJuicioOut)
async def detalle_materia_tipo_juicio(
    materia_id: int,
    tipo_juicio_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una materia_tipo_juicio a partir de su id"""
    if "MATERIAS TIPOS JUICIOS" not in current_user.permissions or current_user.permissions["MATERIAS TIPOS JUICIOS"] < Permiso.VER:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        materia_tipo_juicio = get_materia_tipo_juicio(db, materia_tipo_juicio_id=tipo_juicio_id)
        if materia_tipo_juicio.materia_id != materia_id:
            raise ValueError("No corresponde la materia al tipo de juicio")
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return MateriaTipoJuicioOut.from_orm(materia_tipo_juicio)


@materias_tipos_juicios.get("/{materia_id}/tipos_juicios/{tipo_juicio_id}/sentencias", response_model=LimitOffsetPage[SentenciaOut])
async def listado_materias_tipos_juicios_sentencias(
    materia_id: int,
    tipo_juicio_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de sentencias de un tipo de juicio"""
    if "SENTENCIAS" not in current_user.permissions or current_user.permissions["SENTENCIAS"] < Permiso.VER:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        materia_tipo_juicio = get_materia_tipo_juicio(db, tipo_juicio_id)
        if materia_tipo_juicio.materia_id != materia_id:
            raise ValueError("No corresponde la materia al tipo de juicio")
        listado = get_sentencias(db, materia_tipo_juicio_id=tipo_juicio_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)
