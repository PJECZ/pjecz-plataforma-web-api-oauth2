"""
Autentificaciones
"""
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from config.settings import SECRET_KEY, ALGORITHM
from lib.database import get_db
from plataforma_web.usuarios.models import Usuario as User
from plataforma_web.usuarios.schemas import TokenData, Usuario, UsuarioEnBD

#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
pwd_context = CryptContext(schemes=["pbkdf2_sha256", "des_crypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str, db: Session = Depends(get_db)):
    """Obtener el usuario a partir de su e-mail"""
    usuario = db.query(User).filter(User.email == username).first()
    if usuario:
        datos = {
            "username": usuario.email,
            "id": usuario.id,
            "distrito_id": usuario.autoridad.distrito_id,
            "distrito": usuario.autoridad.distrito.nombre,
            "autoridad_id": usuario.autoridad_id,
            "autoridad": usuario.autoridad.descripcion,
            "rol_id": usuario.rol_id,
            "rol": usuario.rol.nombre,
            "email": usuario.email,
            "nombres": usuario.nombres,
            "apellido_paterno": usuario.apellido_paterno,
            "apellido_materno": usuario.apellido_materno,
            "hashed_password": usuario.contrasena,
            "disabled": usuario.estatus != "A",
        }
        return UsuarioEnBD(**datos)


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    """Autentificar el usuario"""
    user = get_user(username, db)
    print(repr(user))
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(token_data.username, db)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Usuario = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
