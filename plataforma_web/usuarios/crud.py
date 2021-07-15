"""
Usuarios, CRUD: the four basic operations (create, read, update, and delete) of data storage
"""
from sqlalchemy.orm import Session

from plataforma_web.autoridades.models import Autoridad
from plataforma_web.distritos.models import Distrito
from plataforma_web.roles.models import Rol
from plataforma_web.usuarios.models import Usuario


def get_usuarios(db: Session, autoridad_id: int = None):
    """ Consultar usuarios """
    consulta = db.query(Usuario, Autoridad, Distrito, Rol).select_from(Usuario).join(Autoridad).join(Distrito).join(Rol)
    if autoridad_id:
        consulta = consulta.filter(Usuario.autoridad_id == autoridad_id)
    return consulta.filter(Usuario.estatus == 'A').limit(400).all()


def get_usuario(db: Session, usuario_id: int):
    """ Consultar un usuario """
    return db.query(Usuario).get(usuario_id)
