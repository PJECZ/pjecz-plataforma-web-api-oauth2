"""
FastAPI App
"""
from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from plataforma_web.autoridades.views import router as autoridades
from plataforma_web.distritos.views import router as distritos
from plataforma_web.listas_de_acuerdos.views import router as listas_de_acuerdos
from plataforma_web.listas_de_acuerdos_acuerdos.views import router as listas_de_acuerdos_acuerdos
from plataforma_web.materias.views import router as materias
from plataforma_web.roles.views import router as roles
from plataforma_web.usuarios.views import router as usuarios

from plataforma_web.usuarios.authentications import authenticate_user, create_access_token, get_current_active_user, fake_users_db, oauth2_scheme
from plataforma_web.usuarios.models import Usuario
from plataforma_web.usuarios.schemas import Token

from config.settings import ACCESS_TOKEN_EXPIRE_MINUTES

app = FastAPI()

app.include_router(autoridades, prefix="/autoridades")
app.include_router(distritos, prefix="/distritos")
app.include_router(listas_de_acuerdos, prefix="/listas_de_acuerdos")
app.include_router(listas_de_acuerdos_acuerdos, prefix="/listas_de_acuerdos_acuerdos")
app.include_router(materias, prefix="/materias")
app.include_router(roles, prefix="/roles")
app.include_router(usuarios, prefix="/usuarios")


@app.get("/")
async def root(token: str = Depends(oauth2_scheme)):
    """Mensaje de Bienvenida"""
    # return {"message": "Hola. Soy 'Plataforma Web API OAuth2' del Poder Judicial del Estado de Coahuila de Zaragoza."}
    return {"token": token}


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=Usuario)
async def read_users_me(current_user: Usuario = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: Usuario = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]
