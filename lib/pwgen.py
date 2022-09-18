"""
Generador de contraseñas
"""
import random
import re
import string

from hashids import Hashids

from lib.safe_string import CONTRASENA_REGEXP


def generar_api_key(hashid: str, email: str, length: int = 24) -> str:
    """Generar API key que se compone de un hashid y una cadena aleatoria"""
    aleatorio = "".join(random.sample(string.ascii_letters + string.digits, k=length))
    hash_email = Hashids(salt=email, min_length=8).encode(1)
    return hashid + "." + hash_email + "." + aleatorio


def generar_codigo_asistencia(largo: int = 4) -> str:
    """Generar código asistencia"""
    return "".join(random.sample(string.digits, k=largo))


def generar_contrasena(largo: int = 16) -> str:
    """Generar contraseña que tenga por lo menos una mayúscula y un número"""
    temp = ""
    while not re.fullmatch(CONTRASENA_REGEXP, temp):
        temp = "".join(random.sample(string.ascii_letters + string.digits, k=largo))
    return temp
