"""
Configuración para producción
"""
import os

import pytz


# Database
DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_NAME = os.environ.get("DB_NAME", "pjecz_plataforma_web")
DB_PASS = os.environ.get("DB_PASS", "wrongpassword")
DB_USER = os.environ.get("DB_USER", "nouser")

# PostgreSQL
SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

# Always in False
SQLALCHEMY_TRACK_MODIFICATIONS = False

# OAuth2
SECRET_KEY = os.environ.get("SECRET_KEY")  # openssl rand -hex 32
ALGORITHM = os.environ.get("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# CORS or "Cross-Origin Resource Sharing" refers to the situations when a frontend
# running in a browser has JavaScript code that communicates with a backend,
# and the backend is in a different "origin" than the frontend.
# https://fastapi.tiangolo.com/tutorial/cors/
ORIGINS = [
    "https://plataforma-web.justiciadigital.gob.mx",
]

# Huso horario
SERVIDOR_HUSO_HORARIO = pytz.utc
LOCAL_HUSO_HORARIO = pytz.timezone("America/Mexico_City")
