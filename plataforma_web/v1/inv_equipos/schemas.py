"""
Inventario Equipos v1, esquemas de pydantic
"""
from datetime import date
from pydantic import BaseModel


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
    fecha_fabricacion: date
    numero_serie: str
    numero_inventario: int
    descripcion: str
    tipo: str
    direccion_ip: str
    direccion_mac: str
    numero_nodo: int
    numero_switch: int
    numero_puerto: int

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class CantidadesOficinaTipoOut(BaseModel):
    """Cantidades de equipos por tipo y oficina"""

    oficina_clave: str
    inv_equipo_tipo: str
    cantidad: int
