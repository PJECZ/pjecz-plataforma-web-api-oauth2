"""
CLI Config Settings
"""
import os

from dotenv import load_dotenv
import pytz

load_dotenv()

# Host y URL base
HOST = os.getenv("HOST", "http://127.0.0.1:8002")
BASE_URL = f"{HOST}/v1"

# Limit y timeout por defecto en segundos
LIMIT = int(os.getenv("LIMIT", "40"))
TIMEOUT = int(os.getenv("LIMIT", "12"))

# Usuario y contraseña
USERNAME = os.getenv("USERNAME", "")
PASSWORD = os.getenv("PASSWORD", "")

# Huso horario local
# Tome el tiempo de creacion
#     creado = datetime.fromisoformat(registro["creado"])
# Y convierta a un texto en tiempo local
#     creado.astimezone(LOCAL_HUSO_HORARIO).strftime("%Y-%m-%d %H:%M:%S")
LOCAL_HUSO_HORARIO = pytz.timezone("America/Mexico_City")
