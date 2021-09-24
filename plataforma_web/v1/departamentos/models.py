"""
Departamentos v1.0, modelos
"""
from plataforma_web.v1.distritos.models import Distrito


class Departamento(Distrito):
    """Departamento"""

    def __repr__(self):
        """Representación"""
        return f"<Departamento {self.nombre}>"
