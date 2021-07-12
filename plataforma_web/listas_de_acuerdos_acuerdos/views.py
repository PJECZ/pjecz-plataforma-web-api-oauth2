"""
Listas de Acuerdos Acuerdos, vistas
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from plataforma_web.listas_de_acuerdos.crud import get_lista_de_acuerdo
from plataforma_web.listas_de_acuerdos_acuerdos import crud, schemas
from lib.database import get_db

router = APIRouter()


@router.get("", response_model=List[schemas.ListaDeAcuerdoAcuerdo])
async def listar_listas_de_acuerdos_acuerdos(lista_de_acuerdo_id: int, db: Session = Depends(get_db)):
    """Lista de listas_de_acuerdos_acuerdos"""
    lista_de_acuerdo = get_lista_de_acuerdo(db, lista_de_acuerdo_id=lista_de_acuerdo_id)
    if lista_de_acuerdo is None:
        raise HTTPException(status_code=400, detail="No existe la lista de acuerdos.")
    resultados = []
    for acuerdo, lista_de_acuerdo in crud.get_listas_de_acuerdos_acuerdos(db, lista_de_acuerdo_id=lista_de_acuerdo_id):
        resultados.append(
            schemas.ListaDeAcuerdoAcuerdo(
                id=acuerdo.id,
                lista_de_acuerdo_id=lista_de_acuerdo.id,
                fecha=lista_de_acuerdo.fecha,
                folio=acuerdo.folio,
                expediente=acuerdo.expediente,
                actor=acuerdo.actor,
                demandado=acuerdo.demandado,
                tipo_acuerdo=acuerdo.tipo_acuerdo,
                tipo_juicio=acuerdo.tipo_juicio,
            )
        )
    return resultados


@router.get("/{acuerdo_id}", response_model=schemas.ListaDeAcuerdoAcuerdo)
async def consultar_un_acuerdo(lista_de_acuerdo_acuerdo_id: int, db: Session = Depends(get_db)):
    """Consultar un acuerdo"""
    acuerdo = crud.get_lista_de_acuerdo_acuerdo(db, lista_de_acuerdo_acuerdo_id=lista_de_acuerdo_acuerdo_id)
    if acuerdo is None:
        raise HTTPException(status_code=400, detail="No existe el acuerdo.")
    return schemas.ListaDeAcuerdoAcuerdo(
        id=acuerdo.id,
        lista_de_acuerdo_id=acuerdo.lista_de_acuerdo_id,
        fecha=acuerdo.lista_de_acuerdo.fecha,
        folio=acuerdo.folio,
        expediente=acuerdo.expediente,
        actor=acuerdo.actor,
        demandado=acuerdo.demandado,
        tipo_acuerdo=acuerdo.tipo_acuerdo,
        tipo_juicio=acuerdo.tipo_juicio,
    )
