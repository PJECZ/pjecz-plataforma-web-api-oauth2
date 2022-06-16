"""
Inventarios Categorias v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.fastapi_pagination import LimitOffsetPage

from plataforma_web.v1.inv_categorias.crud import get_inv_categoria, get_inv_categorias
from plataforma_web.v1.inv_categorias.schemas import InvCategoriaOut
from plataforma_web.v1.permisos.models import Permiso
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInDB

inv_categorias = APIRouter(prefix="/v1/inv_categorias", tags=["inventarios"])


@inv_categorias.get("", response_model=LimitOffsetPage[InvCategoriaOut])
async def listado_inv_categorias(
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de categorias"""
    if "INV CATEGORIAS" not in current_user.permissions or current_user.permissions["INV CATEGORIAS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_inv_categorias(db)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@inv_categorias.get("/{inv_categoria_id}", response_model=InvCategoriaOut)
async def detalle_inv_categoria(
    inv_categoria_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una categorias a partir de su id"""
    if "INV CATEGORIAS" not in current_user.permissions or current_user.permissions["INV CATEGORIAS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        inv_categoria = get_inv_categoria(db, inv_categoria_id=inv_categoria_id)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return InvCategoriaOut.from_orm(inv_categoria)