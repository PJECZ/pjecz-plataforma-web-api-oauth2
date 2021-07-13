"""
Configuración para producción
"""
import os


# MySQL en Google Cloud
DB_USER = os.environ.get("DB_USER", "wronguser")
DB_PASS = os.environ.get("DB_PASS", "badpassword")
DB_NAME = os.environ.get("DB_NAME", "pjecz_plataforma_web")
DB_SOCKET_DIR = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
CLOUD_SQL_CONNECTION_NAME = os.environ.get("CLOUD_SQL_CONNECTION_NAME", "none")
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@/{DB_NAME}?unix_socket={DB_SOCKET_DIR}/{CLOUD_SQL_CONNECTION_NAME}"

# OAuth2
SECRET_KEY = os.environ.get("SECRET_KEY") # openssl rand -hex 32
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
