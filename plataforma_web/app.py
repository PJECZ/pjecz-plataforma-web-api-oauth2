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

from plataforma_web.v1.autoridades.paths import router as v1_autoridades
from plataforma_web.v1.distritos.paths import router as v1_distritos
from plataforma_web.v1.materias.paths import router as v1_materias
from plataforma_web.v1.roles.paths import router as v1_roles
from plataforma_web.v1.usuarios.paths import router as v1_usuarios

from plataforma_web.v1.usuarios.authentications import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    oauth2_scheme,
)
from plataforma_web.v1.usuarios.schemas import Token, UsuarioInBD

app = FastAPI()

app.include_router(v1_autoridades, prefix=f"/v1/autoridades")
app.include_router(v1_distritos, prefix=f"/v1/distritos")
# app.include_router(listas_de_acuerdos, prefix=f"/v1/listas_de_acuerdos")
# app.include_router(listas_de_acuerdos_acuerdos, prefix=f"/v1/listas_de_acuerdos_acuerdos")
app.include_router(v1_materias, prefix=f"/v1/materias")
app.include_router(v1_roles, prefix=f"/v1/roles")
app.include_router(v1_usuarios, prefix=f"/v1/usuarios")

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


@app.get("/usuarios/yo/", response_model=UsuarioInBD)
async def read_users_me(current_user: UsuarioInBD = Depends(get_current_active_user)):
    """Mostrar el perfil del usuario"""
    return current_user
