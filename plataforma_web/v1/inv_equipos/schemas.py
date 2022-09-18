"""
Inventario Equipos v1, esquemas de pydantic
"""
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class InvEquipoOut(BaseModel):
    """Esquema para entregar equipos"""

    id: int
    inv_custodia_id: int
    inv_custodia_nombre_completo: str
    inv_marca_id: int
    inv_marca_nombre: str
    inv_modelo_id: int
    inv_modelo_descripcion: str
    inv_red_id: int
    inv_red_nombre: str
    fecha_fabricacion: Optional[date] = None
    numero_serie: str
    numero_inventario: Optional[int] = None
    descripcion: str
    tipo: str
    direccion_ip: Optional[str] = None
    direccion_mac: Optional[str] = None
    numero_nodo: Optional[int] = None
    numero_switch: Optional[int] = None
    numero_puerto: Optional[int] = None
    creado: datetime

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneInvEquipoOut(InvEquipoOut, OneBaseOut):
    """Esquema para entregar un distrito"""


class CantidadesOficinaTipoOut(BaseModel):
    """Cantidades de equipos por oficina y tipo de equipo"""

    oficina_clave: str
    inv_equipo_tipo: str
    cantidad: int


class CantidadesOficinaAnioFabricacionOut(BaseModel):
    """Cantidades de equipos por oficina y año de fabricacion"""

    oficina_clave: str
    anio_fabricacion: Optional[int] = None
    cantidad: int
