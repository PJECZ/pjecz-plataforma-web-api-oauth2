"""
Soportes Categorias v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.fastapi_pagination import LimitOffsetPage

from plataforma_web.v1.soportes_categorias.crud import get_soportes_categorias, get_soporte_categoria
from plataforma_web.v1.soportes_categorias.schemas import SoporteCategoriaOut
from plataforma_web.v1.permisos.models import Permiso
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInBD

router = APIRouter()


@router.get("", response_model=LimitOffsetPage[SoporteCategoriaOut])
async def listado_soportes_categorias(
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de Soporte Categorias"""
    if not current_user.permissions["SOPORTE CATEGORIA"] >= Permiso.VER:
        raise HTTPException(status_code=403, detail="Forbidden")
    return paginate(get_soportes_categorias(db))


@router.get("/{soporte_categoria_id}", response_model=SoporteCategoriaOut)
async def detalle_soporte_categoria(
    soporte_categoria_id: int,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una Soporte Categoria a partir de su id"""
    if not current_user.permissions["SOPORTE CATEGORIA"] >= Permiso.VER:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        soporte_categoria = get_soporte_categoria(db, soporte_categoria_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return SoporteCategoriaOut.from_orm(soporte_categoria)
