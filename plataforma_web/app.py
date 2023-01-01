"""
Plataforma Web API OAuth2
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from config.settings import get_settings

from .v1.abogados.paths import abogados
from .v1.autoridades.paths import autoridades
from .v1.centros_trabajos.paths import centros_trabajos
from .v1.distritos.paths import distritos
from .v1.domicilios.paths import domicilios
from .v1.edictos.paths import edictos
from .v1.funcionarios.paths import funcionarios
from .v1.glosas.paths import glosas
from .v1.inv_categorias.paths import inv_categorias
from .v1.inv_componentes.paths import inv_componentes
from .v1.inv_custodias.paths import inv_custodias
from .v1.inv_equipos.paths import inv_equipos
from .v1.inv_marcas.paths import inv_marcas
from .v1.inv_modelos.paths import inv_modelos
from .v1.inv_redes.paths import inv_redes
from .v1.listas_de_acuerdos.paths import listas_de_acuerdos
from .v1.listas_de_acuerdos_acuerdos.paths import listas_de_acuerdos_acuerdos
from .v1.materias.paths import materias
from .v1.materias_tipos_juicios.paths import materias_tipos_juicios
from .v1.modulos.paths import modulos
from .v1.oficinas.paths import oficinas
from .v1.permisos.paths import permisos
from .v1.redams.paths import redams
from .v1.repsvm_agresores.paths import repsvm_agresores
from .v1.repsvm_agresores_delitos.paths import repsvm_agresores_delitos
from .v1.repsvm_delitos.paths import repsvm_delitos
from .v1.roles.paths import roles
from .v1.sentencias.paths import sentencias
from .v1.soportes_categorias.paths import soportes_categorias
from .v1.soportes_tickets.paths import soportes_tickets
from .v1.ubicaciones_expedientes.paths import ubicaciones_expedientes
from .v1.usuarios.paths import usuarios
from .v1.usuarios_roles.paths import usuarios_roles

settings = get_settings()

# FastAPI
app = FastAPI(
    title="Plataforma Web API OAuth2",
    description="Información del Sitio Web www.pjecz.gob.mx",
)

# CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins.split(","),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
app.include_router(abogados)
app.include_router(autoridades)
app.include_router(centros_trabajos)
app.include_router(distritos)
app.include_router(domicilios)
app.include_router(edictos)
app.include_router(funcionarios)
app.include_router(glosas)
app.include_router(inv_categorias)
app.include_router(inv_componentes)
app.include_router(inv_custodias)
app.include_router(inv_equipos)
app.include_router(inv_marcas)
app.include_router(inv_modelos)
app.include_router(inv_redes)
app.include_router(listas_de_acuerdos)
app.include_router(listas_de_acuerdos_acuerdos)
app.include_router(materias)
app.include_router(materias_tipos_juicios)
app.include_router(modulos)
app.include_router(oficinas)
app.include_router(permisos)
app.include_router(redams)
app.include_router(repsvm_agresores)
app.include_router(repsvm_agresores_delitos)
app.include_router(repsvm_delitos)
app.include_router(roles)
app.include_router(sentencias)
app.include_router(soportes_categorias)
app.include_router(soportes_tickets)
app.include_router(ubicaciones_expedientes)
app.include_router(usuarios)
app.include_router(usuarios_roles)

# Pagination
add_pagination(app)


@app.get("/")
async def root():
    """Mensaje de Bienvenida"""
    return {"message": "Bienvenido a Plataforma Web API OAuth2 del Poder Judicial del Estado de Coahuila de Zaragoza."}
