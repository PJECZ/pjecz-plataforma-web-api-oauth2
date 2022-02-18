"""
Plataforma Web API OAuth2
"""
from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from fastapi_pagination import add_pagination

from config.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from lib.database import get_db

from plataforma_web.v1.autoridades.paths import autoridades
from plataforma_web.v1.distritos.paths import distritos
from plataforma_web.v1.funcionarios.paths import funcionarios
from plataforma_web.v1.listas_de_acuerdos.paths import listas_de_acuerdos
from plataforma_web.v1.listas_de_acuerdos_acuerdos.paths import listas_de_acuerdos_acuerdos
from plataforma_web.v1.materias.paths import materias
from plataforma_web.v1.materias_tipos_juicios.paths import materias_tipos_juicios
from plataforma_web.v1.modulos.paths import modulos
from plataforma_web.v1.permisos.paths import permisos
from plataforma_web.v1.roles.paths import roles
from plataforma_web.v1.sentencias.paths import sentencias
from plataforma_web.v1.soportes_categorias.paths import soportes_categorias
from plataforma_web.v1.soportes_tickets.paths import soportes_tickets
from plataforma_web.v1.usuarios.paths import usuarios
from plataforma_web.v1.usuarios_roles.paths import usuarios_roles

from plataforma_web.v1.usuarios.authentications import authenticate_user, create_access_token, get_current_active_user
from plataforma_web.v1.usuarios.schemas import Token, UsuarioInDB

app = FastAPI(
    title="Plataforma Web API OAuth2",
    description="Información del Sitio Web www.pjecz.gob.mx",
)

app.include_router(autoridades)
app.include_router(distritos)
app.include_router(funcionarios)
app.include_router(listas_de_acuerdos)
app.include_router(listas_de_acuerdos_acuerdos)
app.include_router(materias)
app.include_router(materias_tipos_juicios)
app.include_router(modulos)
app.include_router(permisos)
app.include_router(roles)
app.include_router(sentencias)
app.include_router(soportes_categorias)
app.include_router(soportes_tickets)
app.include_router(usuarios)
app.include_router(usuarios_roles)

add_pagination(app)


@app.get("/")
async def root():
    """Mensaje de Bienvenida"""
    return {"message": "Bienvenido a Plataforma Web API OAuth2 del Poder Judicial del Estado de Coahuila de Zaragoza."}


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Entregar el token como un JSON"""
    usuario = authenticate_user(form_data.username, form_data.password, db)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": usuario.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/usuarios/yo/", response_model=UsuarioInDB)
async def read_users_me(current_user: UsuarioInDB = Depends(get_current_active_user)):
    """Mostrar el perfil del usuario"""
    return current_user
