"""
Roles, CRUD: the four basic operations (create, read, update, and delete) of data storage
"""
from sqlalchemy.orm import Session
from plataforma_web.roles.models import Rol


def get_roles(db: Session):
    """Consultar roles activos"""
    return db.query(Rol).filter(Rol.estatus == "A").order_by(Rol.nombre).all()


def get_rol(db: Session, rol_id: int):
    """Consultar un rol"""
    return db.query(Rol).get(rol_id)
