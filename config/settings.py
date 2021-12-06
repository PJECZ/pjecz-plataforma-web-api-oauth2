"""
Configuración para producción
"""
import os


# Google Cloud SQL
DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_NAME = os.environ.get("DB_NAME", "pjecz_plataforma_web")
DB_PASS = os.environ.get("DB_PASS", "wrongpassword")
DB_USER = os.environ.get("DB_USER", "nouser")
DB_SOCKET_DIR = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
CLOUD_SQL_CONNECTION_NAME = os.environ.get("CLOUD_SQL_CONNECTION_NAME", "none")

# DESHABILITADO Google Cloud SQL a Ceres con MySQL
# SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@/{DB_NAME}?unix_socket={DB_SOCKET_DIR}/{CLOUD_SQL_CONNECTION_NAME}"

# NUEVO Google Cloud SQL a Minerva con PostgreSQL
SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

# Always in False
SQLALCHEMY_TRACK_MODIFICATIONS = False

# OAuth2
SECRET_KEY = os.environ.get("SECRET_KEY") # openssl rand -hex 32
ALGORITHM = os.environ.get("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
