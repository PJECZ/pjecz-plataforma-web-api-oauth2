"""
Soportes Tickets v1, rutas (paths)
"""
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PWAnyError
from lib.fastapi_pagination_custom_list import CustomList, ListResult, custom_list_success_false
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from .crud import get_soportes_tickets, get_soporte_ticket, get_cantidades_por_distrito_por_categoria, get_cantidades_por_funcionario_por_estado
from .schemas import SoporteTicketOut, OneSoporteTicketOut, SoporteTicketTotalOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

soportes_tickets = APIRouter(prefix="/v1/soportes_tickets", tags=["soportes"])


@soportes_tickets.get("", response_model=CustomPage[SoporteTicketOut])
async def listado_soportes_tickets(
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    descripcion: str = None,
    estado: str = None,
    estatus: str = None,
    soporte_categoria_id: int = None,
    oficina_id: int = None,
    oficina_clave: str = None,
    usuario_id: int = None,
    usuario_email: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de tickets de soporte"""
    if current_user.permissions.get("SOPORTES TICKETS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        consulta = get_soportes_tickets(
            db,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            descripcion=descripcion,
            estado=estado,
            estatus=estatus,
            soporte_categoria_id=soporte_categoria_id,
            oficina_id=oficina_id,
            oficina_clave=oficina_clave,
            usuario_id=usuario_id,
            usuario_email=usuario_email,
        )
    except PWAnyError as error:
        return custom_page_success_false(error)
    return paginate(consulta)


@soportes_tickets.get("/cantidades_por_distrito_por_categoria", response_model=CustomList[SoporteTicketTotalOut])
async def cantidades_por_distrito_por_categoria(
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    size: int = 100,
):
    """Listado de totales de tickets por oficina y por categoria"""
    if current_user.permissions.get("SOPORTES TICKETS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cantidades_por_distrito_por_categoria(
            db=db,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            size=size,
        )
    except PWAnyError as error:
        return custom_list_success_false(error)
    items = []
    for distrito_clave, soporte_categoria_nombre, cantidad in resultados.all():
        items.append(SoporteTicketTotalOut(distrito_clave=distrito_clave, soporte_categoria_nombre=soporte_categoria_nombre, cantidad=cantidad))
    total = sum(item.cantidad for item in items)
    result = ListResult(total=total, items=items, size=size)
    return CustomList(result=result)


@soportes_tickets.get("/cantidades_por_funcionario_por_estado", response_model=CustomList[SoporteTicketTotalOut])
async def cantidades_por_funcionario_por_estado(
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    size: int = 100,
):
    """Listado de totales de tickets por oficina y por categoria"""
    if current_user.permissions.get("SOPORTES TICKETS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cantidades_por_funcionario_por_estado(
            db=db,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            size=size,
        )
    except PWAnyError as error:
        return custom_list_success_false(error)
    items = []
    for tecnico, estado, cantidad in resultados.all():
        items.append(SoporteTicketTotalOut(tecnico=tecnico, estado=estado, cantidad=cantidad))
    total = sum(item.cantidad for item in items)
    result = ListResult(total=total, items=items, size=size)
    return CustomList(result=result)


@soportes_tickets.get("/{soporte_ticket_id}", response_model=OneSoporteTicketOut)
async def detalle_soporte_ticket(
    soporte_ticket_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una ticket a partir de su id"""
    if current_user.permissions.get("SOPORTES TICKETS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        soporte_ticket = get_soporte_ticket(
            db=db,
            soporte_ticket_id=soporte_ticket_id,
        )
    except PWAnyError as error:
        return OneSoporteTicketOut(success=False, message=str(error))
    return OneSoporteTicketOut.from_orm(soporte_ticket)
