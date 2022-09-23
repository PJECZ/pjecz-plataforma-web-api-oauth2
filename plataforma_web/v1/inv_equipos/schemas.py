"""
Inventario Equipos v1, esquemas de pydantic
"""
from datetime import date, datetime
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class InvEquipoOut(BaseModel):
    """Esquema para entregar equipos"""

    id: int | None
    inv_custodia_id: int | None
    inv_custodia_nombre_completo: str | None
    inv_marca_id: int | None
    inv_marca_nombre: str | None
    inv_modelo_id: int | None
    inv_modelo_descripcion: str | None
    inv_red_id: int | None
    inv_red_nombre: str | None
    fecha_fabricacion: date | None
    numero_serie: str | None
    numero_inventario: int | None
    descripcion: str | None
    tipo: str | None
    direccion_ip: str | None
    direccion_mac: str | None
    numero_nodo: int | None
    numero_switch: int | None
    numero_puerto: int | None
    creado: datetime | None

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
    anio_fabricacion: int | None
    cantidad: int
