"""
FastAPI App
"""
from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from fastapi_pagination import add_pagination

from config.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from lib.database import get_db

from plataforma_web.autoridades.views import router as autoridades
from plataforma_web.distritos.views import router as distritos
from plataforma_web.listas_de_acuerdos.views import router as listas_de_acuerdos
from plataforma_web.listas_de_acuerdos_acuerdos.views import router as listas_de_acuerdos_acuerdos
from plataforma_web.materias.views import router as materias
from plataforma_web.roles.views import router as roles
from plataforma_web.usuarios.views import router as usuarios

from plataforma_web.usuarios.authentications import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    oauth2_scheme,
)
from plataforma_web.usuarios.schemas import Token, UsuarioEnBD

VERSION = "v1.0"

app = FastAPI()

app.include_router(autoridades, prefix=f"/api/{VERSION}/autoridades")
app.include_router(distritos, prefix=f"/api/{VERSION}/distritos")
app.include_router(listas_de_acuerdos, prefix=f"/api/{VERSION}/listas_de_acuerdos")
app.include_router(listas_de_acuerdos_acuerdos, prefix=f"/api/{VERSION}/listas_de_acuerdos_acuerdos")
app.include_router(materias, prefix=f"/api/{VERSION}/materias")
app.include_router(roles, prefix=f"/api/{VERSION}/roles")
app.include_router(usuarios, prefix=f"/api/{VERSION}/usuarios")

add_pagination(app)


@app.get("/")
async def root(token: str = Depends(oauth2_scheme)):
    """Mensaje de Bienvenida"""
    # return {"message": "Hola. Soy 'Plataforma Web API OAuth2' del Poder Judicial del Estado de Coahuila de Zaragoza."}
    return {"token": token}


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


@app.get("/usuarios/yo/", response_model=UsuarioEnBD)
async def read_users_me(current_user: UsuarioEnBD = Depends(get_current_active_user)):
    """Mostrar el perfil del usuario"""
    return current_user
